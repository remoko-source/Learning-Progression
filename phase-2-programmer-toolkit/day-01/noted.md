# Phase 2 — Day 1: Virtual Environment & Pip

## Yang Dipelajari Hari Ini

### Navigasi Terminal
| Perintah | Fungsi |
|---|---|
| `cd nama-folder` | masuk ke folder |
| `ls` | lihat isi folder |

### Virtual Environment
Virtual environment = inventory isolasi per project.
Library yang diinstall di satu venv tidak akan ganggu project lain.

| Perintah | Fungsi |
|---|---|
| `python -m venv venv` | buat virtual environment |
| `source venv/Scripts/activate` | aktifkan venv |
| `deactivate` | keluar dari venv |

### Pip
Pip = robot rumah tangga yang belanja library sesuai perintah.

| Perintah | Fungsi |
|---|---|
| `pip install nama-library` | install library baru |
| `pip list` | lihat semua library yang terinstall |
| `pip freeze > requirements.txt` | simpan daftar library ke file |
| `pip install -r requirements.txt` | install semua library dari daftar |

### Requirements.txt
- Isinya = daftar belanja library project
- Fungsinya = orang lain bisa replikasi environment yang sama dengan satu perintah
- Wajib diupdate setiap kali install library baru

---

## Alur Kerja Standar (Setiap Mulai Project Baru)

1. Buat folder project
2. Masuk ke folder — `cd nama-folder`
3. Buat venv — `python -m venv venv`
4. Aktifkan venv — `source venv/Scripts/activate`
5. Install library yang dibutuhkan — `pip install nama-library`
6. Simpan daftar library — `pip freeze > requirements.txt`
7. Selesai kerja — `deactivate`

---

## Library yang Diinstall Hari Ini

| Library | Fungsi |
|---|---|
| `requests` | komunikasi dengan internet & API |

---

*Phase 2 — Day 1 selesai.*
