# Day 6 — Logging Module 🟡

## Kenapa logging, bukan print()?

`print()` cuma tampil di layar lalu hilang. `logging` mencatat kejadian ke file
dengan timestamp + level kepentingan, jadi bisa dibaca kapan saja.

Penting untuk AI Trading Agent: bot jalan 24 jam tanpa pengawasan, logging =
satu-satunya cara "melihat ke belakang" kalau ada masalah.

---

## Setup Dasar — basicConfig()

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    filename="bot.log",
    format="%(asctime)s - %(levelname)s - %(message)s"
)
```

- `level` → ambang batas minimum yang dicatat
- `filename` → nama file log (otomatis dibuat)
- `format` → template tiap baris log (placeholder otomatis diisi)
- `filemode="w"` → tulis ulang dari awal tiap run ("a" = append, default)
- `datefmt="%Y-%m-%d %H:%M:%S"` → mempercantik format timestamp

---

## Level Severity (urutan rendah → tinggi)

```
DEBUG < INFO < WARNING < ERROR < CRITICAL
```

Semua level **sama atau lebih tinggi** dari `level` yang diset akan dicatat,
yang lebih rendah dibuang.

| Level | Untuk apa | Contoh |
|---|---|---|
| DEBUG | Detail teknis, hanya untuk programmer | "Raw API response: {...}" |
| INFO | Kejadian normal/penting, sesuai rencana | "Order BUY berhasil, beli 0.5 BTC" |
| WARNING | Aneh, tapi program masih lanjut | "Saldo tidak mencukupi" |
| ERROR | Ada yang gagal, tapi sistem masih hidup | "Gagal ambil harga: timeout" |
| CRITICAL | Sistem harus berhenti total / darurat | "API key invalid, bot dihentikan" |

**Catatan penting:** "1 fungsi gagal tapi sistem lain masih jalan" = ERROR,
bukan CRITICAL. CRITICAL hanya kalau seluruh sistem harus berhenti.

---

## Logger Object + Multiple Handler

`basicConfig()` cuma bisa nulis ke 1 tempat. Untuk nulis ke file DAN console
sekaligus, pakai logger object custom:

```python
logger = logging.getLogger("trading_bot")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("bot.log", mode="w")
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)
```

### Alur 2 lapis filter

```
logger.setLevel()  ← gerbang utama (filter pertama)
       ↓ lolos?
  dikirim ke SEMUA handler terdaftar
       ↓
handler.setLevel()  ← filter kedua (per handler)
       ↓ lolos?
  ditulis ke tujuan (file/console)
```

Kalau pesan ditolak di `logger.setLevel()`, handler manapun **tidak akan
pernah kebagian** pesan itu — gerbang utama lebih duluan dicek.

**Best practice:** `logger.setLevel(DEBUG)` (buka selebar-lebarnya), lalu
masing-masing handler yang menyaring lebih lanjut sesuai kebutuhan.

---

## Konsep Tambahan

- `sys.stderr` vs `sys.stdout` — 2 "saluran keluaran" bawaan komputer.
  `StreamHandler()` default ke `sys.stderr`.
- `SyntaxError` (lupa kutip/kurung) → program gak bisa jalan sama sekali,
  beda dengan runtime exception (error saat program sudah jalan, bisa
  ditangkap `try-except`).
- `traceback` (module berbeda, belum dipakai) → menampilkan detail lengkap
  lokasi error saat exception terjadi.

---

## Mini Project Day 6 — Mini Trading Logger System (Mp-06.py)

- Logger dengan 2 handler: file (level DEBUG, mode "w") + console (level INFO)
- Proses order BUY/SELL dari list of dict, pakai `try-except KeyError` untuk
  data order yang gak lengkap
- Validasi saldo sebelum BUY (kalau gak cukup → WARNING, bukan error)
- Validasi jumlah coin sebelum SELL — tambah variabel custom `jumlah` untuk
  tracking kepemilikan coin (inisiatif sendiri)
- Bug yang ditemukan & diperbaiki sendiri:
  - `i['harga'] - saldo_awal` → seharusnya `total - saldo_awal`
  - `jumlah` belum di-inisialisasi (`jumlah = 0`) sebelum loop
- Refleksi: requirement awal "saldo habis → CRITICAL + break" ternyata kurang
  tepat — pendekatan WARNING per-order (program tetap lanjut) lebih masuk akal

---

## Bonus untuk Day 7+

- Materi `random` module (sengaja ditunda, jangan dicampur showcase)
-