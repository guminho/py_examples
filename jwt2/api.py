import base64

import orjson
from algo import Algo


def _base64url_encode(x: bytes):
    return base64.urlsafe_b64encode(x).replace(b"=", b"")


def _base64url_decode(x: bytes):
    rem = len(x) % 4
    if rem > 0:
        x += b"=" * (4 - rem)
    return base64.urlsafe_b64decode(x)


def encode(payload: dict, key: bytes, algorithm: Algo) -> bytes:
    option = orjson.OPT_SORT_KEYS
    header = {"typ": "JWT", "alg": algorithm.name}
    hd = _base64url_encode(orjson.dumps(header, option=option))
    pl = _base64url_encode(orjson.dumps(payload))
    hp = hd + b"." + pl
    sig = algorithm.sign(hp, key)
    sig = _base64url_encode(sig)
    tok = hp + b"." + sig
    return tok


def decode(token: bytes, key: bytes, algorithm: Algo) -> dict:
    hp, sig = token.rsplit(b".", 1)
    sig = _base64url_decode(sig)

    algorithm.verify(sig, hp, key)

    hd, pl = hp.split(b".", 1)
    hd = _base64url_decode(hd)
    pl = _base64url_decode(pl)
    return orjson.loads(pl)
