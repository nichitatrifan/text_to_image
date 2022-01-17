'''Number Generation'''

import Crypto.Util.number
import Crypto.Random.random

def generate_prime_number(bits):
    return Crypto.Util.number.getPrime(bits)

def generate_random_number(bits):
    return Crypto.Random.random.getrandbits(bits)

N_SIZE = 16

def main():
    sz = 1000
    p = generate_prime_number(sz)
    n = generate_random_number(sz)

    print("P: {} ({})".format(p,type(p)))
    print("N: {} ({})".format(n,type(n)))

if __name__ == '__main__':
    main()
