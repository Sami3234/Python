key = 'abcdefghijklmnopqrstuvwxyz'


def gcd(a, b):

    while b != 0:
        a, b = b, a % b

    return a



def dec_multi(k_inv, text):

    result = ''

    for l in text.lower():

        try:

            c = key.index(l)

            p = (c * k_inv) % 26

            result = result + key[p]

        except ValueError:

            result = result + l

    return result



text = input("Enter cipher text: ")

k_inv = int(input("Enter inverse key: "))


# check key valid or not
if gcd(k_inv, 26) != 1:
    print("Key is wrong")
else:
    plain = dec_multi(k_inv, text)
    print("Plain text:", plain)