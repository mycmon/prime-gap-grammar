# Prime Gap Grammar — Empirical Markov Model

This project explores an empirical structure observed in normalized prime gaps.
It is not a theory and does not attempt to predict primes.
It is an exploratory computational study based on:

- normalization of prime gaps by log(p)
- symbolic discretization into a grammar (a, b, c, d)
- Markov transition matrices
- arithmetic filters (mod 30, small primes)
- numerical simulation and comparison with Granville's model

## Features

- Interactive Python simulator (Tkinter)
- Normalized gap grammar
- Markov model (order 1)
- Mod 30 filter
- Anti-multiples filter (7, 11, 13, 17, 19, 23, 29)
- Real-time success rate graph
- Comparison with Granville's probability
- CSV export

## Installation

```bash
pip install sympy matplotlib

## Running the simulator

python main.py

## Reproducing results

Typical results on the interval 1–2 million:

~41% simulated primes

real density: ~7.24%

performance: ~4.1× random

Granville prediction: ~7%


## Document
The folder paper/ contains a short explanatory document (LaTeX + PDF).

## Purpose
This project is exploratory.
It presents an empirical structure observed in prime gaps and shares it with the mathematical community for discussion and further investigation.



