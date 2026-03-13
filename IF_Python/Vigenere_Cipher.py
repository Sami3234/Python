key = 'abcdefghijklmnopqrstuvwxyz'
def make_key(k):
    arr = []
    for l in k.lower():
        arr.append(key.index(l))
    return arr
def enc_vigenere(text, k):
    result = ''
    j = 0
    for l in text.lower():
        try:
            shift = k[j % len(k)]
            i = key.index(l)
            c = (i + shift) % 26
            result = result + key[c]
            j = j + 1
        except ValueError:
            result = result + l
    return result
text = input("Enter text: ")
k = input("Enter key: ")
k2 = make_key(k)
cipher = enc_vigenere(text, k2)
print("Cipher text:", cipher)