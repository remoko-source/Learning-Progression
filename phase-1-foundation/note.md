# Phase 1 — Dasar Python — Ringkasan Lengkap

**Status:** SELESAI ✓
**Fokus:** Fondasi Python — variable, control flow, function, data structure, OOP dasar

---

## Daftar Project yang Dibangun

| Project | Konsep Utama |
|---|---|
| Capstone: CryptoVault | Aplikasi manajemen portofolio crypto modular (main.py, wallet.py, crypto.py, data.json) |

*Catatan: Phase 1 tercatat lebih fokus pada penguasaan fondasi bahasa lewat latihan bertahap, dengan CryptoVault sebagai capstone yang mengintegrasikan seluruh materi.*

---

## Ringkasan Materi

### Variable, Input/Output, Control Flow
- Variable sebagai wadah data, konvensi penamaan
- `input()`/`print()` untuk interaksi dasar dengan user
- `if-else` untuk percabangan logika
- `for`/`while` loop untuk pengulangan

### Function
- Definisi function dengan `def`, parameter, dan `return`
- Perbedaan function yang mengembalikan nilai vs yang hanya menjalankan aksi (`print` di dalam function tanpa `return`)

### List
- Struktur data terurut, bisa diakses lewat index
- Operasi dasar: `append()`, `remove()`, iterasi dengan `for`

### Dictionary
- Struktur data key-value, akses lewat key bukan index
- Nested data — dictionary di dalam dictionary, atau list di dalam dictionary
- Loop lewat data nested untuk mengakses informasi bertingkat

### File Handling — TXT & JSON
- Operasi dasar baca/tulis file `.txt`
- Pengenalan format JSON sebagai cara menyimpan data terstruktur ke file
- `try-except` untuk menangani error dasar saat membaca/menulis file

### OOP Dasar
- Konsep `class` dan `object` — cara membungkus data dan perilaku jadi satu unit
- Constructor (`__init__`), atribut, dan method dasar

---

## Key Learnings Utama

- **Variable, loop, dan function** adalah fondasi yang dipakai terus di setiap phase berikutnya — tidak ada phase yang tidak bergantung pada ini
- **Dictionary dan nested data** adalah bentuk data yang paling sering ditemui saat kerja dengan API (Phase 3 dan seterusnya) — response API hampir selalu berbentuk nested dictionary
- **File JSON** yang dipelajari di sini jadi dasar langsung untuk config eksternal (Phase 3) dan penyimpanan data terstruktur di banyak project berikutnya
- **OOP dasar** memberi pengenalan konsep `class`/`object`, meski penggunaan mendalam (inheritance, custom exception class) baru benar-benar dipraktikkan di Phase 2 (Day 7)

---

## Koneksi ke Roadmap AI Trading Agent

Phase 1 adalah fondasi bahasa yang menopang semua phase berikutnya:
- **List & Dictionary** — dipakai terus-menerus untuk memproses data API (Phase 3), config (semua phase), dan struktur data trading (Phase 8: `Trade`, `Signal`, `Position`)
- **File handling (JSON)** — cikal bakal `config.json`, `baseline.json`, dan seluruh sistem penyimpanan data eksternal
- **OOP dasar** — fondasi untuk custom exception class (Phase 2) dan class-based agent design (Phase 8)
- **CryptoVault** — project pertama yang mengenalkan pola modular (main, wallet, crypto, data) sebelum berkembang jadi TradeDesk CLI (Phase 2) lalu Mini Market Scanner (Phase 3)