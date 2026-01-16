# grammar.py
import math

# Bornes des classes de g = delta / log(p)
# Ici on choisit des seuils simples, à ajuster si besoin.
# a : très serré, b : serré, c : typique, d : large
def classify_gap(g):
    if g < 0.5:
        return "a"
    elif g < 1.0:
        return "b"
    elif g < 1.8:
        return "c"
    else:
        return "d"

def typical_g_for_symbol(sym):
    if sym == "a":
        return 0.3
    elif sym == "b":
        return 0.75
    elif sym == "c":
        return 1.2
    else:
        return 2.0

