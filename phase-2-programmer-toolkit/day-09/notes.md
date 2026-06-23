# Day 9 — JSON Module advanced

## 4 Fungsi Utama

| Fungsi | Arah | Sumber/Target |
|---|---|---|
| `json.load()` | JSON → dict | File |
| `json.loads()` | JSON → dict | String |
| `json.dump()` | dict → JSON | File |
| `json.dumps()` | dict → string | String |

**Trik hapalan:** huruf `s` di ujung = string.

---

## Parameter Penting

```python
json.dump(data, file, indent=4, ensure_ascii=False, default=converter)
```

- `indent=4` → output JSON rapi, tidak satu baris
- `ensure_ascii=False` → karakter non-ASCII (huruf Indonesia, dll) tidak jadi kode unicode aneh
- `default=converter` → handle tipe yang tidak bisa di-serialize JSON (datetime, Path, dll)

---

## Safe Read Pattern

```python
def baca_json(path):
    if not Path(path).exists():
        return {}  # guard clause — file belum ada
    with open(path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}  # file ada tapi corrupt
```

Kombinasi guard clause + try-except untuk dua kasus berbeda.

---

## default=converter

JSON tidak bisa serialize semua tipe Python. Contoh: `datetime`, `Path`.

```python
def converter(obj):
    if isinstance(obj, datetime):
        return obj.strftime("%d/%m/%Y %H:%M:%S")
    elif isinstance(obj, Path):
        return str(obj)
```

- `default=converter` → serahkan fungsi, bukan panggil fungsi (`default=converter` bukan `default=converter()`)
- Dipanggil otomatis oleh `json.dumps`/`json.dump` kalau ketemu tipe yang tidak dikenal
- Bisa handle banyak tipe sekaligus dengan `elif`

---

## isinstance()

```python
isinstance(obj, datetime)  # True/False — cek tipe variabel
isinstance(42, int)        # True
isinstance("halo", str)    # True
```

---

## json.JSONDecodeError

Muncul kalau string/file JSON-nya tidak valid (format salah, corrupt, dll).

```python
try:
    data = json.loads(raw)
except json.JSONDecodeError as e:
    print(f"JSON tidak valid: {e}")
```

Berbeda dengan `FileNotFoundError` — itu untuk file yang tidak ada.

---

## Alur Standar Update File JSON

```
baca file (json.load) → dapat dict lama
update dict di Python
tulis ulang dengan "w" (json.dump)
```

**JSON tidak bisa di-append langsung** dengan `open("a")` — file akan corrupt.

---

## raise vs raise ValueError()

```python
raise                      # lempar ulang exception yang sama ke pemanggil
raise ValueError("pesan")  # buat exception baru dengan pesan custom
```

`raise` tanpa argumen hanya valid di dalam fungsi yang ada pemanggil di atasnya.

---

## Mini Project — Mp-09: JSON Converter CLI

**File:** `Mp-09.py`  
**Fitur:**
- Input coin normal → simpan ke `Test.json` dengan update pattern
- Input string JSON manual (format mode) → parse dengan `loads` → simpan
- LOOK mode → tampilkan semua data rapi
- Logging ke `TESTING.log`
- `converter` untuk datetime
- Safe read pattern