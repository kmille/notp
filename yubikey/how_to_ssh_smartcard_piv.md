# Use case
- use the Yubikey for ssh authentication
- the private key will never leave the yubikey
- use the Yubikey as Smartcard (PIV)
- this is very verbose 
- tested with the Yubikey NEO and Arch Linux


# Generate private key on Yubikey
```
kmille@linbox tmp% pacman -Qo /usr/lib64/pkcs11/opensc-pkcs11.so                                                       
/usr/lib/pkcs11/opensc-pkcs11.so is owned by opensc 0.19.0-2
kmille@linbox tmp% pacman -Qo /usr/bin/yubico-piv-tool          
/usr/bin/yubico-piv-tool is owned by yubico-piv-tool 1.6.2-2
kmille@linbox tmp% pacman -Qo /usr/bin/ykman
/usr/bin/ykman is owned by yubikey-manager 2.1.0-1


kmille@linbox projects% ykman mode              
Current connection mode is: OTP+CCID
Supported USB interfaces are: OTP, FIDO, CCID

kmille@linbox projects% yubico-piv-tool -a status
CHUID:  3019d4e739da739ced39ce739d836858210842108421c84210c3eb341028df6bd1b33af16ec792a5098a14e12e350832303330303130313e00fe00
CCC:    No data available
Slot 9a:
        Algorithm:      RSA2048
        Subject DN:     CN=SSH key
        Issuer DN:      CN=SSH key
        Fingerprint:    da3f587b069450da8317fa61f68692824d423e5a4ba1c9f81e289d34ba98a171
        Not Before:     May 11 14:00:41 2019 GMT
        Not After:      May 10 14:00:41 2020 GMT
PIN tries left: 3

Delete the existing key:
kmille@linbox projects% yubico-piv-tool -a delete-certificate -s 9a

kmille@linbox projects% yubico-piv-tool -a status                  
CHUID:  3019d4e739da739ced39ce739d836858210842108421c84210c3eb341028df6bd1b33af16ec792a5098a14e12e350832303330303130313e00fe00
CCC:    No data available
PIN tries left: 3


Generate a new private key (2048 bit, take some tome)
kmille@linbox tmp% yubico-piv-tool -a generate -s 9a -o public.pem
Successfully generated a new private key.

kmille@linbox tmp% cat public.pem 
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAgcgEqn6mv9FL5eshYtuF
LRq7/Jo/4R2pqiwbUjvDyb6P6E+eH900ITcrwPfOWeW3+6yBINr72OsEfk0dstIo
cJT+FKc2+SIJXWn3cZNmuHezIc6hrUincWNybNLAM712cBpxe1bk9M9nluaV8C+T
mNEkxIqaG09RhcEu0kiWyf+5hAp11jgvsfVMEwRJl3Zl7fkuYX5a5TBGnS/qyTR9
wm3ijbbn8bYtCKd1Ry3z/DIS3Lyvdr4IbkBe5X8hTrgdSjlNtwBff+Pm/VbB0+Jp
PD1263RdGbBYRlAy8RW1/IWflw1cLF5om9a7UVjbegQfElA/SPS5gWeKdYgy9VEV
AQIDAQAB
-----END PUBLIC KEY-----

kmille@linbox tmp% cat public.pem| openssl asn1parse 
    0:d=0  hl=4 l= 290 cons: SEQUENCE          
    4:d=1  hl=2 l=  13 cons: SEQUENCE          
    6:d=2  hl=2 l=   9 prim: OBJECT            :rsaEncryption
   17:d=2  hl=2 l=   0 prim: NULL              
   19:d=1  hl=4 l= 271 prim: BIT STRING        


kmille@linbox tmp% yubico-piv-tool -a verify-pin -a selfsign-certificate -s 9a -S "/CN=SSH key/" -i public.pem -o cert.pem

Enter PIN: 
Successfully verified PIN.
Successfully generated a new self signed certificate.

kmille@linbox tmp% file cert.pem 
cert.pem: PEM certificate

kmille@linbox tmp% cat cert.pem     
-----BEGIN CERTIFICATE-----
MIICpTCCAY2gAwIBAgIJAMCoFE2joC+9MA0GCSqGSIb3DQEBCwUAMBIxEDAOBgNV
BAMMB1NTSCBrZXkwHhcNMTkwNTE3MTAzNTM3WhcNMjAwNTE2MTAzNTM3WjASMRAw
DgYDVQQDDAdTU0gga2V5MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA
gcgEqn6mv9FL5eshYtuFLRq7/Jo/4R2pqiwbUjvDyb6P6E+eH900ITcrwPfOWeW3
+6yBINr72OsEfk0dstIocJT+FKc2+SIJXWn3cZNmuHezIc6hrUincWNybNLAM712
cBpxe1bk9M9nluaV8C+TmNEkxIqaG09RhcEu0kiWyf+5hAp11jgvsfVMEwRJl3Zl
7fkuYX5a5TBGnS/qyTR9wm3ijbbn8bYtCKd1Ry3z/DIS3Lyvdr4IbkBe5X8hTrgd
SjlNtwBff+Pm/VbB0+JpPD1263RdGbBYRlAy8RW1/IWflw1cLF5om9a7UVjbegQf
ElA/SPS5gWeKdYgy9VEVAQIDAQABMA0GCSqGSIb3DQEBCwUAA4IBAQAfGL6Yt9W+
4T+kAxnVwNGdBO863bkg+YjsghGox117KXJvBG4wY8vupKdm1ubVHbdmrJiSXuFF
FPlfOrOT0s2c9GTpxBA7B3iO/X+aS/rQ5af39GXMdY5BO8N8PJ3DTO81L3Vhrakk
SCfeejocT/C9p09LP9a4bdp2zcdXruOKkoIeSIn/qUq/nD8uafQnWmq+7u8vP6GC
COW8eY+hVO65A+rndUpvRqWGVT6BVHkm3UJP3cR/ot86XCbt1pzBarSl6Y+Y+7l0
6nu2ERiy9Gteq1atp/IhxVdyimN+++c6tGsCTIZcEncJ+ftYzDGx6fy2hDUk2NI6
mFUNyByWkdes
-----END CERTIFICATE-----

kmille@linbox tmp% openssl x509 -in cert.pem -noout -dates -subject
notBefore=May 17 10:35:37 2019 GMT
notAfter=May 16 10:35:37 2020 GMT
subject=CN = SSH key

kmille@linbox tmp% yubico-piv-tool -a status                              
CHUID:  3019d4e739da739ced39ce739d836858210842108421c84210c3eb341028df6bd1b33af16ec792a5098a14e12e350832303330303130313e00fe00
CCC:    No data available
Slot 9a:
        Algorithm:      RSA2048
        Subject DN:     CN=SSH key
        Issuer DN:      CN=SSH key
        Fingerprint:    475b3dfa6a871eb0d5bfe33b801f66d18a18da6741a15b7ac3fe8747c82313b3
        Not Before:     May 17 10:35:37 2019 GMT
        Not After:      May 16 10:35:37 2020 GMT
PIN tries left: 3


kmille@linbox tmp% ssh-keygen -i -m PKCS8 -f public.pem | tee public.pub 
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCByASqfqa/0Uvl6yFi24UtGrv8mj/hHamqLBtSO8PJvo/oT54f3TQhNyvA985Z5bf7rIEg2vvY6wR+TR2y0ihwlP4Upzb5Igldafdxk2a4d7MhzqGtSKdxY3Js0sAzvXZwGnF7VuT0z2eW5pXwL5OY0STEipobT1GFwS7SSJbJ/7mECnXWOC+x9UwTBEmXdmXt+S5hflrlMEadL+rJNH3CbeKNtufxti0Ip3VHLfP8MhLcvK92vghuQF7lfyFOuB1KOU23AF9/4+b9VsHT4mk8PXbrdF0ZsFhGUDLxFbX8hZ+XDVwsXmib1rtRWNt6BB8SUD9I9LmBZ4p1iDL1URUB

kmille@linbox tmp% cat public.pub >> ~/.ssh/authorized_keys 


kmille@linbox tmp% ssh localhost                                                                          
kmille@localhost: Permission denied (publickey).

kmille@linbox tmp% ssh -I /usr/lib64/pkcs11/opensc-pkcs11.so localhost
Enter PIN for 'SSH key':
# should now work from here

For convenience: Append 'PKCS11Provider /usr/lib64/pkcs11/opensc-pkcs11.so' to /etc/ssh/ssh_config (or ~/.ssh/config for a dedicated host)
kmille@linbox tmp% ssh localhost          
Enter PIN for 'SSH key':

Add Yubikey private key to ssh-agent. If this does not work kill the running agent.
kmille@linbox tmp%  ssh-add -s /usr/lib64/pkcs11/opensc-pkcs11.so
Enter passphrase for PKCS#11: 
Card added: /usr/lib64/pkcs11/opensc-pkcs11.so

kmille@linbox tmp% ssh-add -l
2048 SHA256:RFE2X8BFTufN2C66eeaBMp0K0q4dRkjWvUEb+sAEtoI /usr/lib/opensc-pkcs11.so (RSA)                                               

kmille@linbox tmp% ssh localhost
Last login: Fri May 17 12:51:53 2019 from ::1

Bug for me: If you remove the the yubike and put it back in I can't use it with the agent
kmille@linbox tmp% ssh localhost     
sign_and_send_pubkey: signing failed: agent refused operation
kmille@localhost: Permission denied (publickey).
kmille@linbox tmp%  ssh-add -s /usr/lib64/pkcs11/opensc-pkcs11.so
Enter passphrase for PKCS#11: 
Could not add card "/usr/lib64/pkcs11/opensc-pkcs11.so": agent refused operation
```

# Use an existing ssh key
```
kmille@linbox tmp% pacman -Qo /usr/bin/puttygen
/usr/bin/puttygen is owned by putty 0.71-1

1. Assumption you already have an encrpyted ssh key
kmille@linbox tmp% ssh-keygen -f thisismyexistingkey 
Generating public/private rsa key pair.
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in thisismyexistingkey.
Your public key has been saved in thisismyexistingkey.pub.
The key fingerprint is:
SHA256:eQRs4QqgjuONB2vqm4QsXyco5GerLUpHt4YzU54X6wM kmille@linbox

kmille@linbox tmp% cat thisismyexistingkey
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAACmFlczI1Ni1jdHIAAAAGYmNyeXB0AAAAGAAAABC3tvEmWS
r0eYzkeiHkz5k+AAAAEAAAAAEAAAEXAAAAB3NzaC1yc2EAAAADAQABAAABAQCRl0GlMhu0
Pm/rQ5ihh8cLq1ukbNnTn6J7aw+G7KNK5uwNEDNomeNEiVo84HJ5nbnb6C36U69nw6wifF
glNMkRE+uHdFmDoS4U5b/ANH7M4v6RuoZQIlpjXA7iS4nQDP8Ts61ZngA9OM1F3tkFbSti
oILcy1gYVrgNfaGmvOc+tnq9m4rC9/ET1DM3aNeG94Fu+6Btq4VfP4Hijgb8FAvSP0/jq0
0tu+lp9GG9rFGlnAqooDP9A+AG77a6x8tUQ2LBFO+TFNNWr+l6vxEPk45IbJVoVYCA9+xF
WC9UfmHCZ3/QNI62GOj40ZeykhOwbpw7ibHveZD97P6A4PmqQPdVAAAD0AVOtypn0Ks3Hh
2e6tK3OAPPHJrZ6xjpR10feFvNUyGCisMP8cCLsPXwGpoHFVVF8v6HbV1AcbMnXEm6SdeU
uCyD401Yhvd4vof2CBKZ8RAhkc/jTZ8vNfSJ41HJjYXjXUDsNSEwIrIUBHOYzrRtIdGCTL
hu0TRa7Oihqfg38DPR1xArAs6QC6eP8Vgs/1jMXmSWEpcRo6X1jxPwX4h2uc9xFWfbXO+A
ySaGYFyk1rMCOQRCgsrwgmOhDupyeJdX7XULIblsJaFSKZ4M9y7basNWLVTEE6N81p6PXs
c/ULag8tgiNu0qHeHEo0n+gYq0P0DsNMUUV8x0osD+OAhy//NumsPkm6aPnac0+KYC9RgM
kstxdM9k7DqaSfvLYImwXvD4G14jByOZU2+y2MzhVZ1NKA4/HI+ngP0VqYp+2cI1gKW6qi
qXNu7mJGoLWEHEvyFjLeKs13AFPWVIY6HH4HyPX7gj2rqT6PQS/qNjw6vUtEMvr7QmYQlW
koT7GRkgOjoucxoXjXtEvvV4lIC4HShrvMdrv/n0YHjfFVjQSwGZkxWBcHG5AB6wwejAB3
hjzAyljB6JmSCO/CDfgeby8sUPTyj7RNKV178XxTkXoucfklJBUZrQWFTzn/xRf7FzSAgL
Mp1XE9ig0dMdyZRfLFbZI3U4MXOZRxEoDJGruejoN7ZvMXf8eKgkf4oyYYzSsq88w6k2tF
tgaeNW/OMQ9u3LacbdmmIYh4QI5ojn9CnldfKBXXugYUSTL1xn2U01nA8QPI4R1A2FcOwo
a2QUXGeSQKFbF5ePhl6JyfDaeD6Z8QE1HQO4JdWS+laM1GRxt9r1O+cQxfl1V3gTanb5Lv
MTtLnbwBtpMkmr2M8l/RrBQUSKiFWAg8ACp7IjGUC2fXwtGHeVOoD6EBVnzfr871EciL2u
8ZLUM79KZWz7Bfg/szuHMpD9Bt7U7QJPZPyqzzdIIUBSKFZE9KAewVJdbAeegJMzonBapx
vEEYVmtFIPMCvU79AEdFmMApzKDPUGk1kJ94LL+BAKd45puEbPf8FJ0RHEU8llgn6I9o0P
AvW7TdwybgeSq23D4hx+8UoviYbZLwImoUh5FH2uLq6dWYCDYH123nf/16PUs4FJYIW2bB
4yPNGsIg4IdJiQmdvsw3kPIChzJUFa5BcaKfZRFHjbF/gOyz6Bbbvcg3MvehGl0UTNmSJD
7EvES/EhYWjZF+/+6OR7ieVgQb1TCYx9YYsYsbD+6qZ9hegkTkei3dY84YOMY4NsH+MvI+
2AJ2uPTrsr+NHqNxhJM6v4aHu0uu0=
-----END OPENSSH PRIVATE KEY-----


2. Remove password from private key
kmille@linbox tmp% ssh-keygen -f thisismyexistingkey -p
Enter old passphrase: 
Key has comment 'kmille@linbox'
Enter new passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved with the new passphrase.

kmille@linbox tmp% cat thisismyexistingkey
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABFwAAAAdzc2gtcn
NhAAAAAwEAAQAAAQEAkZdBpTIbtD5v60OYoYfHC6tbpGzZ05+ie2sPhuyjSubsDRAzaJnj
RIlaPOByeZ252+gt+lOvZ8OsInxYJTTJERPrh3RZg6EuFOW/wDR+zOL+kbqGUCJaY1wO4k
uJ0Az/E7OtWZ4APTjNRd7ZBW0rYqCC3MtYGFa4DX2hprznPrZ6vZuKwvfxE9QzN2jXhveB
bvugbauFXz+B4o4G/BQL0j9P46tNLbvpafRhvaxRpZwKqKAz/QPgBu+2usfLVENiwRTvkx
TTVq/per8RD5OOSGyVaFWAgPfsRVgvVH5hwmd/0DSOthjo+NGXspITsG6cO4mx73mQ/ez+
gOD5qkD3VQAAA8iIs5IniLOSJwAAAAdzc2gtcnNhAAABAQCRl0GlMhu0Pm/rQ5ihh8cLq1
ukbNnTn6J7aw+G7KNK5uwNEDNomeNEiVo84HJ5nbnb6C36U69nw6wifFglNMkRE+uHdFmD
oS4U5b/ANH7M4v6RuoZQIlpjXA7iS4nQDP8Ts61ZngA9OM1F3tkFbStioILcy1gYVrgNfa
GmvOc+tnq9m4rC9/ET1DM3aNeG94Fu+6Btq4VfP4Hijgb8FAvSP0/jq00tu+lp9GG9rFGl
nAqooDP9A+AG77a6x8tUQ2LBFO+TFNNWr+l6vxEPk45IbJVoVYCA9+xFWC9UfmHCZ3/QNI
62GOj40ZeykhOwbpw7ibHveZD97P6A4PmqQPdVAAAAAwEAAQAAAQBGbawk1KuQMtADOAzi
vwLrwzYuwTVSaRu5pl25gEmx1ymDXD3yMNc+9U7AujbGXCVnmtZ7DPaCNKbVe99MCE/nwg
Ii4YbX5SWcmFN9ECfyxzAsoNWOeD/PZt4QXEhLa64NAtMt0f/9nbe3QAkt1dSx/kGvu3Jf
O7wHUqnbNfCLZhILEprwDkelWf9IoaelCsqvMG1MaIIyTOEQWkS2unDZ/WZkmssy3WOK82
4eQR20O9u8jaiTveFJGN/DsV8oQij1aujtDy01Rib/j3Ina3SHsHi6oE3GPU+i0Y8NriJy
wuLxUoh10kSGt4nThNRrQQmp227OZp2x+WjUUjSKbkaBAAAAgQC3LdA0LUboYkdStIJ6/i
gFk3H1SgmSh4dRevtFFtOvomIPZ1f64myOlXZ+3/Sb8KwEAbbMx1yj1vt6cPMszP8ZzBre
d6nQA45ts3GVEevQLS0Jd3vMVPpyk4sF+omF0+KlNDFhoolLBOm1NZptcCpxxwLZm4tVDe
4HX0UV7+oAkgAAAIEAwgMpCzk9M+EmvXGd5EGpSEzgv2oY9XxLwAUoSGnFC6KCgkLg93lo
QLnTSRuxmEDYw7GOdgj863F2r6kqKl7gLe1dcK4bUniGxPsY64DrtXbx73chDoKAvcdvoM
E+r7X4ZHKXu9bK/nHWjkHRYSdaGEme37hVs3dde7xmrDrRauEAAACBAMAbjzRc7Yp7cZyL
Huc7weg0zkB6L9trzkU79/DWjHh5t9eVnwfKwRZZ4YmrGikI9Ea2Iq6j0KazgqE9OjgkAn
ufnDc6wxN7IG1xIn6/AOXZnl5O/r5g7DRo40TVNiZedvVIVM4WzC5lthjABOgvSoeF5d+5
4t6L34C3+CjiCW71AAAADWttaWxsZUBsaW5ib3gBAgMEBQ==
-----END OPENSSH PRIVATE KEY-----

3. I don't know why it has to be that complicated... but it works ...
kmille@linbox tmp% puttygen thisismyexistingkey -O private-sshcom -o thisismyexistingkey.ssh2

kmille@linbox tmp% cat thisismyexistingkey.ssh2 
---- BEGIN SSH2 ENCRYPTED PRIVATE KEY ----
Comment: "kmille@linbox"
P2/56wAAA+4AAAA3aWYtbW9kbntzaWdue3JzYS1wa2NzMS1zaGExfSxlbmNyeXB0e3JzYS
1wa2NzMXYyLW9hZXB9fQAAAARub25lAAADnwAAA5sAAAARAQABAAAH/0ZtrCTUq5Ay0AM4
DOK/AuvDNi7BNVJpG7mmXbmASbHXKYNcPfIw1z71TsC6NsZcJWea1nsM9oI0ptV730wIT+
fCAiLhhtflJZyYU30QJ/LHMCyg1Y54P89m3hBcSEtrrg0C0y3R//2dt7dACS3V1LH+Qa+7
cl87vAdSqds18ItmEgsSmvAOR6VZ/0ihp6UKyq8wbUxogjJM4RBaRLa6cNn9ZmSayzLdY4
rzbh5BHbQ727yNqJO94UkY38OxXyhCKPVq6O0PLTVGJv+PcidrdIeweLqgTcY9T6LRjw2u
InLC4vFSiHXSRIa3idOE1GtBCanbbs5mnbH5aNRSNIpuRoEAAAgAkZdBpTIbtD5v60OYoY
fHC6tbpGzZ05+ie2sPhuyjSubsDRAzaJnjRIlaPOByeZ252+gt+lOvZ8OsInxYJTTJERPr
h3RZg6EuFOW/wDR+zOL+kbqGUCJaY1wO4kuJ0Az/E7OtWZ4APTjNRd7ZBW0rYqCC3MtYGF
a4DX2hprznPrZ6vZuKwvfxE9QzN2jXhveBbvugbauFXz+B4o4G/BQL0j9P46tNLbvpafRh
vaxRpZwKqKAz/QPgBu+2usfLVENiwRTvkxTTVq/per8RD5OOSGyVaFWAgPfsRVgvVH5hwm
d/0DSOthjo+NGXspITsG6cO4mx73mQ/ez+gOD5qkD3VQAABAC3LdA0LUboYkdStIJ6/igF
k3H1SgmSh4dRevtFFtOvomIPZ1f64myOlXZ+3/Sb8KwEAbbMx1yj1vt6cPMszP8ZzBred6
nQA45ts3GVEevQLS0Jd3vMVPpyk4sF+omF0+KlNDFhoolLBOm1NZptcCpxxwLZm4tVDe4H
X0UV7+oAkgAABADAG480XO2Ke3Gcix7nO8HoNM5Aei/ba85FO/fw1ox4ebfXlZ8HysEWWe
GJqxopCPRGtiKuo9Cms4KhPTo4JAJ7n5w3OsMTeyBtcSJ+vwDl2Z5eTv6+YOw0aONE1TYm
Xnb1SFTOFswuZbYYwAToL0qHheXfueLei9+At/go4glu9QAABADCAykLOT0z4Sa9cZ3kQa
lITOC/ahj1fEvABShIacULooKCQuD3eWhAudNJG7GYQNjDsY52CPzrcXavqSoqXuAt7V1w
rhtSeIbE+xjrgOu1dvHvdyEOgoC9x2+gwT6vtfhkcpe71sr+cdaOQdFhJ1oYSZ7fuFWzd1
17vGasOtFq4Q==
---- END SSH2 ENCRYPTED PRIVATE KEY ----

Now get the private key in RSA format:

kmille@linbox tmp% ssh-keygen -f thisismyexistingkey.ssh2 -i | tee thisismyexistingkey.rsa
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAkZdBpTIbtD5v60OYoYfHC6tbpGzZ05+ie2sPhuyjSubsDRAz
aJnjRIlaPOByeZ252+gt+lOvZ8OsInxYJTTJERPrh3RZg6EuFOW/wDR+zOL+kbqG
UCJaY1wO4kuJ0Az/E7OtWZ4APTjNRd7ZBW0rYqCC3MtYGFa4DX2hprznPrZ6vZuK
wvfxE9QzN2jXhveBbvugbauFXz+B4o4G/BQL0j9P46tNLbvpafRhvaxRpZwKqKAz
/QPgBu+2usfLVENiwRTvkxTTVq/per8RD5OOSGyVaFWAgPfsRVgvVH5hwmd/0DSO
thjo+NGXspITsG6cO4mx73mQ/ez+gOD5qkD3VQIDAQABAoIBAEZtrCTUq5Ay0AM4
DOK/AuvDNi7BNVJpG7mmXbmASbHXKYNcPfIw1z71TsC6NsZcJWea1nsM9oI0ptV7
30wIT+fCAiLhhtflJZyYU30QJ/LHMCyg1Y54P89m3hBcSEtrrg0C0y3R//2dt7dA
CS3V1LH+Qa+7cl87vAdSqds18ItmEgsSmvAOR6VZ/0ihp6UKyq8wbUxogjJM4RBa
RLa6cNn9ZmSayzLdY4rzbh5BHbQ727yNqJO94UkY38OxXyhCKPVq6O0PLTVGJv+P
cidrdIeweLqgTcY9T6LRjw2uInLC4vFSiHXSRIa3idOE1GtBCanbbs5mnbH5aNRS
NIpuRoECgYEAwgMpCzk9M+EmvXGd5EGpSEzgv2oY9XxLwAUoSGnFC6KCgkLg93lo
QLnTSRuxmEDYw7GOdgj863F2r6kqKl7gLe1dcK4bUniGxPsY64DrtXbx73chDoKA
vcdvoME+r7X4ZHKXu9bK/nHWjkHRYSdaGEme37hVs3dde7xmrDrRauECgYEAwBuP
NFztintxnIse5zvB6DTOQHov22vORTv38NaMeHm315WfB8rBFlnhiasaKQj0RrYi
rqPQprOCoT06OCQCe5+cNzrDE3sgbXEifr8A5dmeXk7+vmDsNGjjRNU2Jl529UhU
zhbMLmW2GMAE6C9Kh4Xl37ni3ovfgLf4KOIJbvUCgYBphMaB8DO1T7N+PZkeWAf1
5rol4VKJ0Xxxh1yNZdlhppVMu4sXjdSBv4+Gp6VDpaE/bgaJdAH7G87tYxgny0oq
MHstmcQKarsBz3+SNp/8JiEXmLdF6PyUOzAfQnsRnerm1txnsT7efJOw82Mpb/m0
U/Ywv1T9MuKJNcKx0ZusgQKBgFmGPlUrnTM01bwbBRrDOVkKCrf3eQfrFGQlTyU4
Bpw6NNdNjZ/m99Z/qmAqkXVgC95MEJuMEbct3olfbBsvhMyxk+4U/0W70l/OIkIo
prV2lZvjekmkB09hNdAlACgfS5aAz6x+6UYR9itQiLjfGP9RAdAh4zzMuCpXEVmU
BMtlAoGBALct0DQtRuhiR1K0gnr+KAWTcfVKCZKHh1F6+0UW06+iYg9nV/ribI6V
dn7f9JvwrAQBtszHXKPW+3pw8yzM/xnMGt53qdADjm2zcZUR69AtLQl3e8xU+nKT
iwX6iYXT4qU0MWGiiUsE6bU1mm1wKnHHAtmbi1UN7gdfRRXv6gCS
-----END RSA PRIVATE KEY-----

kmille@linbox tmp% yubico-piv-tool -s 9a -a import-key  -K PEM -i thisismyexistingkey.rsa
Successfully imported a new private key.


kmille@linbox tmp% openssl rsa -in ovh.rsa -pubout | tee ovh.rsa.pub
writing RSA key
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAmzu84NTmCqiyyXskRBYr
tZcE+PlNGs7SEZacJejTB3sDFKKWFY7OlfpT5cjtSnuFB+/okOa8Bfy8lkppLt+Q
ZyKS8KyvuBHAEF9i9djKPn+dBibbe8eurckTacNY+td3rzpaSnxXSxf1OYtBwAff
Qg8Jw6KMxGC7IZQqsQWuP1xh8NUZcNbPZCc4clPu4nQzmnEPvjR1PIvyg2vNac+p
G3F4kD70YqF6l6+s4RG/aj3Q47uz+pH5g3OpMG3nfvT8xyM19YdrEEFtRYVithR9
poxMFbq/KPnmLZByCn0YJ8aMbpavGuRnvhT5qd27cktz8w/Bp+2+nwr0bUY/5Cgn
BwIDAQAB
-----END PUBLIC KEY-----


kmille@linbox tmp% yubico-piv-tool -a verify-pin -a selfsign-certificate -s 9a -S "/CN=SSH key/" -i ovh.rsa.pub -o cert.pem                                              
Enter PIN:
Successfully verified PIN.
Successfully generated a new self signed certificate.
kmille@linbox tmp% yubico-piv-tool -a import-certificate -s 9a -i cert.pem

kmille@linbox tmp% yubico-piv-tool -a status                              
CHUID:  3019d4e739da739ced39ce739d836858210842108421c84210c3eb341028df6bd1b33af16ec792a5098a14e12e350832303330303130313e00fe00
CCC:    No data available
Slot 9a:
        Algorithm:      RSA2048
        Subject DN:     CN=SSH key
        Issuer DN:      CN=SSH key
        Fingerprint:    d9e945b719c00cd547db0c1b1a58d23bcd1f9e0ffe162c3ad2992fc5f46ab350
        Not Before:     May 18 09:56:19 2019 GMT
        Not After:      May 17 09:56:19 2020 GMT
PIN tries left: 3

kmille@linbox tmp% ssh <ip>
Enter PIN for 'SSH key':
Linux yolo 4.19.0-2-amd64 #1 SMP Debian 4.19.16-1 (2019-01-17) x86_64
```

# Resources 
- https://access.redhat.com/articles/1523343
- https://www.freifunk-gera-greiz.de/wiki/-/wiki/Allgemein/SSH+mit+Yubikey+4+unter+Ubuntu/pop_up
- https://developers.yubico.com/PIV/Guides/SSH_with_PIV_and_PKCS11.html
- https://0day.work/using-a-yubikey-for-gpg-and-ssh/
- https://news.ycombinator.com/item?id=16145586
- https://wiki.archlinux.org/index.php/YubiKey
- https://github.com/drduh/YubiKey-Guide
