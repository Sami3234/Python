letters = 'abcdefghijklmnopqrstuvwxyz'

text = input("Enter plaintext: ").lower()
key = int(input("Enter key: "))

cipher = ''
for l in text:
    if l.isalpha():
        n = letters.index(l) + 1   
        n = n * key                
        while n > 26:                
            n -= 26
        cipher += letters[n - 1]    
    else:
        cipher += l   

print("Cipher text:", cipher)