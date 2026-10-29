# Modular Arithmetic and RSA Cryptography

**Authors:** Jaime Tuesta de Simón and Ignacio Mascarell Agúndez (group GP11B)
**Context:** Lab assignments 1 and 2 of *Matemática Discreta* (Discrete Mathematics), 2nd year, Universidad Pontificia Comillas (ICAI), academic year 2025–2026.
**Language:** code comments, console messages and report are in Spanish; this README is in English.

> **Educational project.** The RSA implementation uses small keys, encrypts one character at a time and uses a home-made padding scheme. It is meant to illustrate the mathematics and must not be used to protect real data.

## Overview

The project has two parts that build on each other:

1. **`modular.py`, a number theory library, and IMAT-LAB, its command interpreter.** The library covers primality testing, prime factorisation, gcd and Bézout coefficients (with Lehmer's algorithm for large integers), fast modular exponentiation, modular inverses, Euler's totient, the Legendre symbol, systems of linear congruences with arbitrary moduli, modular square roots (Cipolla's algorithm) and quadratic equations modulo a prime. `imatlab.py` exposes all of this through text commands, interactively or in batch mode.
2. **RSA on top of the library.** The second part adds key generation, decimal padding, encryption of strings, a program to register users, a two-user encrypted chat, and two attacks:
   - **key attack:** factor *n* to compute φ(*n*) and recover *d*;
   - **chosen-plaintext attack:** decrypt an unpadded message using only the public key, by encrypting every possible character and matching the ciphertexts.

## How to run

Python 3.10 or newer is required. Only the standard library is used, so there is nothing to install.

```bash
# IMAT-LAB
python imatlab.py                           # interactive mode (an empty line exits)
python imatlab.py "resolverSistema([1;1;6],[1;1;9],[1;1;12])"   # single command -> 1 (mod 36)
python imatlab.py commands.txt              # one command per line, results to the screen
python imatlab.py commands.txt results.txt  # results to a file

# RSA
python registrarusuario.py                  # asks for a name, a prime interval and padding digits
python criptochat.py alice bob              # alice encrypts for bob and decrypts messages sent to her
```

`registrarusuario.py` writes the keys to a `Usuarios/` folder in the working directory:
- `pub_<name>.txt` contains *n*, *e* and the number of padding digits;
- `priv_<name>.txt` contains *d*.

To chat, register both users (for example with primes between 1000 and 10000), then run `criptochat.py` once for each of them. Paste the ciphertext produced by one user into the other user's chat to decrypt it.

The attacks are library functions:

```python
import rsa
n, e, d = rsa.generar_claves(1000, 10000)
c = rsa.cifrar_cadena_rsa("Hola", n, e, 0)   # no padding
rsa.romper_clave(n, e) == d                  # key attack -> True
rsa.ataque_texto_elegido(c, n, e)            # chosen-plaintext attack -> 'Hola'
```

IMAT-LAB prints `NOP` for invalid commands and `NE` when a valid command has no solution. The full list of commands is shown in interactive mode and described in the report.

## Method highlights

- **Primality and factorisation.** Trial division by 2, 3 and candidates of the form 6k ± 1 up to √n. A Miller–Rabin test is also implemented but not used by the rest of the library.
- **Bézout coefficients.** Extended Euclid, switching to Lehmer's algorithm when both numbers exceed 128 bits.
- **Systems of congruences.** Each equation *a·x ≡ b (mod p)* is reduced to *x ≡ c (mod p/d)*. The equations are then merged one at a time, checking compatibility modulo gcd(M, p), so the moduli need not be pairwise coprime.
- **Square roots.** Cipolla's algorithm, working in the extension F_p[ω] with ω² = t² − n.
- **RSA.** Keys come from two distinct random primes in a user-given interval. Padding appends *k* random decimal digits (*m′ = m·10^k + r*), so the same character no longer always gives the same ciphertext. That randomness is what defeats the chosen-plaintext attack.

## Repository structure

```
├── modular.py              # number theory library (part 1)
├── imatlab.py              # IMAT-LAB command interpreter (part 1)
├── rsa.py                  # RSA functions and attacks (part 2)
├── registrarusuario.py     # creates a user and stores their keys (part 2)
├── criptochat.py           # encrypted chat between two users (part 2)
├── report/
│   ├── Memoria_Aritmetica_Modular_RSA.pdf   # report covering both parts (Spanish)
│   └── memoria.tex                          # LaTeX source of the report
└── README.md
```

## Limitations

- Not secure:
  - keys are small and characters are encrypted independently;
  - the padding is not a standard scheme such as OAEP;
  - there is no authentication or integrity check.
- Key generation lists every prime in the interval, so it does not scale beyond keys of a few tens of bits per prime.
- The key attack factors *n* by trial division and is only feasible for small moduli.
- Decrypting with the wrong private key produces meaningless characters; the scheme cannot detect it.
- `raiz_mod_p` and `ecuacion_cuadratica` assume a prime modulus and do not check it.

## Changes made for publication

The original assignments were submitted separately, with their own reports. For this repository:

- **`modular.py`**
  - `bezout` now returns correct coefficients when an input is negative. This also fixes modular inverses and `bezout_n` with negative numbers.
  - A single `resolver_sistema_congruencias` now handles non-coprime and negative moduli, replacing the two previous functions.
  - `lista_primos(0, 2)` now returns `[]`.
  - `ecuacion_cuadratica` raises `IncompatibleEquationError` when *a* ≡ 0 (mod p).
  - The documentation now states that Miller–Rabin is not used.
- **`imatlab.py`**
  - Restructured into one function per command, with centralised error handling.
  - The interactive mode keeps reading commands until an empty line.
  - Some invalid inputs no longer print `NE` followed by a result.
  - Negative moduli are accepted where the library supports them.
- **`rsa.py`:** `ataque_texto_elegido` is now an actual chosen-plaintext attack. It previously recovered the private key instead.
- **`registrarusuario.py`**
  - Correctly ordered intervals are now accepted; previously they were rejected.
  - The program asks again when the interval does not contain two distinct primes.
  - Negative padding is rejected.
  - The public and private exponents are written to the correct files; they were swapped.
- **`criptochat.py`:** non-numeric ciphertexts, undecodable messages and missing key files are reported instead of crashing the program.
- **Report:** the two reports were merged into a single revised report. Student ID numbers were removed, and the decrypted text from the assignment statement is not reproduced.
