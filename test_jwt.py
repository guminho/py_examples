import base64
import hashlib
import hmac

import jwt
import orjson


def base64url_encode(x: bytes):
    return base64.urlsafe_b64encode(x).replace(b"=", b"")


def base64url_decode(x: bytes):
    rem = len(x) % 4
    if rem > 0:
        x += b"=" * (4 - rem)
    return base64.urlsafe_b64decode(x)


def encode_hs256(payload: dict, key: bytes) -> bytes:
    option = orjson.OPT_SORT_KEYS
    header = {"typ": "JWT", "alg": "HS256"}
    hd = base64url_encode(orjson.dumps(header, option=option))
    pl = base64url_encode(orjson.dumps(payload))
    hp = hd + b"." + pl
    sig = base64url_encode(hmac.digest(key, hp, hashlib.sha256))
    tok = hp + b"." + sig
    return tok


def decode_hs256(token: bytes, key: bytes) -> dict:
    hp, sig = token.rsplit(b".", 1)
    sig = base64url_decode(sig)
    sig1 = hmac.digest(key, hp, hashlib.sha256)
    assert hmac.compare_digest(sig, sig1)
    hd, pl = hp.split(b".", 1)
    hd = base64url_decode(hd)
    pl = base64url_decode(pl)
    return orjson.loads(pl)


payload = {"hello": "abc"}
key = b"world"

tok = encode_hs256(payload, key)
rev = decode_hs256(tok, key)

print("cmp:", tok, jwt.encode(payload, key).encode() == tok)
print("jwt:", rev, jwt.decode(tok, key, "HS256") == rev == payload)
