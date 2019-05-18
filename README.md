# How to use TOTP with python

## 
```
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt

(venv) kmille@linbox notp master % python demo.py
This is a simple implemtation for time based one time passwords (TOTP)
Generating random key for OTP
key: 7A6J7WZJODMRL4CY
Building provisioning uri
Uri: otpauth://totp/secret%20app:kmille?secret=7A6J7WZJODMRL4CY&issuer=secret%20app
█████████████████████████████████████████
█████████████████████████████████████████
████ ▄▄▄▄▄ █▄▄█▄█▀ █▀█ █▄ ▀███ ▄▄▄▄▄ ████
████ █   █ █▄█ ▀▄█ ▀ ▄▀▄█▄ ▄▀█ █   █ ████
████ █▄▄▄█ █▀   ██ ▄ ▄▀▄█▄▄█ █ █▄▄▄█ ████
████▄▄▄▄▄▄▄█▄▀ █ █ █▄█ █ █▄█▄█▄▄▄▄▄▄▄████
████▄▀ ███▄▄▀▄▄  ██  █  ▀▀▄ ▀▀▀▄█▀▄█ ████
█████▀ ▄█▀▄▀▄▀▄██▄  ▄█▄▄▀█▄ ▀▄ ▄  ▄█▄████
████▄ █ ▀ ▄▀█ ▄█   █ ▄█▄ ▀ █ █ ▀█▀█▀▀████
████▄██ ▀▄▄ ▄▄▀█▄▀▀▀ █▄ ▀█▀ ▀▄▀███▄▀ ████
████▄▀▄█▀█▄  ▄▀█▄▄█▀█▀ ▀ █▀  ▄  ████▀████
████ ▄ ██▄▄▄█▄▄ █▄ ▄▄▄█ ▄█▀▄ ▀▄ ▄ ▄█▄████
█████▄▀█▄▄▄▀ █▀ ▀ █▄▄█ ▄ ▄▀ █▀  █ ▀█▀████
████▄▄█▀▄ ▄ ▀▀ ▀ ▄▀▄█▄▄ ▄█ ▄▀▀▀▀▄▀██ ████
████▄▄▄▄▄▄▄▄ ▄▄▀▀▀█▀▀██▀▀██▀ ▄▄▄ ██▄▀████
████ ▄▄▄▄▄ █▄▀█▄   ▄▄▄█ ██▀▀ █▄█ ▀▄▀▄████
████ █   █ ██▀▄█▀▀▄▄▀▄█▄ ▄▀  ▄▄  ██ ▀████
████ █▄▄▄█ █▄▄▀▄ ▄█ █▄  ▄▄▀▀▀ █▀▄▀█▄▄████
████▄▄▄▄▄▄▄█▄▄▄▄█▄█▄████▄██▄▄▄▄█▄▄██▄████
█████████████████████████████████████████
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
OTP: 356071
OTP: 356071
OTP: 356071
OTP: 356071
OTP: 356071
OTP: 356071
OTP: 356071
OTP: 356071
OTP: 356071
OTP: 356071
OTP: 356071
OTP: 340533
OTP: 340533
^CTraceback (most recent call last):
  File "demo.py", line 19, in <module>
      time.sleep(2)
      KeyboardInterrupt


```

# Use TOTP from command line 
- use the command line (e. g. from your server) as your second factor
- tokenizer.py will just en/decrypt your OTP secret
- you just need otp.py for generating OTPs

```
kmille@linbox notp master % python tokenizer.py 
encrypt or decrypt <context>

(venv) kmille@linbox notp master % python tokenizer.py encrypt demo123
OTP Token: HSBRGZRKZDRLBVEY
Password: 
data: 'HSBRGZRKZDRLBVEY'  nonce: 5145c86fcfcb7f8fa76eed7134f982e6   key: 9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08
Ciphertext: ce6e078d804b7934c42571f47e163414b7f12f9ee840a730c02adfed1e82a83e
Wrote encrpyted OTP Token to file
(venv) kmille@linbox notp master % cat data/demo123
5145c86fcfcb7f8fa76eed7134f982e6
ce6e078d804b7934c42571f47e163414b7f12f9ee840a730c02adfed1e82a83e%                                                                                                        (venv) kmille@linbox notp master % python tokenizer.py decrypt demo123
Password: 
< this will print the otp shared secret (HSBRGZRKZDRLBVEY) but it is commented out because the function is used in otp.py >
(venv) kmille@linbox notp master % 

(venv) kmille@linbox notp master % python otp.py
need contetxt: demo123 | .gitkeep
(venv) kmille@linbox notp master % python otp.py demo123
Password: 
958973
958973
958973
958973
958973
958973
958973
958973
958973
958973
056204
056204
```
