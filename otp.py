#!/usr/bin/env python3
import sys
import os
import os.path
import time

from tokenizer import decrypt_token
import pyotp

if len(sys.argv) != 2:
    here = os.path.dirname(os.path.realpath(__file__))
    base_dir = os.path.join(here, "data")
    ctx = " | ".join(os.listdir(base_dir))
    print("need contetxt: {}".format(ctx))
    exit()

key = decrypt_token(sys.argv[1])
otp = pyotp.totp.TOTP(key)
while 1:
    print(otp.now())
    time.sleep(2)


