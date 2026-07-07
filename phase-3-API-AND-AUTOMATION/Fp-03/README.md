# Mini Market Scanner — Setup & Requirements

Capstone Phase 3: AI Trading Agent Roadmap v2.1

---

## Requirements

Buat file `requirements.txt` di folder project (`Fp-03/`), isinya:

```
requests
python-dotenv
tabulate
```

**Kenapa cuma 3 library ini yang perlu ditulis** — bukan semua yang di-`import` di kode kamu:

| Library di-import | Perlu di requirements.txt? | Kenapa |
|---|---|---|
| `requests` | ✅ Ya | Bukan bawaan Python, wajib di-install |
| `python-dotenv` | ✅ Ya | Bukan bawaan Python, wajib di-install |
| `tabulate` | ✅ Ya | Bukan bawaan Python, wajib di-install |
| `os`, `sys`, `time`, `json`, `copy`, `logging` | ❌ Tidak | **Built-in module** — sudah ikut Python, tidak perlu install apapun |
| `winsound` | ❌ Tidak | Built-in juga, tapi **khusus Windows** (tidak akan jalan di Linux/Mac) |
| `pathlib` | ❌ Tidak | Built-in sejak Python 3.4 |

**Analogi:** `requirements.txt` itu kayak daftar belanja — cuma barang yang **belum ada di rumah** yang perlu ditulis. Built-in module itu udah "ada di rumah" (ikut paket instalasi Python), jadi gak perlu dibeli lagi.

---

## Cara Install (Windows 8, Git Bash)

```bash
pip install -r requirements.txt
```

Kalau nanti pindah laptop atau kolaborasi sama Fardan, dia tinggal jalanin baris ini — semua dependency ke-install otomatis tanpa perlu install satu-satu manual.

## Cara Generate Otomatis (kalau environment sudah jalan lancar)

```bash
pip freeze > requirements.txt
```

**Catatan penting kalau pakai `pip freeze`:** perintah ini nge-dump SEMUA package yang ke-install di environment kamu, termasuk dependency dari dependency (misal `requests` butuh `urllib3`, `charset-normalizer`, dll). Itu normal dan aman — tapi kalau kamu mau versi yang lebih bersih/minimal (cuma yang kamu import langsung), lebih baik tulis manual seperti daftar di atas.

---

## Catatan Kompatibilitas Windows 8

`winsound` di `main.py` kamu **hanya jalan di Windows**. Ini bukan masalah sekarang (karena kamu di Windows 8), tapi jadi catatan penting untuk masa depan:

- Kalau nanti project ini pindah ke Linux (Phase 9 — Deployment & Linux, atau kalau pakai server VPS), baris `winsound.Beep(...)` akan **error** karena modul itu gak ada di Linux
- Solusi jangka panjang (belum perlu sekarang): bungkus pemanggilan `winsound` dengan pengecekan OS, atau ganti ke library cross-platform kalau notifikasi suara masih dibutuhkan setelah deployment

Untuk sekarang, gak perlu diubah — ini baru jadi relevan pas masuk Phase 9.

---

*README ini dibuat untuk dokumentasi setup capstone Phase 3 — Mini Market Scanner.*