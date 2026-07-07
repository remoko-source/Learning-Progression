# Day 6 — Config Eksternal & Credential Handling

## Materi

- Pisahkan data yang sering berubah (coin list, threshold, interval) ke `config.json`
- Pisahkan data sensitif (API key) ke `.env`, load pakai `python-dotenv`
- `.gitignore` di root repo sudah cover `.env` untuk semua subfolder — tidak perlu `.gitignore` per folder
- `python-dotenv` wajib di-install di dalam venv (bukan global), dan sekali install dipakai terus di project berikutnya

## Mp-06 — Resilient Market Config Tracker

Gabungan retry logic (Day 5) + config eksternal (Day 6) + tabulate (Day 4).

### Struktur fungsi

```
get_logger()      -> setup logger (FileHandler + StreamHandler, level beda)
load_config()     -> baca config.json
fetch_retry()     -> request + retry dengan exponential backoff
build_table()     -> gabungkan hasil fetch jadi tabel tabulate
main()            -> alur utama
```

### Bug yang ditemukan & diperbaiki

1. **`requests.exception` → `requests.exceptions`**
   Typo modul, kurang huruf "s". Muncul di dua tempat (HTTPError dan ConnectionError/Timeout).

2. **`params["id"]` → `params["ids"]`**
   CoinGecko butuh key `"ids"`, bukan `"id"`.

3. **List harus di-`.join()` jadi string sebelum masuk params**
   `config["coins"]` itu list Python — request butuh string dipisah koma.
   `",".join(config["coins"])`

4. **`response is None` tapi kode lanjut ke `response.json()`**
   Kalau semua retry gagal, `fetch_retry()` return `None`. Tanpa `return` setelah `logger.critical(...)`, baris berikutnya (`response.json()`) tetap jalan dan crash `AttributeError`.
   Fix: `return` setelah log critical.

5. **`build_table()` butuh `config` DAN `data_harga` — bukan cuma salah satu**
   - `config["coins"]` = daftar coin yang *seharusnya* dicek (rencana)
   - `data_harga` = hasil fetch yang berhasil (kenyataan — CoinGecko diam saja untuk ID invalid, tidak error)
   - Coin yang gagal tidak akan muncul di `data_harga` kalau tidak digabung manual

   Solusi akhir pakai dict comprehension:
   ```python
   result = {coin: hasil_fetch.get(coin) for coin in config["coins"]}
   ```
   `hasil_fetch.get(coin)` return `None` kalau coin tidak ditemukan — `build_table()` tinggal cek `if value == None` untuk render status ERROR.

### Konsep kunci

**Retry logic — permanen vs sementara**
- Error permanen (401, 403, 404) → langsung `break`, retry percuma
- Error sementara (5xx, ConnectionError, Timeout) → retry dengan exponential backoff (`(i+1) * interval`)

**Kenapa `config` dan `data_harga` harus digabung, bukan pakai salah satu saja**
CoinGecko tidak melempar error untuk coin ID yang salah — dia cuma tidak mengembalikan key itu di response. Kalau `build_table()` cuma loop dari `data_harga`, coin yang gagal akan **hilang total** dari tabel, bukan tampil sebagai FAILED. Makanya butuh `config["coins"]` sebagai acuan daftar lengkap.

**Threshold check — di-skip untuk Mp-06 ini**
Butuh baseline harga sebelumnya untuk hitung persen perubahan. Program Mp-06 jalan sekali lalu selesai (bukan loop terus-menerus), jadi tidak ada "harga sebelumnya" untuk dibandingkan kecuali baseline disimpan persist ke file. Scope creep dari tujuan Day 6 (config + retry) — jadi materi terpisah nanti saat sistem benar-benar jalan kontinu.

## Status

- Day 6: Selesai
- Mp-06: Selesai, output tabulate sudah sesuai requirement (coin gagal tetap tampil dengan status ERROR)

## Selanjutnya

Phase 3 Capstone — Mini Market Scanner