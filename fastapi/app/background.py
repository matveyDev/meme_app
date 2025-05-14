import time
import threading
import json
from solders.signature import Signature
from app.solana import client, RECEIVING_WALLET, EXPECTED_AMOUNT_SOL
from app.storage import load_data, save_data

# Очередь ожидающих транзакций
pending_transactions = {}  # txid: {"wallet": str, "timestamp": float}

# Добавление транзакции в очередь
def track_transaction(txid: str, wallet: str):
    pending_transactions[txid] = {
        "wallet": wallet,
        "timestamp": time.time()
    }

# Фоновая проверка каждые 10 сек
CHECK_INTERVAL = 10
TX_TIMEOUT = 300  # 5 минут

def background_worker():
    while True:
        now = time.time()
        to_remove = []

        for txid, entry in pending_transactions.items():
            wallet = entry["wallet"]
            signature = Signature.from_string(txid)
            tx = client.get_transaction(signature, encoding="jsonParsed")

            if not tx or not tx.value:
                if now - entry["timestamp"] > TX_TIMEOUT:
                    to_remove.append(txid)
                continue

            result = json.loads(tx.value.to_json())
            meta = result.get("meta")
            if not meta or meta.get("err"):
                to_remove.append(txid)
                continue

            instructions = result["transaction"]["message"].get("instructions", [])
            for instr in instructions:
                parsed = instr.get("parsed")
                if not parsed:
                    continue
                if parsed.get("type") == "transfer":
                    info = parsed.get("info", {})
                    if (
                        info.get("source") == wallet and
                        info.get("destination") == RECEIVING_WALLET and
                        float(info.get("lamports", 0)) / 1e9 >= EXPECTED_AMOUNT_SOL
                    ):
                        data = load_data()
                        data[wallet]["canGenerate"] = True
                        data[wallet]['limit'] += 10
                        save_data(data)
                        to_remove.append(txid)
                        break

        for txid in to_remove:
            pending_transactions.pop(txid, None)

        time.sleep(CHECK_INTERVAL)

# Запуск фонового потока
threading.Thread(target=background_worker, daemon=True).start()
