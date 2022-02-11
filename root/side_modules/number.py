'''Number Generation'''

import Crypto.Util.number
import Crypto.Random.random

def generate_prime_number(bits):
    return Crypto.Util.number.getPrime(bits)

def generate_random_number(bits):
    return Crypto.Random.random.getrandbits(bits)

def generate_public_key(n:int, h:int, a:int):
    return pow(n,a,h)

def decode_private_key(B:int, h:int, a:int): # B' = A^b (mod h)
    return pow(B,a,h)

N_SIZE = 16

def main():
    sz = 1000
    h = generate_prime_number(N_SIZE)
    n = generate_prime_number(N_SIZE)
    a = generate_prime_number(N_SIZE)
    A = generate_public_key(n, h, a)

    print("h (modula): {} ({})".format(h,type(h)))
    print("n (generator num): {} ({})".format(n,type(n)))
    print("a (private num): {} ({})".format(a,type(a)))
    print("A (public key): {} ({})".format(A,type(A)))

if __name__ == '__main__':
    main()
    
    #
    # sample input:
    # a = [37199, 56843, 48523]
    #
    # {
    # "n":[
    #     [48497,37951,57829]
    #     ],
    # "h":[
    #     [51043,35159,60353]
    #     ],
    # "A":[
    #     [14706,17085,24848]
    #     ]
    # }
    #
    # {"B": [[31852, 16866, 13534]]}
