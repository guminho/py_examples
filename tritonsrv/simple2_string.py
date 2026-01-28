import numpy as np
from tritonclient.grpc import InferenceServerClient as TritonClient
from tritonclient.grpc import InferInput, InferRequestedOutput, InferResult

cli = TritonClient("localhost:8001")
MODEL_STR = "simple_string"
MODEL_IDT = "simple_identity"


def StringInput(i0: list, i1: list):
    a0 = [str(x).encode() for x in i0]
    a1 = [str(x).encode() for x in i1]
    dats = (
        ("INPUT0", np.array([a0], np.object_)),
        ("INPUT1", np.array([a1], np.object_)),
    )
    return [InferInput(k, [1, 16], "BYTES").set_data_from_numpy(x) for k, x in dats]


def StringOutput(res: InferResult):
    o0: list = res.as_numpy("OUTPUT0")[0].tolist()
    o1: list = res.as_numpy("OUTPUT1")[0].tolist()
    o0 = [int(x) for x in o0]
    o1 = [int(x) for x in o1]
    return o0, o1


def infer_string(i0, i1: list[int]):
    OUTS = [InferRequestedOutput(k) for k in ("OUTPUT0", "OUTPUT1")]

    res = cli.infer(
        model_name=MODEL_STR,
        inputs=StringInput(i0, i1),
        outputs=OUTS,
    )
    o0, o1 = StringOutput(res)
    assert [x0 + x1 for x0, x1 in zip(i0, i1)] == o0
    assert [x0 - x1 for x0, x1 in zip(i0, i1)] == o1


def IdentityInput(i0: list[bytes]):
    a = np.array([i0], np.object_)
    return [InferInput("INPUT0", a.shape, "BYTES").set_data_from_numpy(a)]


def IdentityOutput(res: InferResult):
    return res.as_numpy("OUTPUT0")[0].tolist()


def infer_identity(i0: list[bytes]):
    OUTS = [InferRequestedOutput("OUTPUT0")]

    res = cli.infer(
        model_name=MODEL_IDT,
        inputs=IdentityInput(i0),
        outputs=OUTS,
    )
    o0 = IdentityOutput(res)
    assert i0 == o0


infer_string(list(range(0, 16)), [1] * 16)
infer_identity([b"he\x00llo"] * 16)
infer_identity([b"\x00\x01\x02\x03"] * 32)
print("PASS")
