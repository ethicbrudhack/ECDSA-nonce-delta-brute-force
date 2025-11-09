Bitcoin ECDSA Nonce-Delta Brute-Force — README

Educational tool — do not use on third-party wallets or systems you don't own or have explicit permission to test.

Small, self-contained Python script that demonstrates how correlated ECDSA nonces across two signatures can leak a private key. The script brute-forces a small integer delta between the two nonces (k2 = k1 - delta), reconstructs candidate nonces and private keys, and — if a match is found — prints the recovered private key together with its compressed public key and a Bech32 P2WPKH address.

Quick summary

Attempts to recover an ECDSA private key d when two signatures were created with nonces k1 and k2 related by a small integer difference delta.

Iterates over a configurable integer range of delta values and tests algebraic solutions for k1, k2, d1, d2.

On success the script:

prints the recovered private key d

shows the compressed public key (hex)

prints a Bech32 (bc1...) P2WPKH-style address derived from the public key

For research and educational purposes only. Use only on signatures/keys you control or for which you have written authorization.

Features

Pure-Python demonstration of the nonce-correlation attack on secp256k1.

Uses ecdsa library to derive public keys from recovered private keys.

Produces human-readable diagnostic logs during the brute-force loop (can be noisy).

Derives compressed public key and Bech32 P2WPKH address after a successful recovery.

File structure
recover_key.py        # Main script (the code you provided)


(You can split into modules later — e.g. crypto.py, scanner.py, cli.py — for readability and testing.)

How it works (high level)

ECDSA signature equation (mod n):

s = k^{-1}(z + r * d) mod n


where k is the per-signature nonce, d is the private key, r and s are signature components, z is the message hash, and n is the secp256k1 order.

If two signatures (r1, s1, z1) and (r2, s2, z2) use nonces k1 and k2 that obey k2 = k1 - delta (for small integer delta), you can solve algebraically for k1 (and k2) and then for d.

The script:

loops over candidate integer delta values,

computes candidate k1 and k2 using modular arithmetic (including modular inverses),

computes candidate private keys d1 and d2 from each signature,

if d1 == d2, treats it as a successful recovery and prints results.

Important implementation notes

The script uses Python integers and sympy.mod_inverse for modular inverses and the ecdsa package to compute public keys.

The result logging prints a line for every tested delta — this will produce very large output if the range is large.

Many delta candidates will produce modular inverse errors or divide-by-zero conditions; the script catches and skips these.

The script assumes the particular algebraic relation k2 = k1 - delta. If the real relation differs (e.g. k2 = k1 + delta), the math must be adjusted.

Output format

When a candidate is found the script prints something like:

[INFO] Found private key! d = 123456789... (delta = 42)
    k1 = ...
    k2 = ...
    d1 = ...
    d2 = ...
    Public (compressed) = 02abcdef...
    Bech32 address = bc1q...


If no candidate is found in the tested range the script prints a final message indicating failure.

Dependencies

Python 3.8+

ecdsa — key and public-key ops

sympy — modular inverse (you may replace with a faster implementation)

bech32 — Bech32 address encoding

Install via pip:

pip install ecdsa sympy bech32

How to run

Edit the script to include the two signatures you want to analyze:

r1 = int('<hex>', 16)
s1 = int('<hex>', 16)
z1 = int('<hex>', 16)

r2 = int('<hex>', 16)
s2 = int('<hex>', 16)
z2 = int('<hex>', 16)


Configure the delta search range inside brute_force_d (or add CLI flags to set min/max):

for delta in range(-10000000, 10000001):
    ...


Tip: start with a small range (e.g. ±10_000) and reduce or remove per-iteration logging for speed.

Run:

python recover_key.py

Performance tips & improvements

Reduce logging: printing each iteration is slow. Log only every N iterations or use a verbosity flag.

Use multiprocessing: split delta range across CPU cores.

Replace sympy.mod_inverse with a custom fast modular inverse (extended Euclidean) for speed.

Add verification: once d is found, verify by deriving the public key and re-checking that (r1,s1) and (r2,s2) validate for z1, z2.

Bounds pruning: add mathematical checks to skip impossible delta candidates early.

Safety, ethics & legality

This repository is educational. Do not use this script to attack, recover, or steal keys from third parties. Unauthorized recovery or use of private keys is illegal and unethical. Use only:

on keys/signatures you control,

as part of authorized security research with explicit written permission,

or for learning in a safe, isolated environment.

If you plan to use this for research, document permissions and follow local laws and ethical guidelines.

BTC donation address: bc1q4nyq7kr4nwq6zw35pg0zl0k9jmdmtmadlfvqhr
