TradeDesk CLI

«Aplikasi jurnal trading berbasis terminal yang dibangun menggunakan Python murni — tanpa library eksternal.»

---

Tentang Project

TradeDesk CLI adalah final project dari Phase 2 learning journey saya.

Project ini mensimulasikan sistem pencatatan dan manajemen trade sederhana lengkap dengan validasi input, logging aktivitas, penyimpanan data JSON, dan update hasil trading.

Semua berjalan langsung melalui terminal menggunakan Python standard library tanpa dependency tambahan.

Project ini dibuat sebagai bukti penguasaan konsep Python intermediate dan software engineering dasar sebelum masuk ke fase API dan automation.

---

Fitur

- Menambahkan trade baru
- Melihat seluruh riwayat trade
- Update posisi OPEN menjadi WIN atau LOSS
- Perhitungan otomatis profit dan loss
- Validasi input menggunakan custom exception
- Penyimpanan data menggunakan JSON
- Logging aktivitas aplikasi ke file log
- Auto create folder dan file saat pertama kali dijalankan
- Timestamp otomatis untuk setiap transaksi

---

Struktur Project

TradeDesk/
├── main.py          # Entry point & menu utama aplikasi
├── storage.py       # Load, save, add, dan update trade
├── validator.py     # Validasi input dan custom exception
├── logger.py        # Konfigurasi logging aplikasi
├── scanner.py       # Bootstrap folder dan file project
│
├── data/
│   └── trades.json  # Database trade berbasis JSON
│
└── logs/
    └── tradedesk.log # Aktivitas aplikasi

---

Konsep Python yang Dipelajari

Konsep| Implementasi
Function| "add()", "view()", "update()"
Import antar file| Pemisahan logic ke beberapa module
Modular programming| "storage", "validator", "logger", "scanner"
"pathlib"| Manajemen path lintas sistem operasi
JSON read/write| "json.load()" dan "json.dump()"
Logging| "FileHandler", "Formatter", "logger.info()"
Custom Exception| "InvalidCoinError", "InvalidStatusError", dll
Inheritance| Semua error mewarisi "TradeValidationError"
"try-except"| Penanganan error input user
"raise"| Melempar exception dari validator
"datetime"| Timestamp otomatis trade
"while True"| Loop menu utama dan validasi input
"break" dan "continue"| Kontrol alur program
Dictionary| Penyimpanan data trade
List of Dictionary| Database JSON sederhana
Guard Clause| Validasi ID dan kondisi trade
Separation of Concerns| Tiap file memiliki tanggung jawab masing-masing

---

Modul Standard Library yang Digunakan

"pathlib"

Digunakan untuk manajemen path file dan folder agar kompatibel lintas OS.

"json"

Digunakan untuk penyimpanan data trade secara permanen.

"logging"

Digunakan untuk mencatat aktivitas penting aplikasi.

"datetime"

Digunakan untuk mencatat waktu setiap transaksi dilakukan.

"os"

Digunakan untuk membersihkan terminal ("cls").

"sys"

Digunakan untuk keluar dari program secara bersih menggunakan "sys.exit()".

"time"

Digunakan untuk memberikan delay pada antarmuka terminal.

---

Konsep Software Engineering

- Separation of Concerns
- Modular Project Structure
- Layered Architecture sederhana
- Validation Layer
- Storage Layer
- Logging Layer
- Bootstrap Scanner
- Error Handling Strategy
- Custom Exception Hierarchy

---

Keputusan Engineering

- Input hanya dilakukan pada "main.py"
- "storage.py" hanya bertugas membaca dan menulis data
- "validator.py" hanya bertugas melakukan validasi
- "logger.py" hanya menangani aktivitas penting aplikasi
- Error validasi tidak langsung menghentikan program
- Semua file dan folder dibuat otomatis saat startup aplikasi

---

Tech Stack

- Language: Python 3
- Storage: JSON Flat File
- Logging: Python Logging Module
- Interface: Terminal / CLI
- Dependency: Tidak ada (Standard Library Only)

---

Cara Menjalankan

python main.py

Tidak membutuhkan dependency tambahan.

Cukup install Python 3 dan jalankan program.

---

Learning Journey Status

✅ Phase 1 — Selesai
✅ Phase 2 — Selesai
🔜 Phase 3 — API, Request, Live Data & Automation

---

Author

Remoko-source
GitHub: github.com/Remoko-source

«Dibangun sebagai bagian dari learning journey menuju AI Trading Agent System.»