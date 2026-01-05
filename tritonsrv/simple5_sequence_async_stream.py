from queue import Queue
from uuid import uuid4

import numpy as np
from tritonclient.grpc import InferenceServerClient as TritonClient
from tritonclient.grpc import InferInput, InferRequestedOutput, InferResult

cli = TritonClient("localhost:8001")
MODEL_SEQ = "simple_sequence"
MODEL_DYN = "simple_dyna_sequence"
OUTS = [InferRequestedOutput("OUTPUT")]


def SimpleInput(x: int):
    a = np.array([[x]], np.int32)
    return [InferInput("INPUT", a.shape, "INT32").set_data_from_numpy(a)]


def SimpleOutput(res: InferResult):
    return res.as_numpy("OUTPUT").item()


def stream_infer(seqid: int, model: str, values: list):
    count = 1
    for x in values:
        cli.async_stream_infer(
            model_name=model,
            inputs=SimpleInput(x),
            outputs=OUTS,
            request_id="{}_{}".format(seqid, count),
            sequence_id=seqid,
            sequence_start=(count == 1),
            sequence_end=(count == len(values)),
        )
        count += 1


values = [11, 7, 5, 3, 2, 0, 1]
values2 = [-x for x in values]
queue = Queue()
outs0, outs1, outs2, outs3, outs4 = [], [], [], [], []
with cli:
    cli.start_stream(
        callback=lambda result, error: queue.put(error or result),
    )
    # seq
    stream_infer(1000, MODEL_SEQ, [0] + values)
    stream_infer(1001, MODEL_SEQ, [100] + values2)
    stream_infer(str(uuid4()), MODEL_SEQ, [20] + values2)
    # dyna
    stream_infer(1002, MODEL_DYN, [0] + values)
    stream_infer(1003, MODEL_DYN, [100] + values2)

    for _ in range(5 * (len(values) + 1)):
        result: InferResult = queue.get(timeout=0.03)
        seqid = result._result.id.split("_")[0]
        out = SimpleOutput(result)
        if seqid == "1000":
            outs0.append(out)
        elif seqid == "1001":
            outs1.append(out)
        elif seqid == "1002":
            outs3.append(out)
        elif seqid == "1003":
            outs4.append(out)
        else:
            outs2.append(out)

assert outs0 == [1] + values
assert outs1 == [101] + values2
assert outs2 == [21] + values2
assert outs3 == [1] + [x + 1002 if x == 1 else x for x in values]
assert outs4 == [101] + [-x + 1003 if x == 1 else -x for x in values]
print("PASS")
