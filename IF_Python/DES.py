from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

def encrypt(plaintext, key):
    key_bytes = key.encode('utf-8')
    plain_bytes = plaintext.encode('utf-8')

    cipher = DES.new(key_bytes, DES.MODE_ECB)
    padded_text = pad(plain_bytes, DES.block_size)

    encrypted_text = cipher.encrypt(padded_text)
    return encrypted_text

def decrypt(ciphertext, key):
    key_bytes = key.encode('utf-8')

    cipher = DES.new(key_bytes, DES.MODE_ECB)
    decrypted_padded_text = cipher.decrypt(ciphertext)

    decrypted_text = unpad(decrypted_padded_text, DES.block_size)
    return decrypted_text.decode('utf-8')

if __name__ == "__main__":
    plaintext = "FA24-BSE-080"
    Key = "comsats7"
    encrypted = encrypt(plaintext, Key)
    print("Encrypted:", encrypted)

    decrypted = decrypt(encrypted, Key)
    print("Decrypted:", decrypted)