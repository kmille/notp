import pyotp
import os
import time

key = pyotp.random_base32() 
print("key: {}".format(key))
uri = pyotp.totp.TOTP(key).provisioning_uri("kmille", issuer_name="secret app")
print(uri)
os.system("qr {}".format(uri))

otp = pyotp.totp.TOTP(key)
while 1:
    print(otp.now())
    time.sleep(2)

