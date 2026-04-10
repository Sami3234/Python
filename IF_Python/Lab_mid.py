import hmac
import hashlib

def transform_text(text):
    return text.encode("utf-8")
def calculate_hmac_md5(message, key):
    message_bytes = transform_text(message)
    key_bytes = transform_text(key)
    return hmac.new(key_bytes, message_bytes, hashlib.md5).hexdigest()
message = input("Enter message: ")
key = input("Enter key: ")
print("HMAC-MD5:", calculate_hmac_md5(message, key))