# Bitcoin ECDSA Nonce-Delta Brute-Force

> Educational tool — **do not** use on third-party wallets or systems you don't own or have explicit permission to test.

A small, self-contained Python script that demonstrates how correlated ECDSA nonces across two signatures can leak a private key.  
The script brute-forces a small integer `delta` between two nonces (`k2 = k1 - delta`), reconstructs candidate nonces and private keys, and — if a match is found — prints the recovered private key together with its compressed public key and a Bech32 P2WPKH address.

---

## 🚀 Quick summary

- Attempts to recover an ECDSA private key `d` when two signatures were produced with nonces `k1` and `k2` that differ by a small integer `delta`.
- Iterates over a configurable integer range of `delta` values and tests algebraic solutions for `k1`, `k2`, `d1`, and `d2`.
- On success prints:
  - recovered private key `d`
  - compressed public key (hex)
  - derived Bech32 (bc1...) P2WPKH address

> **For research and educational purposes only.** Use only on signatures/keys you control or for which you have written authorization.

---

## ✅ Features

- Pure-Python demonstration of a nonce-correlation attack targeting secp256k1.
- Uses `ecdsa` to derive public keys from recovered private keys.
- Produces diagnostic logs while brute-forcing (configurable verbosity recommended).
- Derives compressed pubkey and Bech32 address if private key recovery succeeds.
- Easy to modify: add CLI flags, change delta bounds, add multiprocessing.

---

## 📁 File structure

.
├─ recover_key.py # Main script (the code)
├─ README.md # This file
└─ examples/ # (optional) put sample inputs/outputs here


---

## 🧠 How it works (high level)

ECDSA signature equation (mod n):



s = k^{-1} (z + r * d) (mod n)


Where:
- `k` = per-signature nonce
- `d` = private key
- `(r, s)` = signature components
- `z` = message hash
- `n` = curve order (secp256k1)

If two signatures `(r1, s1, z1)` and `(r2, s2, z2)` use nonces `k1` and `k2` such that:



k2 = k1 - delta


(for small integer `delta`) then algebraic manipulations allow solving for `k1` and therefore `d`. The script loops candidate `delta` values, computes candidate `k1/k2`, derives candidate private keys `d1/d2` and reports success when `d1 == d2`.

---

## ⚙️ Configuration

Open the script and set or modify these variables / parameters:

- `r1, s1, z1` and `r2, s2, z2` — signature values (hex → int)
- `n` — secp256k1 order (already included)
- `delta` search range — adjust the `range(...)` in `brute_force_d()` or add CLI args
- Logging/verbosity — printing every iteration is expensive; consider logging only every N steps

**Dependencies**
- Python 3.8+
- `ecdsa` — for public key derivation
- `sympy` — `mod_inverse` (substitute if you prefer a faster function)
- `bech32` — Bech32 encoding

Install with:
```bash
pip install ecdsa sympy bech32

📤 Output format

When a candidate d is found the script prints:

[INFO] Found private key! d = <decimal> (delta = <value>)
    k1 = <value>
    k2 = <value>
    d1 = <value>
    d2 = <value>
    Public (compressed) = 02abcdef...
    Bech32 address = bc1q...


If no key was found in the tested delta range, the script prints an ending message indicating failure.

🏁 How to run

Edit recover_key.py and paste your signatures (only for keys you control):

r1 = int('...hex...', 16)
s1 = int('...hex...', 16)
z1 = int('...hex...', 16)

r2 = int('...hex...', 16)
s2 = int('...hex...', 16)
z2 = int('...hex...', 16)


Configure delta search range (example uses ±10_000):

for delta in range(-10000, 10001):
    ...


Run:

python recover_key.py


Tips

Start with a small range (±1,000 or ±10,000).

Disable per-iteration logging (or log every N iterations) to speed up the search.

If you want to run a large range, use multiprocessing to distribute the workload.

⚡ Performance & improvements

Remove or batch logs — printing is slow.

Use a custom modular inverse (extended Euclidean) instead of sympy for speed.

Add multiprocessing: split delta ranges by CPU core.

Add a verification step: after recovering d, derive the public key and verify that both (r1,s1) and (r2,s2) validate for z1 and z2.

Add CLI (argparse) to configure delta bounds and verbosity.

🛡️ Ethics & legality

This tool demonstrates known cryptographic weaknesses and must be used responsibly:

Only run on keys and signatures you control.

Do not attempt to recover keys from third-party wallets, exchanges, or other systems without explicit written permission.

Unauthorized key recovery or use is illegal and unethical.

If you intend to perform research on real systems, obtain documented authorization and follow applicable laws and institutional policies.

BTC donation address: bc1q4nyq7kr4nwq6zw35pg0zl0k9jmdmtmadlfvqhr
