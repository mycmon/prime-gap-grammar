# granville.py
import math
from filters import is_allowed_mod30

def granville_probability(n):
    if n < 3:
        return 0.0
    if not is_allowed_mod30(n):
        return 0.0
    return 1.2 / math.log(n)

