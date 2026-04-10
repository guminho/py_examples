from cryptography.fernet import Fernet

key = Fernet.generate_key()
print(f"Keep this safe: key={key.decode()}")

cipher_suite = Fernet(key)
cipher_text = cipher_suite.encrypt(b"Hello, World!")
print(f"Cipher text: {cipher_text.decode()}")

plain_text = cipher_suite.decrypt(cipher_text)
print(f"Plain text: {plain_text.decode()}")
