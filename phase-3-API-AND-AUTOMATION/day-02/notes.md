# Phase 3 — Day 2: Fear & Greed Viewer
**Tanggal:** 2026/06/28

---

## Apa yang dibangun
Fear & Greed Viewer — fetch data sentimen pasar crypto 7 hari terakhir dari API `alternative.me`, tampilkan dalam format tabel terminal, hitung rata-rata, dan beri kesimpulan FEAR/GREED.

---

## Konsep Baru

### 1. Unix Timestamp
- Angka bulat yang merepresentasikan **jumlah detik sejak 1 Januari 1970 00:00:00**
- Dipakai secara universal di sistem dan API sebagai format waktu standar
- Konversi ke tanggal readable:
```python
from datetime import datetime
datetime.fromtimestamp(int(unix_string)).strftime("%Y/%m/%d")
```
- Perlu `int()` karena nilai dari API datang sebagai **string**

---

### 2. Akses Nested List + Dict
- API bisa return data dalam bentuk **list of dict**
- Struktur response `alternative.me/fng/`:
```python
{
  'name': 'Fear and Greed Index',
  'data': [          # ← LIST
    {
      'value': '18',
      'value_classification': 'Extreme Fear',
      'timestamp': '1782604800',
      'time_until_update': '37852'
    },
    ...
  ]
}
```
- Kenapa list? Supaya API bisa return lebih dari 1 hari (`?limit=7`)
- Akses elemen pertama: `data['data'][0]`
- Iterate semua: `for i in data['data']:`

---

### 3. Query Parameter di URL
- Tambahkan parameter langsung di URL dengan `?key=value`
- Contoh: `https://api.alternative.me/fng/?limit=7`
- Slash sebelum `?` penting — tanpa slash bisa error atau redirect

---

### 4. `enumerate()` untuk iterasi dengan index
```python
for index, i in enumerate(data['data']):
    if index == 0:
        # hari ini — tampilkan UPDATE time
    else:
        # hari sebelumnya
```
- `enumerate()` return tuple `(index, value)` saat iterasi
- Berguna untuk perlakuan berbeda pada elemen pertama

---

### 5. Akumulasi nilai dalam loop
```python
sebelum = 0
for i in data['data']:
    sebelum += int(i['value'])
rata_rata = sebelum / len(data['data'])
```
- Inisialisasi variabel akumulator **sebelum** loop
- Gunakan `len(data['data'])` bukan `len(i)` — `i` adalah dict elemen terakhir, panjangnya = jumlah keys, bukan jumlah iterasi

---

## Bug yang ditemukan dan diperbaiki
- **`rata_rata = sebelum / len(i)`** → SALAH
  - `i` setelah loop = dict elemen terakhir, `len(i)` = 4 (jumlah keys)
  - Kebetulan output keliatan masuk akal tapi matematikanya salah
- **Fix:** `rata_rata = sebelum / len(data['data'])` → benar, = 7

---

## Clarifikasi Penting
- **`InvalidURL`** = format URL rusak total (kosong, malformed)
- **`ConnectionError`** = URL format valid tapi domain tidak ditemukan (DNS failed)
- Urutan except tetap: spesifik → general
- `value` dan `timestamp` dari API selalu datang sebagai **string** → selalu konversi dengan `int()` sebelum dipakai sebagai angka

---

## Konsep yang dikonfirmasi ulang
- `value_classification` sudah disediakan API — tidak perlu kondisional manual berdasarkan angka
- Untuk emoji tetap butuh kondisional berdasarkan `value_classification` (API tidak sediakan emoji)
- Windows 8 CMD dan PowerShell 2014 tidak support emoji — gunakan teks biasa `[EXTREME FEAR]` dll

---

## Output Program
```
--------------------------------------------------
Fear and Greed Index
==================================================
2026/06/28 | 18 | Extreme Fear | UPDATE: 15:49:04
--------------------------------------------------
2026/06/27 | 15 | Extreme Fear
2026/06/26 | 13 | Extreme Fear
2026/06/25 | 12 | Extreme Fear
2026/06/24 | 17 | Extreme Fear
2026/06/23 | 23 | Extreme Fear
2026/06/22 | 20 | Extreme Fear
--------------------------------------------------
RATA RATA:  17
PASAR 7 Hari Terakhir Dominan  FEAR
==================================================
```

---

## File
- `Mp-02.py` — Fear & Greed Viewer
- `Mp.log` — log program
- `latihan.py` — latihan nested dict dan unix timestamp
-