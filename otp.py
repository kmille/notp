#!/usr/bin/env python3
import sys
import time

from tokenizer import decrypt_token
import pyotp

if len(sys.argv) != 2:
    print("need contetxt")
    exit()

key = decrypt_token(sys.argv[1])
otp = pyotp.totp.TOTP(key)
while 1:
    print(otp.now())
    time.sleep(2)


