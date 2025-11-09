import hashlib
import bech32
from sympy import mod_inverse
from ecdsa import SigningKey, SECP256k1

# Stała n dla secp256k1
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

def hash160(data: bytes) -> bytes:
    sha = hashlib.sha256(data).digest()
    ripemd = hashlib.new('ripemd160')
    ripemd.update(sha)
    return ripemd.digest()

def d_to_pubkey_and_bc1(d: int):
    """Zwraca (skompresowany_pubkey_hex, adres_Bech32)"""
    sk = SigningKey.from_secret_exponent(d, curve=SECP256k1)
    vk = sk.verifying_key
    x = vk.pubkey.point.x()
    y = vk.pubkey.point.y()
    prefix = b'\x02' if (y % 2 == 0) else b'\x03'
    compressed_pubkey = prefix + x.to_bytes(32, 'big')
    h160 = hash160(compressed_pubkey)
    bc1 = bech32.encode("bc", 0, h160)
    return compressed_pubkey.hex(), bc1

def brute_force_d(r1, s1, z1, r2, s2, z2):
    """Przeszukuje zakres delta od -10000 do 10000 i wyświetla logi z każdej iteracji."""
    for delta in range(-10000000, 10000001):
        print(f"[LOG] Testujemy delta = {delta}")
        try:
            # Obliczamy k1 i k2
            # Wzór k1 i k2 oparty na twojej dotychczasowej implementacji
            k1 = ((s1 * r2 - s2 * r1 + delta * s2) * mod_inverse((s1 - s2), n)) % n
            k2 = (k1 - delta) % n
            
            # Obliczamy dwa klucze prywatne
            d1 = ((s1 * k1 - z1) * mod_inverse(r1, n)) % n
            d2 = ((s2 * k2 - z2) * mod_inverse(r2, n)) % n
            
            print(f"    k1 = {k1}")
            print(f"    k2 = {k2}")
            print(f"    d1 = {d1}")
            print(f"    d2 = {d2}")
            
            # Jeśli d1 == d2, uznajemy to za potencjalny sukces
            if d1 == d2:
                print(f"[INFO] Znaleziono klucz prywatny! d = {d1} (delta = {delta})")
                
                # Generujemy publiczny klucz i adres Bech32
                pubkey_hex, bc1 = d_to_pubkey_and_bc1(d1)
                print(f"    Publiczny (skompresowany) = {pubkey_hex}")
                print(f"    Adres Bech32 = {bc1}")
                
                # Zwracamy wynik, by przerwać brute force
                return d1
        except Exception as e:
            print(f"    [ERROR] Wyjątek w iteracji delta={delta}: {e}")
            # Pomijamy tę iterację
            continue
    return None

# Dane, które podałeś
r1 = int('5ff5f23406cf26c25442f1924d823a9e92a8aa07921a586d79917c4df82ee2dc', 16)
s1 = int('18fb92555b8c06fd2692cf8f9b3ca8547ff81bf0b8c854a60c877d4f261d2013', 16)
z1 = int('b06f4026aaf81d3629e9e0bfa361f1554c47f497a101917c011dbdeccb0645ea', 16)

r2 = int('5ff5eb8f25ffac4705832fcf410738d20d112764f564d7ff23837246487660d5', 16)
s2 = int('45bbd3ab3fa2be1b86f9698e3e5c7ce36452d2e94a7e4a79c9d463ff9a9e3b36', 16)
z2 = int('cf814ec7d323a48f98d5f9c1115d9303e37eaae201a0593b80ee9a2e33825711', 16)

# Uruchamiamy brute force
print("[START] Rozpoczynamy brute-force...\n")
d = brute_force_d(r1, s1, z1, r2, s2, z2)

if d:
    print(f"\n[END] Znaleziono klucz prywatny d = {d}")
else:
    print("\n[END] Nie udało się odzyskać klucza prywatnego (w danym zakresie).")
