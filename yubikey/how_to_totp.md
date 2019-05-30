# Use Yubikey for TOPT (time based one time password)
```
kmille@linbox tmp% ykman oath add test123
Enter a secret key (base32): H7TTOPOIDLOXGT4E

kmille@linbox tmp% ykman oath list       
test123

kmille@linbox tmp% ykman oath code
test123  446319

kmille@linbox tmp% ykman oath delete test123
Delete credential: test123 ? [y/N]: y
Deleted test123.

kmille@linbox yubikey master % pacman -Qo /usr/bin/yubioath-desktop
/usr/bin/yubioath-desktop is owned by yubico-yubioath-desktop 4.3.5-1

```
