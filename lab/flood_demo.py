#!/usr/bin/env python3
"""Demo klien: 50 request ke localhost, nomor sintetis. Bukan target nyata."""
import json, urllib.request, urllib.error, time, collections

URL   = "http://127.0.0.1:8765/api/otp/request"
PHONE = "081200000000"   # sintetis
N     = 50

def one():
    req = urllib.request.Request(
        URL,
        data=json.dumps({"phone": PHONE}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=3) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}")
    except Exception as e:
        return 0, {"error": type(e).__name__}

def main():
    stats = collections.Counter()
    t0 = time.time()
    for i in range(1, N + 1):
        code, body = one()
        stats[code] += 1
        if i <= 5 or i % 10 == 0:
            print(f"[{i:02d}] {code} {body}")
        time.sleep(0.05)
    dt = time.time() - t0
    print("\n=== HASIL ===")
    for k, v in sorted(stats.items()):
        print(f"  http {k}: {v}")
    sent = stats.get(200, 0)
    blocked = stats.get(429, 0)
    print(f"\n  terkirim : {sent}")
    print(f"  ditolak  : {blocked}")
    print(f"  durasi   : {dt:.2f}s")
    print(f"  efektivitas: {sent/N*100:.1f}% request lolos rate limit")
    if blocked > 0:
        print("  kesimpulan: rate limit menahan flood; sisa request tidak sampai ke SMS gateway.")

if __name__ == "__main__":
    main()
