import random
import sys
import hashlib
import math
from math import gcd

# Rabin-Miller primality test
def rabinMiller(num):
    s = num - 1
    t = 0
    while s % 2 == 0:
        s //= 2
        t += 1
    for trials in range(5):
        a = random.randrange(2, num - 1)
        v = pow(a, s, num)
        if v != 1:
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False
                i += 1
                v = (v ** 2) % num
    return True

def isPrime(num):
    if num < 2:
        return False
    lowPrimes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,
                 53,59,61,67,71,73,79,83,89,97,101,103,107,
                 109,113,127,131,137,139,149,151,157,163,167,
                 173,179,181,191,193,197,199,211,223,227,229,
                 233,239,241,251,257,263,269,271,277,281,283,
                 293,307,311,313,317,331,337,347,349,353,359,
                 367,373,379,383,389,397,401,409,419,421,431,
                 433,439,443,449,457,461,463,467,479,487,491,
                 499,503,509,521,523,541,547,557,563,569,571,
                 577,587,593,599,601,607,613,617,619,631,641,
                 643,647,653,659,661,673,677,683,691,701,709,
                 719,727,733,739,743,751,757,761,769,773,787,
                 797,809,811,821,823,827,829,839,853,857,859,
                 863,877,881,883,887,907,911,919,929,937,941,
                 947,953,967,971,977,983,991,997]
    if num in lowPrimes:
        return True
    for prime in lowPrimes:
        if num % prime == 0:
            return False
    return rabinMiller(num)

def generateLargePrime(keysize):
    while True:
        num = random.randrange(2**(keysize-1), 2**keysize)
        if isPrime(num):
            return num

def squareAndMultiply(x, c, n):
    z = 1
    c = "{0:b}".format(c)[::-1]
    l = len(c)
    for i in range(l-1, -1, -1):
        z = pow(z, 2) % n
        if c[i] == '1':
            z = (z * x) % n
    return z

def computeInverse(in1, in2):
    a, b = in1, in2
    s, old_s = 0, 1
    t, old_t = 1, 0
    while b != 0:
        q = a // b
        a, b = b, a - q * b
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    return old_s % in2

def shaHash(fileName):
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    with open(fileName, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    return int("0x" + hasher.hexdigest(), 0)

# Key Generation
def keyGeneration():
    print("Computing key values, please wait...")
    loop = True
    while loop:
        k = random.randrange(2**415, 2**416)
        q = generateLargePrime(160)
        p = (k * q) + 1
        while not isPrime(p):
            k = random.randrange(2**415, 2**416)
            q = generateLargePrime(160)
            p = (k * q) + 1
        L = p.bit_length()
        t = random.randint(1, p-1)
        g = squareAndMultiply(t, (p-1)//q, p)
        if L >= 512 and L <= 1024 and L % 64 == 0 and squareAndMultiply(g, q, p) == 1:
            loop = False
            a = random.randint(2, q-1)
            h = squareAndMultiply(g, a, p)
            with open("key.txt", "w") as f1:
                f1.write(f"{p}\n{q}\n{g}\n{h}")
            with open("secretkey.txt", "w") as f2:
                f2.write(str(a))
            print("Verification key stored at key.txt and secret key stored at secretkey.txt")

# Signing
def sign():
    if len(sys.argv) < 2:
        print("Format: python sign.py filename")
    else:
        print("Signing the file...")
        fileName = sys.argv[1]
        with open("key.txt", "r") as f1, open("secretkey.txt", "r") as f2:
            p = int(f1.readline().strip())
            q = int(f1.readline().strip())
            g = int(f1.readline().strip())
            h = int(f1.readline().strip())
            a = int(f2.readline().strip())
        loop = True
        while loop:
            r = random.randint(1, q-1)
            c1 = squareAndMultiply(g, r, p) % q
            c2 = (shaHash(fileName) + (a * c1)) % q
            Rinverse = computeInverse(r, q)
            c2 = (c2 * Rinverse) % q
            if c1 != 0 and c2 != 0:
                loop = False
        with open("signature.txt", "w") as f:
            f.write(f"{c1}\n{c2}")
        print("Signature stored at signature.txt")

# Verification
def verification():
    if len(sys.argv) < 2:
        print("Format: python verify.py filename")
    else:
        print("Checking the signature...")
        fileName = sys.argv[1]
        with open("key.txt", "r") as f1, open("signature.txt", "r") as f2:
            p = int(f1.readline().strip())
            q = int(f1.readline().strip())
            g = int(f1.readline().strip())
            h = int(f1.readline().strip())
            c1 = int(f2.readline().strip())
            c2 = int(f2.readline().strip())
        t1 = (shaHash(fileName) * computeInverse(c2, q)) % q
        t2 = (c1 * computeInverse(c2, q)) % q
        valid1 = squareAndMultiply(g, t1, p)
        valid2 = squareAndMultiply(h, t2, p)
        valid = ((valid1 * valid2) % p) % q
        if valid == c1:
            print("Valid signature")
        else:
            print("Invalid signature")
