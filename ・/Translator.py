#問題文

import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.number import bytes_to_long


def encrypt(plaintext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pad(plaintext.encode(), 16))

flag = os.environ.get("FLAG", "CTF{dummy_flag}")
flag_bin = f"{bytes_to_long(flag.encode()):b}"
trans_0 = input("translations for 0> ")
trans_1 = input("translations for 1> ")
flag_translated = flag_bin.translate(str.maketrans({"0": trans_0, "1": trans_1}))
key = os.urandom(16)
print("ct:", encrypt(flag_translated, key).hex())

#ソルバ
import os
from pwn import *
from Crypto.Util.number import long_to_bytes

sc = remote("01-translator.challenges.beginners.seccon.jp", 9999)
sc.recvuntil(b"> ")
sc.sendline(b"a"*16)
sc.recvuntil(b"> ")
sc.sendline(b"b"*16)
sc.recvuntil(b": ")
ct = bytes.fromhex(sc.recvline().decode())
binary = ""
for i in range(0, len(ct)-16, 16):
    if ct[:16] == ct[i:i+16]:
        binary += "1"
    else:
        binary += "0"
print(long_to_bytes(int(binary, 2)))
