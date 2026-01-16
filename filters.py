# filters.py
ALLOWED_MOD30 = {1, 7, 11, 13, 17, 19, 23, 29}
SMALL_PRIMES = [7, 11, 13, 17, 19, 23, 29]

def is_allowed_mod30(n):
    return n % 30 in ALLOWED_MOD30

def passes_small_prime_filter(n):
    for p in SMALL_PRIMES:
        if n % p == 0:
            return False
    return True

