import requests, time
from collections import defaultdict

def whale_flip():
    print("Base — Whale Flip Detector (whale buys/sells same token repeatedly)")
    # wallet_token → [timestamps]
    flips = defaultdict(list)

    while True:
        try:
            r = requests.get("https://api.dexscreener.com/latest/dex/transactions/base?limit=500")
            now = time.time()

            for tx in r.json().get("transactions", []):
                if tx.get("valueUSD", 0) < 50_000: continue  # whale only

                wallet = tx["from"]
                pair = tx["pairAddress"]
                side = tx["side"]
                key = (wallet, pair)

                flips[key].append((now, side))

                # Keep last 5 actions
                if len(flips[key]) > 5:
                    flips[key] = flips[key][-5:]

                actions = [s for t, s in flips[key][-4:]]  # last 4
                if actions.count("buy") >= 2 and actions.count("sell") >= 2:
                    token = tx["token0"]["symbol"] if "WETH" in tx["token1"]["symbol"] else tx["token1"]["symbol"]
                    print(f"WHALE FLIPPING HARD\n"
                          f"Wallet {wallet[:10]}... trading {token} non-stop\n"
                          f"Last actions: {' → '.join(actions)}\n"
                          f"https://dexscreener.com/base/{pair}\n"
                          f"https://basescan.org/address/{wallet}\n"
                          f"→ Scalping or manipulating — high volatility incoming\n"
                          f"{'FLIP'*30}")
                    flips[key].clear()  # reset after alert

        except:
            pass
        time.sleep(1.5)

if __name__ == "__main__":
    whale_flip()
