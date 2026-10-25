# OTP Rate-Limit Lab — owner @sidzx12

Lab lokal untuk mendemonstrasikan mengapa flood OTP gagal dan bagaimana
rate limiting seharusnya dipasang. **Semua trafik ke 127.0.0.1.**

## Yang TIDAK ada di repo ini
- Tidak ada client ke layanan OTP pihak ketiga.
- Tidak ada bypass rate limit / CAPTCHA / device fingerprint.
- Tidak ada daftar nomor target atau rotasi proxy.

## Termux
    pkg update && pkg install python -y
    git clone <repo-url> otp-ratelimit-lab
    cd otp-ratelimit-lab
    python main.py

## Hasil yang diharapkan
Menu -> opsi 2 -> sekitar 3 dari 50 request mendapat 200, sisanya 429.
Angka itu bukan kegagalan demo; itu bukti kontrol bekerja.

## Parameter lab
ubah `WINDOW_SEC`, `MAX_PER_WIN`, `COOLDOWN_SEC` di `lab/otp_server.py`
untuk melihat efek pada laju request yang lolos.
