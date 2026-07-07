# Phase 2 — Programmer Toolkit — Ringkasan Lengkap

**Status:** SELESAI ✓
**Fokus:** Standard library Python, developer tooling, version control

---

## Daftar Project yang Dibangun

| Hari | Nama Project | Konsep Utama |
|---|---|---|
| Day 1 | Package Manager Setup | `venv`, `pip install/list/freeze` |
| Day 2 | Git via Terminal | `git status/add/commit/push`, `git remote set-url`, `git log` |
| Day 3 (Mp-03) | File Organizer | `os` module — organisasi file berdasarkan ekstensi |
| Day 4 (Mp-04) | CLI Calculator | `sys` module — `sys.argv`, guard clause |
| Day 5 | Activity Logger + Time Comparator | `datetime` — parsing, formatting, perbandingan waktu |
| Day 6 (Mp-06) | Mini Trading Logger System | `logging` module — level severity, FileHandler, StreamHandler |
| Day 7 (Mp-07) | Resilient Order Validator | Error handling lanjutan, custom exception class |
| Day 7 Bonus | GACHA Trading Simulator | `random` module — probabilitas, mutable vs immutable |
| Day 8 (Mp-08) | PathScout CLI Tool | `pathlib` — operasi file/folder modern |
| Day 9 | JSON Module Deep Dive | `json` — load/loads/dump/dumps, safe read pattern |
| Capstone | TradeDesk CLI | Integrasi seluruh skill Phase 2 dalam satu tool modular |

---

## Ringkasan Materi per Hari

### Day 1 — venv, pip, requests
- `python -m venv venv` untuk membuat virtual environment terisolasi per-project
- Aktivasi/deaktivasi environment, `pip install/list/freeze` untuk kelola dependency

### Day 2 — Git via Terminal
- Perintah dasar: `pwd`, `ls`, `cd`, `git status/add/commit/push`
- `git remote set-url` untuk mengubah remote repository
- `git log`/`git log --oneline` untuk melihat histori commit
- Memahami perbedaan `-` vs `--` sebagai flag, dan bahwa maknanya bisa context-dependent antar command

### Day 3 (Mp-03) — os module
- `os.getcwd()`, `os.mkdir()`, `os.makedirs()` untuk manajemen folder
- `os.path.exists()`, `os.path.join()`, `os.path.splitext()` untuk manipulasi path
- `os.listdir()` untuk membaca isi folder
- `exist_ok=True` untuk mencegah error saat folder sudah ada
- **Project:** File Organizer — otomatis memindahkan file ke folder berdasarkan ekstensinya

### Day 4 (Mp-04) — sys module
- `sys.argv` untuk menerima argumen dari command line
- `sys.exit()` untuk keluar program dengan kontrol eksplisit
- Guard clause untuk validasi input sebelum eksekusi lanjut
- Konversi `int()` untuk argumen dari `sys.argv` (selalu berbentuk string)
- **Project:** CLI Calculator yang menerima operasi matematika lewat argumen terminal

### Day 5 — datetime
- `datetime.now()`, `.strftime()` untuk format tampilan, `.strptime()` untuk parsing string jadi datetime
- `timedelta` untuk operasi penjumlahan/pengurangan waktu
- Pattern `is None` sebagai flag untuk cek "belum pernah terjadi"
- Perbandingan datetime bisa dilakukan langsung dengan operator `<`, `>`, dll
- **Project:** Activity Logger dengan bonus Time Comparator

### Day 6 (Mp-06) — logging
- `logging.basicConfig()` untuk setup cepat
- Level severity: DEBUG → INFO → WARNING → ERROR → CRITICAL
- Logger object lengkap: `getLogger()`, `setLevel()`, `FileHandler`, `StreamHandler`, `Formatter`, `addHandler()`
- Alur 2 lapis filter: level logger vs level masing-masing handler
- Pengenalan `sys.stderr`/`sys.stdout`, perbedaan `SyntaxError` (error sebelum program jalan) vs runtime Exception (error saat program jalan), serta cara membaca traceback
- **Project:** Mini Trading Logger System

### Day 7 (Mp-07) — Error handling lanjutan
- `try-except-else-finally` — alur lengkap penanganan error
- Multiple except: urutan dari yang paling spesifik ke paling general
- `raise` untuk melempar exception secara manual
- Custom exception class (inheritance dari `Exception`)
- `for-else` — blok `else` pada loop yang jalan hanya kalau loop selesai tanpa `break`
- **Project:** Resilient Order Validator dengan custom exception `SaldoTidakCukupError` dan `CoinTidakDitemukanError`

### Day 7 Bonus — random module
- `randint()`, `choice()`, `random()` (menghasilkan float 0.0–1.0, bukan 0–100), `uniform()`, `shuffle()` (memodifikasi list secara in-place)
- Konsep mutable (list) vs immutable (int/str) — mutable bisa diubah langsung tanpa `return`
- Perbedaan `list.pop(index)` vs `list.remove(value)`
- **Project:** GACHA Trading Simulator dengan 5 jalur probabilitas, custom exception `FailedPurchaseError`

### Day 8 (Mp-08) — pathlib
- `Path()`, operator `/` untuk menggabungkan path (lebih modern dari `os.path.join()`)
- `Path.cwd()`/`Path.home()` untuk portabilitas antar device
- `.mkdir(parents=True, exist_ok=True)` untuk membuat folder bertingkat dengan aman
- Attribute berguna: `.name`, `.stem`, `.suffix`, `.parent`
- `.write_text()`/`.read_text()` untuk operasi file singkat; `open("a")` tetap dibutuhkan untuk mode append
- `.exists()`, `.is_file()`, `.is_dir()` untuk validasi
- `.iterdir()`, `.glob()` untuk menjelajahi isi folder; `.stat().st_size` untuk info ukuran file
- **Project:** PathScout CLI Tool dengan custom exception `PathNotFoundError`

### Day 9 — JSON Module
- `json.load()`/`json.loads()` untuk membaca (dari file / dari string)
- `json.dump()`/`json.dumps()` untuk menulis (ke file / ke string)
- Pola aman: load → update dict di Python → dump ulang dengan mode `"w"` (JSON tidak bisa langsung di-append)
- Safe read pattern: guard clause `exists()` dikombinasikan dengan `try-except JSONDecodeError`
- `isinstance()` untuk validasi tipe data sebelum diproses
- `default=converter` untuk serialisasi tipe non-native JSON (`datetime`, `Path`)

### Capstone — TradeDesk CLI
- Integrasi seluruh skill Phase 2 dalam satu tool modular (main, wallet, validator, storage, logger)
- Fondasi langsung untuk `memory/trade_journal.py` dan `data/exports/` di arsitektur final

---

## Key Learnings — File & Data

- `write_text()` selalu overwrite; append tetap wajib pakai `open("a")`
- `Path()` hanya diperlukan kalau input masih berupa string biasa
- JSON tidak bisa di-append langsung — alur wajib: load → edit dict → dump ulang dengan `"w"`
- `isinstance()` untuk mengecek tipe variabel sebelum diproses lebih lanjut

## Key Learnings — Python Patterns

- `logger.info()` tidak menerima banyak argumen seperti `print()` dengan koma — harus pakai f-string
- `Path.home()` dan `Path.cwd()` adalah best practice untuk portabilitas GitHub, supaya username/path lokal tidak ter-hardcode
- Mutable objects (list) bisa dimodifikasi in-place di dalam fungsi tanpa `return`/`global`; immutable (int/str) tidak bisa
- `random.random()` menghasilkan float 0.0–1.0, bukan 0–100 — sering disalahpahami pemula
- Urutan multiple except: dari yang paling spesifik ke paling general
- `raise` tanpa argumen (re-raise) berbeda dari `raise ValueError("pesan")` custom

## Key Learnings — Engineering & Belajar

- Modularisasi (banyak file dengan tanggung jawab terpisah: main, validator, storage, logger) mulai dilatih serius di Phase 2 lewat capstone TradeDesk CLI
- Label skala kesulitan (🟢/🟡/🔴/🔴🔴) membantu kalibrasi ekspektasi sebelum masuk materi baru
- Self-debugging: coba dulu sendiri sebelum minta bantuan — pola ini penting dipertahankan karena mempercepat kemampuan trace error secara mandiri

---

## Koneksi ke Roadmap AI Trading Agent

Phase 2 membangun fondasi tooling yang dipakai terus-menerus di semua phase berikutnya:
- **Virtual environment & dependency management** (Day 1) — dasar semua project Python ke depan
- **Version control workflow** (Day 2) — kebiasaan commit/push yang akan terus dipakai
- **`logging`, `pathlib`, `json`** (Day 6, 8, 9) — tiga modul yang paling sering dipakai ulang di Phase 3 dan seterusnya
- **Custom exception & error handling** (Day 7) — pondasi untuk sistem yang robust, relevan langsung ke hard-coded risk guardrails di Phase 8
- **TradeDesk CLI** — cikal bakal `memory/trade_journal.py` dan `data/exports/` di arsitektur final (sekitar 5–8% dari sistem akhir)