def ksa(key_bytes):
    s = list(range(256))
    j = 0
    key_len = len(key_bytes)
    for i in range(256):
        j = (j + s[i] + key_bytes[i % key_len]) % 256
        s[i], s[j] = s[j], s[i]
    return s
def prga(s):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + s[i]) % 256
        s[i], s[j] = s[j], s[i]
        k = s[(s[i] + s[j]) % 256]
        yield k
def rc4_crypt(data_bytes, key_text):
    key_bytes = key_text.encode("utf-8")
    if not key_bytes:
        raise ValueError("Key cannot be empty.")
    s = ksa(key_bytes)
    keystream = prga(s)
    return bytes(b ^ next(keystream) for b in data_bytes)
def encrypt_rc4(plain_text, key_text):
    cipher_bytes = rc4_crypt(plain_text.encode("utf-8"), key_text)
    return cipher_bytes.hex()

def decrypt_rc4(cipher_hex, key_text):
    cipher_bytes = bytes.fromhex(cipher_hex)
    plain_bytes = rc4_crypt(cipher_bytes, key_text)
    return plain_bytes.decode("utf-8", errors="replace")
if __name__ == "__main__":
    print("RC4 Cipher")
    print("1) Encrypt")
    choice = input("Choose (1) ").strip()
    key = input("Enter key: ")
    if choice == "1":
        message = input("Enter plaintext: ")
        cipher_hex = encrypt_rc4(message, key)
        print("Cipher (hex):", cipher_hex)
        recovered = decrypt_rc4(cipher_hex, key)
        print("Decrypted back:", recovered)
    elif choice == "2":
        cipher_hex = input("Enter cipher (hex): ").strip()
        try:
            message = decrypt_rc4(cipher_hex, key)
            print("Plaintext:", message)
        except ValueError:
            print("Invalid hex input.")
    else:
        print("Invalid choice.")