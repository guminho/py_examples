import jwt

import algo
import api

# keys
secret_key = b"world"
with open("KEY", "rb") as f:
    private_key = f.read()
with open("KEY.pub", "rb") as f:
    public_key = f.read()

# payload
payload = {"hello": "abc"}

# hs256
token = api.encode(payload, secret_key, algo.HS256())
print("token:", token)
print(token == jwt.encode(payload, secret_key, "HS256").encode())
rev = api.decode(token, secret_key, algo.HS256())
print(rev == jwt.decode(token, secret_key, "HS256"))

# rs256
token = api.encode(payload, private_key, algo.RS256())
print("token:", token)
print(token == jwt.encode(payload, private_key, "RS256").encode())
rev = api.decode(token, public_key, algo.RS256())
print(rev == jwt.decode(token, public_key, "RS256"))
