import pyotp
import os
import time

print("This is a simple implemtation for time based one time passwords (TOTP)")

print("Generating random key for OTP")
key = pyotp.random_base32() 
print("key: {}".format(key))

print("Building provisioning uri")
uri = pyotp.totp.TOTP(key).provisioning_uri("kmille", issuer_name="secret app")
print("Uri: {}".format(uri))
os.system("qr {}".format(uri))

otp = pyotp.totp.TOTP(key)
while 1:
    print("OTP: {}".format(otp.now()))
    time.sleep(2)

