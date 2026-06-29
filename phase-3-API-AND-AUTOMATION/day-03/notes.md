# Phase 3 — Day 3: BTC Alert Bot

## Yang Dibangun
Bot monitoring harga BTC secara otomatis dengan sistem alert berlevel, cooldown logic, dan countdown timer.

---

## Konsep Baru

### `while True`
Loop yang jalan terus tanpa henti sampai ada kondisi yang menghentikannya (`break` atau `KeyboardInterrupt`).

### `time.sleep(detik)`
Membuat program "istirahat" selama N detik. Berguna untuk:
- Jaga CPU agar tidak kerja sia-sia
- Delay antar aksi

### `time.time()`
Mengembalikan Unix timestamp — jumlah detik sejak 1 Jan 1970.
- Bukan untuk ditampilkan, tapi untuk **dihitung selisihnya**
- Selalu berjalan, tidak peduli program nyala atau tidak
- Untuk display jam yang benar tetap pakai `datetime.now().strftime()`

```python
start = time.time()
# ... beberapa saat kemudian ...
elapsed = time.time() - start  # selisih dalam detik
```

### Countdown Timer
Cek selisih dari `start` — kalau sudah melewati durasi, `break`.

```python
start = time.time()
durasi = 60

while True:
    if time.time() - start >= durasi:
        break
```

### Rate Limiter / Cooldown Logic
Simpan timestamp terakhir aksi, cek selisihnya sebelum aksi lagi.

```python
last_alert = 0  # 0 = belum pernah, selisih pasti besar → langsung jalan

if time.time() - last_alert >= cooldown:
    # lakukan aksi
    last_alert = time.time()  # update timestamp
```

### Multi-threshold dengan Dictionary
Mapping level alert ke konfigurasi masing-masing — lebih clean daripada if-elif panjang.

```python
levels = {
    "WARNING":  {"min": 65000, "max": 70000, "freq": 500},
    "DANGER":   {"min": 60000, "max": 65000, "freq": 1000},
    "CRITICAL": {"min": 0,     "max": 60000, "freq": 2000},
}

for level, config in levels.items():
    if config["min"] <= harga < config["max"]:
        winsound.Beep(config["freq"], 500)
```

### `winsound.Beep(frekuensi, durasi_ms)`
Bunyi alert di Windows. Makin tinggi frekuensi, makin nyaring.

```python
winsound.Beep(1000, 500)  # 1000Hz selama 500ms
```

---

## Perbedaan Penting

| | `time.sleep()` | Cooldown |
|---|---|---|
| Fungsi | Ngatur kecepatan loop | Ngatur kapan alert boleh bunyi |
| Saling ganti? | Tidak — beda tujuan |  |
| Gabung? | Bisa — tapi hitung total delay-nya |  |

| | `time.time()` | `datetime.now()` |
|---|---|---|
| Tujuan | Kalkulasi selisih waktu | Display jam ke user |
| Output | Float besar (Unix timestamp) | Object datetime |

---

## Bug yang Ditemukan & Diperbaiki

### Fetch di dalam `for` loop
Fetch API tidak boleh ada di dalam `for level in levels` — artinya fetch dilakukan sebanyak jumlah level per putaran.
**Fix:** pindahkan fetch ke atas `for` loop.

### Fetch di luar `while` loop
Harga tidak pernah update kalau fetch hanya dilakukan sekali sebelum loop.
**Fix:** fetch harus ada di dalam `while True`.

### Cooldown + `time.sleep()` menambah delay
Kalau pakai keduanya, total delay = cooldown + sleep.
**Fix:** pilih salah satu, atau pakai `time.sleep(0.1)` sebagai penjaga CPU saja.

---

## CoinGecko Public API
- Rate limit: **5–15 calls per menit** (tergantung traffic global)
- Cache harga: update setiap **1–2 menit**
- Aman: fetch maksimal setiap **30–60 detik**
- `raise_for_status()` wajib ditambahkan agar error dari server tertangkap sebelum akses data

---

## Struktur Akhir Bot

```
inisialisasi variabel & print header
└── while True
    ├── cek countdown → break kalau habis
    └── cek cooldown → kalau boleh:
        ├── fetch harga dari API
        ├── loop levels → cek threshold
        │   └── kalau match → print + beep
        └── update last_alert
    time.sleep(0.1)  ← jaga CPU
```

---

## Relevansi ke AI Trading Agent
- **Rate limiter** → akan terus dipakai sampai Phase Agent untuk throttle request ke API maupun LLM
- **Multi-threshold** → cikal bakal signal level system (entry, warning, exit)
- **while True + sleep** → pola dasar scheduler agent yang akan dipakai di Phase 8