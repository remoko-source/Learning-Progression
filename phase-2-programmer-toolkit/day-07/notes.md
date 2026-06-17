# Day 7 Bonus — `random` Module
**Tanggal:** 17 Juni 2026

---

## 5 Fungsi Utama

### 1. `random.randint(a, b)`
- Menghasilkan **integer acak** antara `a` dan `b` (keduanya inklusif)
- Contoh: `random.randint(1, 10)` → bisa keluar 1 sampai 10

### 2. `random.choice(list)`
- Memilih **1 item acak** dari sebuah list
- List harus dibuat dulu sebelum dipakai
- Contoh: `random.choice(["BTC", "ETH", "SOL"])` → salah satu dari ketiganya

### 3. `random.random()`
- Menghasilkan **float acak antara 0.0 sampai 1.0** (tidak mungkin menyentuh 1.0)
- Berguna untuk **simulasi probabilitas/chance**
- Contoh: `if random.random() < 0.3:` → 30% kemungkinan terjadi

### 4. `random.uniform(a, b)`
- Menghasilkan **float acak** antara `a` dan `b` (custom range)
- Cocok untuk simulasi harga (desimal, bukan bulat)
- Contoh: `random.uniform(60000, 70000)` → harga BTC simulasi

### 5. `random.shuffle(list)`
- **Mengacak urutan list secara in-place** (langsung ubah list aslinya)
- Tidak perlu `return` atau `global` — karena list bersifat **mutable**
- Contoh:
```python
deck = ["A", "B", "C"]
random.shuffle(deck)
print(deck)  # urutan sudah acak
```

---

## Konsep Penting: Mutable vs Immutable

| Tipe | Sifat | Efek dalam fungsi |
|---|---|---|
| `list`, `dict` | **Mutable** — isi bisa diubah langsung | `shuffle`, `append`, dll langsung ngaruh ke luar **tanpa return/global** |
| `int`, `str`, `float` | **Immutable** — operasi buat object baru | Perubahan TIDAK ngaruh ke luar, **wajib return** |

---

## pop() vs remove()

```python
data = ["A", "B", "C"]
data.pop(0)      # hapus berdasarkan INDEX → hapus "A"
data.remove("B") # hapus berdasarkan NILAI → hapus "B"
```

---

## Bonus Mp — GACHA Trading Simulator

**Konsep:** Setiap transaksi punya probabilitas berbeda berdasarkan `random.random()`:

| Range | Kondisi | Efek |
|---|---|---|
| < 0.1 | Critical Error | `sys.exit()` |
| 0.1 – 0.2 | System Overload | `time.sleep(5)` |
| 0.2 – 0.4 | Gagal Bayar | `logger.error(...)` |
| > 0.4 | Proses Pembelian | GACHA coin random |
| > 0.4 tapi saldo kurang | `FailedPurchaseError` | raise custom exception |

**Struktur data harga:**
```python
listt = {
    "BTC": (60000, 70000),
    "ETH": (3000, 4000),
    "SOL": (100, 200)
}
# Ambil harga: random.uniform(*listt[coin])
# *listt[coin] = unpack tuple (min, max) jadi 2 argumen
```

**Semua 5 fungsi random terpakai:**
- `randint` → saldo awal acak
- `random` → luck check probabilitas
- `choice` → pilih coin acak
- `uniform` → harga coin acak
- `shuffle` → acak urutan customer

---

## Catatan

- `random.random()` menghasilkan 0.0–1.0, **bukan 0–100** — jangan salah tulis kondisi `if nilai > 51`
- `import random` cukup sekali di atas file
- `round(nilai, 2)` → bulatkan float ke 2 desimal (built-in, bukan dari `random`)
-