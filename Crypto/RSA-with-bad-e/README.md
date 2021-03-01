### RSA With Bad e

This tool is the result of reading **[this](https://eprint.iacr.org/2020/1059.pdf)** paper by Daniel Shumow

Specifically, it refers to RSA with an encryption exponent such that e|p-1 or e|q-1 and e is small.

It works on the principal that having a small e value will yield a set of e possible plaintexts.

```
usage: rsa-with-bad-e.py [-h] [-c C] [-p P] [-q Q] [-n N] [-e E] [-v V] [-o O]

RSA With Bad e

Required Arguments:
  -c C  Specify the ciphertext. Format: Int or Hex
  -e E  Specify the encryption exponent. Format: Int or Hex

Optional Arguments:
  -p P  Specify the first prime *NOTE: Either both p and q or n must be given*
        Format: Int or Hex
  -q Q  Specify the second prime *NOTE: Either both p and q or n must be
        given* Format: Int or Hex
  -n N  Specify the modulus *NOTE: Either both p and q or n must be given*
        Format: Int or Hex
  -v V  Verbose mode. Format: 0=  False, 1 = True
  -o O  Output mode. Format: 0 (default) = Hex, 1 = Int
```