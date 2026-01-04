from time import sleep

import numpy as np
from tritonclient.grpc import InferenceServerClient as TritonClient
from tritonclient.grpc import InferInput, InferRequestedOutput, InferResult

cli = TritonClient("localhost:8001")
MODEL = "simple"
OUTS = [InferRequestedOutput(k) for k in ("OUTPUT0", "OUTPUT1")]


def SimpleInput(i0: list, i1: list):
    dats = (
        ("INPUT0", np.array([i0], np.int32)),
        ("INPUT1", np.array([i1], np.int32)),
    )
    return [InferInput(k, [1, 16], "INT32").set_data_from_numpy(x) for k, x in dats]


def SimpleOutput(res: InferResult):
    o0: list = res.as_numpy("OUTPUT0")[0].tolist()
    o1: list = res.as_numpy("OUTPUT1")[0].tolist()
    return o0, o1


def infer_simple(i0, i1: list[int]):
    outs = []
    cli.async_infer(
        model_name=MODEL,
        inputs=SimpleInput(i0, i1),
        outputs=OUTS,
        callback=lambda result, error: outs.append(error or result),
    )
    count = 0
    while len(outs) == 0 and count < 10:
        sleep(0.001)
        count += 1
    o0, o1 = SimpleOutput(outs[0])
    assert [x0 + x1 for x0, x1 in zip(i0, i1)] == o0
    assert [x0 - x1 for x0, x1 in zip(i0, i1)] == o1


infer_simple(list(range(0, 16)), [1] * 16)
print("PASS")
