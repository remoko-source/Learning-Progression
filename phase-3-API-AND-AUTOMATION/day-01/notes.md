# Day 01 — `requests` & API

## Apa itu `requests`?
Library Python untuk mengirim HTTP request ke server.
Tanpa library ini, kamu harus tulis koneksi internet
dari nol — sangat rumit. `requests` menyederhanakan
semua itu jadi satu baris.

```python
import requests
response = requests.get(url)
```

---

## Client & Server

- **Client** → yang minta data (program Python kamu)
- **Server** → yang punya data (CoinGecko, dll)
- Komunikasi terjadi lewat **HTTP Request**

Analogi: client = pelanggan, server = warung,
HTTP = cara memesan.

---

## Anatomi URL

```
https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd
│                        │                   │
protokol                 endpoint            parameter
```

- **Endpoint** → pintu/menu yang dituju di server
- **Parameter** → spesifikasi permintaan (coin apa, mata uang apa)
- Parameter dimulai dengan `?`, dipisah dengan `&`

---

## Flow Lengkap

```
Program Python
      ↓
requests.get(url)
      ↓
HTTP Request dikirim ke server
      ↓
Server proses
      ↓
Response balik (status code + JSON)
      ↓
Kamu baca & tampilkan
```

---

## Status Code

```
2xx → Sukses
4xx → Salah dari sisi client (kamu)
5xx → Salah dari sisi server
```

Yang paling sering ditemui:
- `200` → OK
- `404` → tidak ditemukan
- `429` → rate limit (terlalu banyak request)
- `500` → server crash
- `503` → server down

---

## Method Penting

```python
response = requests.get(url)

response.status_code        # cek status (200, 404, dll)
response.json()             # ambil isi response sebagai dict
response.raise_for_status() # lempar HTTPError jika 4xx/5xx
```

**Penting:** `raise_for_status()` WAJIB dipasang tepat
setelah `requests.get()` — tanpa ini, HTTPError
tidak akan pernah ter-trigger meski status code error.

---

## Error Handling

```python
except requests.exceptions.ConnectionError:
    # tidak ada koneksi internet

except requests.exceptions.Timeout:
    # koneksi ada tapi server tidak merespons

except requests.exceptions.InvalidURL:
    # format URL tidak valid

except requests.exceptions.HTTPError as e:
    # status code 4xx atau 5xx
    # pakai as e untuk tangkap detail errornya
    if response.status_code >= 500:
        logger.critical("FATAL — server error")
    else:
        logger.error("HTTP Error")
```

Urutan: spesifik → general (sama seperti Phase 2)

---

## String Formatting Baru

```python
# Padding — rata kiri, total N karakter
f"{key:<10}"        # "bitcoin   "

# Pemisah ribuan
f"{67500:,}"        # "67,500"
f"{1089450000:,}"   # "1,089,450,000"

# Gabungan
f"{key:<10}: ${value['usd']:,}"
```

**Tips:** Kalau f-string terlalu panjang, pecah ke variabel dulu:
```python
usd = f"${value['usd']:,}"
idr = f"Rp{value['idr']:,}"
print(f"{key:<10}: {usd:<15} | {idr}")
```

---

## List Comprehension + strip()

```python
# Masalah: input user mungkin ada spasi
# "bitcoin, ethereum" → ["bitcoin", " ethereum"] ← spasi!

# Solusi:
coins = [c.strip() for c in coins.split(",")]
# hasil: ["bitcoin", "ethereum"]
```

- `strip()` → hapus spasi di kiri dan kanan string
- List comprehension → loop + transform dalam satu baris

---

## Mp-01: Crypto Price Checker

**Fitur:**
- Input nama coin dari user (bisa multiple, pisah koma)
- Fetch harga USD + IDR dari CoinGecko API
- Tampilkan dengan formatting rapi + padding
- Full error handling (Connection, Timeout, InvalidURL, HTTP)
- Logging ke `Mp.log` — INFO untuk sukses, ERROR/CRITICAL untuk gagal
- `.lower()` di input supaya user bisa ketik huruf besar

**Hal yang ditemukan:**
- `raise_for_status()` wajib ada untuk trigger HTTPError
- 5xx = fatal, tidak bisa di-handle dari sisi client
- Nama coin harus pakai ID resmi CoinGecko, bukan ticker