# markov.py
import random

# Matrice de transition Markov d'ordre 1 sur {a,b,c,d}
# Probabilités empiriques simplifiées (à ajuster si besoin).
TRANSITIONS = {
    "a": [("a", 0.2), ("b", 0.6), ("c", 0.2)],
    "b": [("a", 0.2), ("b", 0.3), ("c", 0.4), ("d", 0.1)],
    "c": [("b", 0.4), ("c", 0.3), ("d", 0.3)],
    "d": [("c", 0.6), ("d", 0.4)],
}

SYMBOLS = ["a", "b", "c", "d"]

def next_symbol(current):
    choices = TRANSITIONS.get(current, TRANSITIONS["b"])
    r = random.random()
    cum = 0.0
    for sym, prob in choices:
        cum += prob
        if r <= cum:
            return sym
    return choices[-1][0]

def initial_symbol():
    # Distribution initiale simple
    return random.choice(SYMBOLS)

