# CryptoVault

> Aplikasi simulasi trading crypto berbasis terminal yang dibangun dengan Python murni — tanpa library eksternal.

---

## Tentang Project

CryptoVault adalah final project dari Phase 1 learning journey saya.

Project ini mensimulasikan sistem trading crypto sederhana lengkap dengan sistem akun, wallet, dan manajemen portofolio — semua berjalan di terminal.

Dibangun dari nol sebagai bukti penguasaan fondasi Python sebelum masuk ke fase API dan AI automation.

---

## Fitur

- Register & Login akun pengguna
- Deposit dan Withdraw saldo
- Beli dan Jual koin crypto
- Lihat harga koin secara real-time (simulasi)
- Update harga koin manual
- Analisis persentase kenaikan dan penurunan harga

---

## Struktur Project

```
fp-1/
├── main.py        # Entry point & state manager (while loop utama)
├── wallet.py      # Class Wallet — kelola saldo & transaksi
├── crypto.py      # Class Crypto — kelola koin & harga
├── data.json      # Penyimpanan data user & portofolio
└── note.md        # Dokumentasi project
```

---

## Konsep Python yang Dipelajari

| Konsep | Implementasi |
|---|---|
| OOP — Class & Object | `Wallet`, `Crypto` |
| `__init__`, `self`, attribute | Inisialisasi data tiap object |
| Method | `beli()`, `jual()`, `deposit()`, `withdraw()` |
| Inheritance & Enkapsulasi | Struktur class modular |
| Import antar file | `main.py` import `wallet.py` & `crypto.py` |
| Interaksi antar object | Object saling passing lewat parameter |
| JSON read/write | Simpan & load data user |
| try-except | Error handling tiap input |
| while loop | State manager menu utama |
| for-else | Logika pencarian data |
| Global variable | Menyimpan state session login |

---

## Tech Stack

- **Language:** Python 3
- **Storage:** JSON (flat file)
- **Interface:** Terminal / CLI
- **Editor:** Notepad++
- **OS:** Windows 8

---

## Cara Menjalankan

```bash
python main.py
```

Tidak ada dependency eksternal. Cukup Python 3 terinstall.

---

## Status

✅ Phase 1 — Selesai  
🔜 Phase 2 — Programmer Toolkit (GitHub, VS Code, pip, virtual environment)

---

## Author

**Remoko-source**  
GitHub: [github.com/Remoko-source](https://github.com/Remoko-source)

> *Dibangun sebagai bagian dari learning journey menuju AI Trading Agent System.*
