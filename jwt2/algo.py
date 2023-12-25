import abc
import hashlib
import hmac

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


class Algo(abc.ABC):
    name: str = None

    @abc.abstractmethod
    def sign(self, message: bytes, key: bytes) -> bytes:
        ...

    @abc.abstractmethod
    def verify(self, signature: bytes, message: bytes, key: bytes):
        ...


class HS256(Algo):
    name = "HS256"

    def sign(self, message: bytes, key: bytes):
        return hmac.digest(key, message, hashlib.sha256)

    def verify(self, signature: bytes, message: bytes, key: bytes):
        expected = hmac.digest(key, message, hashlib.sha256)
        assert hmac.compare_digest(signature, expected)


class RS256(Algo):
    name = "RS256"

    def sign(self, message: bytes, key: bytes) -> bytes:
        key: rsa.RSAPrivateKey = serialization.load_pem_private_key(key, None)
        return key.sign(message, padding.PKCS1v15(), hashes.SHA256())

    def verify(self, signature: bytes, message: bytes, key: bytes):
        key: rsa.RSAPublicKey = serialization.load_ssh_public_key(key)
        key.verify(signature, message, padding.PKCS1v15(), hashes.SHA256())
