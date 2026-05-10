import json
import os

entity_files = [
    "coinbase.json", "binance.json", "kraken.json", "okx.json",
    "circle.json", "paxos.json", "tether.json",
    "anchorage.json", "bitgo.json", "tornado_cash.json"
]

for filename in entity_files:
    filepath = os.path.join("entities", filename)
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
        print(f"✓ {filename}: VALID — entity_id is '{data['entity_id']}'")
    except FileNotFoundError:
        print(f"✗ {filename}: FILE NOT FOUND")
    except json.JSONDecodeError as e:
        print(f"✗ {filename}: INVALID JSON — {e}")
    except KeyError as e:
        print(f"✗ {filename}: MISSING KEY — {e}")