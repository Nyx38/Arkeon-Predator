# Arkeon-Predator

Arkeon-Predator is an advanced, autonomous Bitcoin wallet scanner designed for Termux and Linux environments. It leverages high-speed local filtering to scan BTC addresses without the risk of API rate-limiting or privacy leaks.

## Features
- **Local-First Scanning:** Uses BloomFilter for lightning-fast address matching with minimal RAM usage.
- **Hybrid Engine:** Combines random Hex brute-forcing with BIP39 Mnemonic Typo-Hunting.
- **Autonomous Sweeper:** Integrated automated fund transfer (sweep) for identified active wallets.
- **Termux Optimized:** Designed to run 24/7 on mobile devices with CPU thermal protection and multi-threading.
- **No API Dependency:** Performs heavy lifting locally, only connecting to the network when a match is found.

## Setup
1. Clone the repository: `git clone https://github.com/yourusername/Arkeon-Predator.git`
2. Install requirements: `pip install -r requirements.txt`
3. Prepare your `temiz_adresler` (target addresses) and `bip39.txt` files.
4. Launch the engine: `python arkeon.py`

## Security Warning
This tool is for educational purposes and research on Bitcoin wallet security. Use responsibly and ensure you own the destination wallet address.
