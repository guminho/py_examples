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


def infer_seq(seqid: int, model: str, values: list):
    outs = []
    count = 1
    for x in values:
        res = cli.infer(
            model_name=model,
            inputs=SimpleInput(x),
            outputs=OUTS,
            sequence_id=seqid,
            sequence_start=(count == 1),
            sequence_end=(count == len(values)),
        )
        outs.append(SimpleOutput(res))
        count += 1
    return outs


values = [11, 7, 5, 3, 2, 0, 1]
values2 = [-x for x in values]

# seq
outs0 = infer_seq(1000, MODEL_SEQ, [0] + values)
outs1 = infer_seq(1001, MODEL_SEQ, [100] + values2)
outs2 = infer_seq(str(uuid4()), MODEL_SEQ, [20] + values2)
assert outs0 == [1] + values
assert outs1 == [101] + values2
assert outs2 == [21] + values2

# dyna
outs0 = infer_seq(1000, MODEL_DYN, [0] + values)
outs1 = infer_seq(1001, MODEL_DYN, [100] + values2)
assert outs0 == [1] + [x + 1000 if x == 1 else x for x in values]
assert outs1 == [101] + [-x + 1001 if x == 1 else -x for x in values]
print("PASS")
