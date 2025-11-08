from sage.all import *
from Crypto.Util.number import long_to_bytes
import cuso
import ast

with open("output.txt", "r") as f:
    n = ast.literal_eval(f.readline().removeprefix("n = "))
    e = ast.literal_eval(f.readline().removeprefix("e = "))
    c = ast.literal_eval(f.readline().removeprefix("c = "))
    r = ast.literal_eval(f.readline().removeprefix("r = "))

a = next_prime(r) - r
for Q in Zmod(r)(n/a).nth_root(3, all=True):
    Q = int(Q)
    x, p = var("x, p")
    roots = cuso.find_small_roots(
        relations=[Q+x*r],
        bounds={x: (0, 2**61)},
        modulus_multiple=n,
        modulus_lower_bound=2**279,
        modulus_upper_bound=2**280
    )
    for root in roots:
        p = int(root[p])
        q = n // p
        print(long_to_bytes(pow(c, pow(e, -1, (p-1)*(q-1)), n)))
        break
