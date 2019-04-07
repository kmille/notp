1. Get token
2. python tokenizer.py encrypt test123
    -> enter OTP key
    -> enter a password to encrypt 
3. encrpyted data is in data/test123 (nonce\ncipher in hex)
4. python otp.py test123
    -> enter password to decrypt
    -> current otp is shown
