# Day 8 — `pathlib` Module

## Apa itu `pathlib`?
Versi modern dari `os.path`. Bedanya, `pathlib` berbasis **object** — bukan sekedar string yang diproses fungsi.

```python
from pathlib import Path

p = Path("folder/subfolder/file.txt")  # p adalah object Path
```

---

## Operator `/` — Gabung Path

```python
# Cara lama
os.path.join("Documents", "projects", "data.json")

# pathlib
Path("Documents") / "projects" / "data.json"
```

- Yang paling kiri **harus** object Path, sisanya boleh string biasa
- Kalau path dinamis (dari variable/input), operator `/` lebih clean
- Kalau statis, tulis langsung juga fine — hasilnya sama

```python
base = Path("Documents")
p = base / folder / filename  # dinamis
```

---

## `Path.cwd()` vs `Path.home()`

```python
Path.cwd()   # folder tempat script dijalankan — relatif ke project
Path.home()  # C:/Users/username — folder home user
```

**Best practice:** Jangan hardcode username di path. Pakai `cwd()` atau `home()` biar portable di GitHub.

---

## `.mkdir(parents=True, exist_ok=True)`

```python
p.mkdir(parents=True, exist_ok=True)
```

- `parents=True` → buat semua folder induk yang belum ada
- `exist_ok=True` → kalau sudah ada, skip (tidak error)
- Keduanya hampir selalu dipasang bareng

Kalau path sampai ke **file**, mkdir di parent-nya dulu:
```python
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text("isi")
```

---

## Attribute File

```python
p = Path("Documents/projects/data.json")

p.name    # "data.json"        — nama + ekstensi
p.stem    # "data"             — nama tanpa ekstensi
p.suffix  # ".json"            — ekstensi saja
p.parent  # "Documents/projects" — folder induk
```

**Ingat:** ini **attribute**, bukan method — tidak pakai `()`

---

## Baca & Tulis File

```python
# Buat file baru / overwrite
p.write_text("isi file")

# Baca isi file
isi = p.read_text()

# Tambah tanpa hapus isi lama (append)
with open(p, "a") as f:
    f.write("\nbaris baru")
```

Pattern umum:
- `write_text` → bikin file pertama kali
- `read_text` → baca kapanpun
- `open("a")` → update/tambah data

`write_text` hanya terima **string** — konversi dulu kalau bukan:
```python
p.write_text(str(angka))
p.write_text(f"hasil: {angka}")
p.write_text(json.dumps(data))
```

---

## Cek Keberadaan

```python
p.exists()   # True/False — ada atau tidak
p.is_file()  # True/False — apakah file
p.is_dir()   # True/False — apakah folder
```

**Ingat:** ini **method** — harus pakai `()`

---

## `.iterdir()` & `.glob()`

```python
# List semua isi folder
for item in p.iterdir():
    if item.is_file():
        print(f"FILE: {item.name}")
    elif item.is_dir():
        print(f"FOLDER: {item.name}")

# Filter by ekstensi
for file in folder.glob("*.json"):
    print(file.name)
```

---

## `.stat()` — Info Teknis File

```python
p.stat().st_size   # ukuran dalam bytes
p.stat().st_mtime  # waktu terakhir dimodifikasi (Unix timestamp)
```

Untuk baca waktu:
```python
from datetime import datetime
print(datetime.fromtimestamp(p.stat().st_mtime))
```

---

## Logging — Jangan Pakai Koma

```python
logger.info("File: ", p.name)   # ❌ TypeError
logger.info(f"File: {p.name}")  # ✅
```

`logger` tidak pakai koma seperti `print()`.

---

## Build Path Incrementally (Pattern Bagus)

```python
p = Path.home()

while True:
    mana = input("Masukkan folder (atau 'stop'): ")
    if mana == "stop":
        break
    p = p / mana
```

Daripada hardcode atau pakai index `[0][1]`, build bertahap — lebih fleksibel dan bersih.

---

## Mp-08: PathScout

**Fitur:**
- Terima path via `sys.argv[1]`
- Cek file → tampilkan nama, ekstensi, ukuran, isi
- Cek folder → list semua isi + hitung file & subfolder
- Tidak exist → raise `PathNotFoundError`
- Log semua aktivitas ke `PathScout.log`

**Bug yang ditemukan & difix sendiri:**
1. `PermissionError` → path terbuat sebagai folder, bukan file
2. `logger.info("msg:", var)` → harus f-string
3. `is_file` tanpa `()` → tidak dipanggil, selalu truthy