#問題文
import os
import secrets
from fastecdsa.curve import secp256k1
from fastecdsa.point import Point

flag = os.environ.get("FLAG", "CTF{dummy_flag}")
y = secrets.randbelow(secp256k1.p)
print(f"{y = }")
x = int(input("x = "))
if not secp256k1.is_point_on_curve((x, y)):
    print("// Not on curve!")
    exit(1)
a = int(input("a = "))
P = Point(x, y, secp256k1)
Q = a * P
if a < 0:
    print("// a must be non-negative!")
    exit(1)
if P.x != Q.x:
    print("// x-coordinates do not match!")
    exit(1)
if P.y == Q.y:
    print("// P and Q are the same point!")
    exit(1)
print("flag =", flag)

#ソルバ

import os
from pwn import *
from sympy.ntheory.residue_ntheory import nthroot_mod
from fastecdsa.curve import secp256k1
from fastecdsa.point import Point

while True:
    with remote("elliptic4b.challenges.beginners.seccon.jp", 9999) as sc:
        sc.recvuntil(b"y = ")
        y = int(sc.recvline())
        x = nthroot_mod(y**2 - 7, 3, secp256k1.p)
        if x is None:
            continue
        sc.recvuntil(b"x = ")
        sc.sendline(str(x).encode())
        sc.recvuntil(b"a = ")
        a = secp256k1.q - 1
        sc.sendline(str(a).encode())
        print(sc.recvline())
        break
