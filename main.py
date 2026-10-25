#!/usr/bin/env python3
# owner: @sidzx12
import os, sys, subprocess, platform, time

OWNER = "@sidzx12"

def clear():
    os.system("clear" if os.name != "nt" else "cls")

def pause():
    input("\n[enter] kembali ke menu...")

def sysinfo():
    clear()
    print("=== SYSTEM INFO ===")
    print(f"owner   : {OWNER}")
    print(f"host    : {platform.node()}")
    print(f"os      : {platform.system()} {platform.release()}")
    print(f"machine : {platform.machine()}")
    print(f"python  : {platform.python_version()}")
    print(f"time    : {time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    pause()

def run_lab():
    clear()
    print("=== OTP RATE-LIMIT LAB (localhost only) ===")
    print("server akan bind 127.0.0.1:8765, lalu demo kirim 50 request.")
    print("semua trafik tetap di perangkat ini.\n")
    base = os.path.dirname(os.path.abspath(__file__))
    srv = subprocess.Popen(
        [sys.executable, os.path.join(base, "lab", "otp_server.py")],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )
    try:
        time.sleep(1.5)
        subprocess.run(
            [sys.executable, os.path.join(base, "lab", "flood_demo.py")],
            check=False
        )
    finally:
        srv.terminate()
        try:
            srv.wait(timeout=3)
        except subprocess.TimeoutExpired:
            srv.kill()
    pause()

def menu():
    while True:
        clear()
        print("=" * 40)
        print(f"  OTP RATE-LIMIT LAB   owner {OWNER}")
        print("=" * 40)
        print(" 1. System info")
        print(" 2. Jalankan lab rate-limit")
        print(" 0. Keluar")
        print("=" * 40)
        c = input("pilih > ").strip()
        if c == "1":
            sysinfo()
        elif c == "2":
            run_lab()
        elif c == "0":
            print("keluar.")
            sys.exit(0)
        else:
            print("menu tidak ada.")
            time.sleep(0.8)

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\ninterrupted.")
        sys.exit(130)
