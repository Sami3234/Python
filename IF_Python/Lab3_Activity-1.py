key = 'abcdefghijklmnopqrstuvwxyz' 
def enc_substitution(n, plaintext): 
    result = '' 
    for l in plaintext.lower(): 
        try: 
            i = (key.index(l) + n) % 26
            result += key[i] 
        except ValueError: 
            result += l 
    return result 
def dec_substitution(n, ciphertext): 
    result = '' 
    for l in ciphertext: 
        try: 
            i = (key.index(l) - n) % 26 
            result += key[i] 
        except ValueError: 
            result += l 
    return result 
origtext = 'Muhammad Sami Ullah' 
ciphertext = enc_substitution(13, origtext) 
plaintext = dec_substitution(13, ciphertext) 
print("Original Text:", origtext) 
print("Ciphertext:", ciphertext) 
print("Decrypted Text:", plaintext) 