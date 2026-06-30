# Day 4 — Multi-Coin Price Tracker

**Phase:** 3 — API & Automation
**File:** `Mp-04.py`
**Folder:** `phase-3-api/day-04/`

---

## Tujuan Project

Tracking harga beberapa coin sekaligus (BTC, ETH, SOL) dalam satu sistem yang:
- Fetch banyak coin dalam satu API call
- Hitung perubahan harga (%) dari baseline awal program dijalankan
- Tampilkan hasil dalam tabel rapi di terminal
- Bunyi alert tiap cycle refresh
- Auto-stop setelah durasi tertentu

---

## Materi Baru

### 1. `tabulate` — Tabel Rapi di Terminal

Dua cara input data ke `tabulate`:

**List of list** (urutan kolom manual via index):
```python
data = [["Bitcoin", 67000, "+2.5%"]]
headers = ["Coin", "Price", "Change"]
tabulate(data, headers=headers, tablefmt="grid")
```

**List of dict** (kolom otomatis dari key):
```python
data = [{"Coin": "Bitcoin", "Price": 67000, "Change": "+2.5%"}]
tabulate(data, headers="keys", tablefmt="grid")
```

Tradeoff: list of dict lebih aman & self-describing (cocok untuk data dari API/JSON), list of list lebih cepat ditulis untuk data statis kecil.

### 2. Snapshot Harga Awal (Baseline Tetap — Versi A)

Dua pendekatan hitung % change:
- **Versi A (dipilih):** baseline disimpan sekali di awal program, tidak berubah → "perubahan sejak mulai mantau"
- **Versi B:** baseline di-update tiap cycle (rolling) → "perubahan per interval terakhir"

Versi A dipilih karena lebih sesuai nama project ("Tracker") dan lebih simpel untuk dikuasai dulu sebagai fondasi. Versi B lebih relevan untuk scalping real (momentum jangka pendek) — kemungkinan dipakai nanti di Mini Market Scanner atau Phase 8.

Rumus:
```python
persen = ((harga_sekarang - harga_awal) / harga_awal) * 100
```

### 3. Fetch Multiple Coins dalam Satu Request

```python
coins = ["bitcoin", "ethereum", "solana"]
ids_param = ",".join(coins)
url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids_param}&vs_currencies=usd"
```

Kenapa penting: hemat rate limit (CoinGecko cuma kasih 5-15 calls/menit), lebih cepat, lebih simpel handle error dibanding fetch satu-satu per coin. Prinsip ini disebut **batching**.

---

## Key Learnings Tambahan

- **`list.copy()` itu shallow copy** — list baru, tapi dictionary di dalamnya masih objek yang sama dengan list asli. Modifikasi dictionary di copy-an ikut merusak data asli.
- **`copy.deepcopy()`** — copy independen sampai ke dalam-dalamnya, dipakai supaya tabel "tampilan bersih" (tanpa kolom `Harga_awal`) tidak merusak data `lol` asli yang masih dibutuhkan untuk kalkulasi berikutnya.
- **`dict.pop("key_name")`** beda dengan `list.pop(index)` — dictionary minta nama key (string), list minta posisi (index angka). Salah pakai bikin `KeyError` atau hasil yang nggak sesuai.
- **`floatfmt` di tabulate bisa tuple per-kolom**, misal `(".2f", "g")` — supaya kolom dengan skala beda (harga besar vs persen kecil) sama-sama kebaca presisinya. Jumlah elemen tuple harus cocok jumlah kolom yang di-print.
- **`colalign` & `numalign`** — atur alignment kolom (`"left"/"right"/"center"`), supaya tabel lebih enak dibaca (nama rata kiri, angka rata kanan).
- **`raise_for_status()` harus dipanggil sebelum `.json()`** — kalau kebalik, `response` udah ketiban jadi dictionary biasa (bukan objek `Response` lagi), jadi manggil `.raise_for_status()` di atas dictionary bakal lempar `AttributeError`, error yang nggak ketangkep sama except `requests.exceptions.*` manapun.

---

## Bug yang Ditemukan & Diperbaiki

1. **% change belum dikali 100** — hasil kalkulasi awal masih desimal mentah (`0.0001966...`), bukan persen beneran. Sudah difix dengan `* 100`.
2. **`raise_for_status()` dipanggil setelah `.json()`** — urutan salah, bikin error nggak ketangkep except manapun. Sudah difix dengan menukar urutan: `raise_for_status()` dulu, baru `.json()`.

## Known Issue (Belum Diperbaiki — Keputusan Sadar)

- Tabel versi "bersih" (3 kolom, tanpa `Harga_awal`) cuma jalan di blok `else` (iterasi pertama/first run). Iterasi kedua dan seterusnya (`if i > 1`) masih nge-print `lol` mentah dengan 4 kolom (termasuk `Harga_awal`). Akibatnya format tabel berubah-ubah jumlah kolomnya antar iterasi. Sudah disadari, sengaja belum difix — alasan: aneh kalau `Harga_awal` dan `Harga` ditampilkan sama persis di iterasi pertama.

---

## Refleksi

Project ini paling kompleks sejauh ini di Phase 3 — gabungan state tracking, multi-coin handling, dan custom table formatting dalam satu sistem yang jalan terus-menerus (`while True`). Berhasil nemu & fix dua bug penting secara mandiri (kalkulasi persen, urutan `raise_for_status`), dan paham bedanya shallow copy vs deep copy dari pengalaman langsung kena bug-nya.

**Next:** sebelum lanjut ke capstone Phase 3 (Mini Market Scanner), ada 2 materi tambahan dulu — Retry Logic & Resilience (Day 5), dan Config Eksternal & Credential Handling (Day 6). Dua ini ngisi gap "Automation" yang belum kesentuh dari Day 1-4 (program saat ini belum bisa retry otomatis kalau gagal, dan semua setting masih hardcoded di source code).