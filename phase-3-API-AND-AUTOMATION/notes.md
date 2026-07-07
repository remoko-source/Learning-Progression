# Phase 3 — API & Automation — Ringkasan Lengkap

**Status:** SELESAI ✓
**Fokus:** Fetching live data dari API, resilient system design, config eksternal

---

## Daftar Project yang Dibangun

| Hari | Nama Project | Konsep Utama |
|---|---|---|
| Day 1 | Crypto Price Checker | `requests`, parsing JSON, `raise_for_status()` |
| Day 2 | Fear & Greed Viewer | Nested dict/list, Unix timestamp, Alternative.me API |
| Day 3 | BTC Alert Bot | `while True`, cooldown, `time.time()`, multi-threshold dict |
| Day 4 | Multi-Coin Price Tracker | `tabulate`, `deepcopy`, baseline tracking, `floatfmt` |
| Day 5 | Retry Logic & Resilience | Retry pattern, batas percobaan, exponential backoff |
| Day 6 (Mp-06) | Resilient Market Config Tracker | Gabungan retry logic + config eksternal + tabulate |
| Capstone | Mini Market Scanner | Integrasi semua skill Phase 3 + baseline persist antar-run |

---

## Ringkasan Materi per Hari

### Day 1 — Crypto Price Checker
- `requests.get()` untuk fetch data dari CoinGecko public API
- `raise_for_status()` **wajib** dipanggil sebelum `.json()`, bukan setelah
- Parsing response JSON jadi dictionary Python

### Day 2 — Fear & Greed Viewer
- Navigasi struktur data nested (dict di dalam list, list di dalam dict)
- Unix timestamp — detik sejak 1 Jan 1970, konversi pakai `datetime.fromtimestamp(int())`
- Sumber API kedua: Alternative.me (beda struktur response dari CoinGecko)

### Day 3 — BTC Alert Bot
- Loop `while True` untuk polling berkala
- `time.time()` untuk hitung selisih waktu (cooldown), beda tujuan dari `datetime.now()` (buat display)
- Multi-threshold pakai dictionary mapping level → config
- `try-except KeyboardInterrupt` lebih idiomatis diletakkan **di luar** `while` loop

### Day 4 — Multi-Coin Price Tracker
- Fetch multi-coin dalam satu request via batching: `ids=bitcoin,ethereum,solana`
- `','.join(list)` untuk generate comma-separated string dari list Python
- `list.copy()` = shallow copy; `copy.deepcopy()` untuk independensi total dari data asli
- `tabulate`: perbedaan `headers="keys"` (list of dict) vs headers manual (list of list)
- `floatfmt` bisa berupa tuple per-kolom untuk handle skala angka berbeda — jumlah elemen tuple harus cocok jumlah kolom
- Baseline tracking versi tetap vs rolling — beda tujuan penggunaan

### Day 5 — Retry Logic & Resilience
- Retry pattern: coba ulang request yang gagal dalam batas percobaan tertentu
- Exponential backoff: `delay * (2 ** attempt)` — delay antar percobaan makin lama biar gak membanjiri server
- Perbedaan error permanen (401/403/404 — jangan retry, langsung stop) vs error sementara (5xx, ConnectionError, Timeout — layak diulang)

### Day 6 (Mp-06) — Resilient Market Config Tracker
- Menggabungkan retry logic (Day 5) + config eksternal (JSON) + `python-dotenv` untuk credential
- `config["coins"]` (planned) digabung dengan hasil fetch aktual pakai dict comprehension: `{coin: hasil_fetch.get(coin) for coin in config["coins"]}` — supaya coin yang gagal fetch tetap muncul di tabel sebagai FAILED, bukan hilang begitu saja

### Capstone — Mini Market Scanner
- Integrasi seluruh skill di atas dalam struktur modular multi-file (`logger.py`, `fetcher.py`, `baseline_store.py`, `analyzer.py`, `main.py`)
- Fitur baru: **baseline tracking lintas-proses** — harga hari ini dibandingkan dengan harga run sebelumnya (dibaca dari `baseline.json`), bukan dalam satu eksekusi program yang sama
- Deteksi "🔥 MOVER" — coin yang pergerakan harganya melewati threshold tertentu

---

## Key Learnings — API & Networking

- `raise_for_status()` WAJIB dipanggil setelah `requests.get()`, sebelum akses `.json()`
- Status 5xx = fatal error di sisi server (layak retry); status 401/403/404 = error permanen (jangan retry, langsung stop)
- Nama coin di CoinGecko harus pakai ID resmi API, bukan nama umum sembarangan
- CoinGecko public API: limit sekitar 5–15 calls/menit, cache API update tiap 1–2 menit — fetch tiap 30–60 detik itu aman
- `params` di `requests.get()` dikombinasikan dengan `.join()` untuk convert list Python jadi string comma-separated yang dibutuhkan API

## Key Learnings — File & Data

- `write_text()` selalu overwrite; kalau butuh append, pakai `open("a")`
- JSON tidak bisa langsung di-append — alurnya: load → update dict di Python → dump ulang pakai mode `"w"`
- Safe read pattern: guard clause `exists()` **dikombinasikan** dengan `try-except JSONDecodeError` — file yang ada tapi kosong/corrupt tetap bisa bikin `json.load()` crash kalau cuma cek `exists()` saja
- `list.copy()` itu shallow copy; `copy.deepcopy()` untuk salinan yang benar-benar independen

## Key Learnings — Python Patterns

- Urutan multiple `except`: dari yang paling spesifik ke paling general
- `logger.info()` pakai f-string, bukan koma seperti `print()`
- `Path.home()` / `Path.cwd()` adalah best practice untuk portabilitas antar device/GitHub — hindari hardcode path absolut
- `random.random()` menghasilkan float 0.0–1.0, bukan 0–100
- `json.load/loads/dump/dumps`: pola "load-dump" untuk file, "loads-dumps" untuk string
- `default=converter` dipakai untuk serialisasi tipe data yang bukan native JSON (misal `datetime`, `Path`)
- `isinstance()` untuk mengecek tipe data sebelum diproses
- `dict.pop("key_name")` berbeda perilaku dari `list.pop(index)`
- Circular import terjadi kalau dua modul saling bergantung satu sama lain — arah dependency harus dijaga satu arah
- Operator precedence: `**` (eksponen di Python) beda dari `^` (XOR) — sering ketuker orang yang baru pindah dari bahasa lain
- Conditional expression: `nilai_true if kondisi else nilai_false` — urutan baca beda dari urutan eksekusi (kondisi dicek duluan meski ditulis di tengah)
- Dict comprehension: `{k: v for k in list}` — cara ringkas mengubah list jadi dictionary

## Key Learnings — Time & Display

- Unix timestamp dikonversi pakai `datetime.fromtimestamp(int())`
- `time.time()` untuk kalkulasi selisih waktu (durasi, cooldown); `datetime.now()` untuk keperluan display ke user
- Cooldown vs `time.sleep()` — dua konsep dengan tujuan berbeda, bisa digabung tapi total delay harus dihitung dengan hati-hati
- Windows 8 CMD/PowerShell tidak mendukung emoji — gunakan label teks sebagai gantinya

## Key Learnings — Looping & Struktur Program

- `try-except KeyboardInterrupt` lebih idiomatis diletakkan di luar `while` loop
- Fetch API harus berada di dalam `while` loop dan di luar `for` loop (per-coin)
- `last_alert = 0` valid sebagai representasi "belum pernah alert sebelumnya"
- Multi-threshold sebaiknya pakai dictionary yang memetakan level → konfigurasi, bukan banyak if-else terpisah

## Key Learnings — Tabulate

- List of dict cocok pakai `headers="keys"`; list of list butuh header manual — masing-masing ada tradeoff dan perlu familiar dengan keduanya
- `floatfmt` bisa berupa tuple untuk format berbeda per kolom; jumlah elemen tuple wajib sama dengan jumlah kolom

## Key Learnings — Engineering Mindset

- Overengineering itu beda dari bug matematika/logika yang menghasilkan data salah — yang kedua **wajib** diperbaiki, bukan dianggap "sudah cukup"
- Hard-coded rules (seperti threshold, batas retry) untuk hal yang butuh determinism — prinsip ini nanti jadi dasar untuk `risk/` guardrails di Phase 8

---

## Koneksi ke Roadmap AI Trading Agent

Phase 3 ini membangun fondasi untuk:
- **`api/`** — pola fetch + retry + config eksternal yang dipakai di sini akan jadi dasar koneksi ke exchange/data provider yang lebih kompleks
- **`analysis/`** — `calculate_change()` dan `is_mover()` adalah versi paling sederhana dari deteksi pattern yang nanti berkembang jauh di Phase 8
- **`memory/`** — `baseline_store.py` adalah cikal bakal trade journal/histori yang nanti pindah ke SQLite di Phase 6.5