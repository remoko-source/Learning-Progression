# Phase 5 Day 1 — Data-to-Text Translation

## Tujuan Hari Ini
Mengubah data harga mentah (angka time-series) menjadi narasi teks yang bisa dipahami LLM sebagai konteks — karena LLM tidak bisa langsung "mengerti" deretan angka tanpa penjelasan.

## Materi yang Dipelajari

### 1. DataFrame (pandas)
- Struktur tabel di Python — bisa dibuat dari dictionary biasa (`{"close": [list]}`) atau list of dictionaries (`[{"coins":..., "harga":...}, ...]`)
- Index otomatis mulai dari 0 (RangeIndex), bisa dikustom pakai parameter `index=`
- Untuk data time-series, index idealnya pakai tanggal/waktu asli, bukan angka urutan

### 2. Moving Average (MA)
- Konsep: rata-rata harga bergeser (rolling), meratakan fluktuasi harga biar kelihatan arah trennya
- Implementasi: `df["close"].rolling(window=N).mean()`
- Baris pertama sebanyak (N-1) akan bernilai `NaN` karena data belum cukup untuk mengisi jendela

### 3. RSI (Relative Strength Index) — dihitung manual
Karena `pandas-ta` tidak kompatibel dengan Python 3.10 (butuh Python 3.12+), RSI dihitung manual pakai pandas murni:

1. `df["change"] = df["close"].diff()` — selisih harga vs hari sebelumnya
2. Pisah gain & loss pakai `.where()`:
   ```python
   df["gain"] = df["change"].where(df["change"] > 0, 0)
   df["loss"] = -df["change"].where(df["change"] < 0, 0)
   ```
3. Rolling average dari gain & loss (window = periode, standar 14)
4. RS = avg_gain / avg_loss
5. RSI = `100 - (100 / (1 + RS))`

**Insight penting:** kalau avg_loss mendekati 0 (harga naik terus), RS mendekati infinity, dan RSI mendekati 100 — bukan error, itu representasi matematis dari kondisi "extreme overbought".

**Insight lain:** konsep rolling window itu universal — window yang dipelajari di MA berlaku sama persis di RSI, karena keduanya sama-sama pakai `.rolling()`.

### 4. Data-to-Text Translation
Mengubah angka indikator jadi kalimat, memakai logic if-elif-else (mirip pola threshold di Phase 3-4):
- RSI ≥ 70 → "overbought", RSI ≤ 30 → "oversold", selain itu → "netral"
- Harga di atas MA → "tren naik", di bawah → "tren turun"

## Kendala yang Ditemukan & Solusi

**Masalah:** `pandas-ta` gagal diinstall di Python 3.10 (butuh Python 3.12+), versi lama pun sudah tidak tersedia di PyPI.

**Solusi:** hitung RSI & MA manual pakai pandas polos. Ini dipilih dengan sadar (bukan cuma solusi darurat) karena:
- Fondasi lebih kuat — paham cara kerja indikator, bukan cuma manggil fungsi jadi
- Menghindari dependency rapuh (proyek `pandas-ta` asli sempat terancam diarsipkan)
- Sesuai prinsip roadmap: "jangan pakai abstraksi yang belum dipahami"

## Mini Project: Mp-01 — Market Narrator

Struktur akhir:
- `analisis(data, N, M)` — hitung MA dan RSI, return DataFrame
- `narasi_rsi(rsi_akhir)` — ubah angka RSI jadi teks kondisi
- `narasi_MA(MA_akhir, harga_akhir, N)` — ubah perbandingan harga vs MA jadi teks tren
- `buat_laporan(data, nama_coin, config)` — gabungkan semua jadi satu paragraf narasi utuh

Fitur tambahan yang dikembangkan sendiri (di luar requirement awal):
- `config` dict (`MA_PERIOD`, `RSI_PERIOD`) — periode indikator bisa diatur dari luar, tidak hardcode
- Struktur data nested (`data["coins"]["bitcoin"]["close"]`) — mendekati bentuk data asli dari CoinGecko nantinya
- Format output multi-line dengan separator visual per coin

Berhasil menghasilkan laporan untuk 2 coin (BITCOIN, ETHEREUM) dengan data dummy 20 titik harga masing-masing.

## Status
Phase 5 Day 1 — **SELESAI**# Phase 5 Day 1 — Data-to-Text Translation

## Tujuan Hari Ini
Mengubah data harga mentah (angka time-series) menjadi narasi teks yang bisa dipahami LLM sebagai konteks — karena LLM tidak bisa langsung "mengerti" deretan angka tanpa penjelasan.

## Materi yang Dipelajari

### 1. DataFrame (pandas)
- Struktur tabel di Python — bisa dibuat dari dictionary biasa (`{"close": [list]}`) atau list of dictionaries (`[{"coins":..., "harga":...}, ...]`)
- Index otomatis mulai dari 0 (RangeIndex), bisa dikustom pakai parameter `index=`
- Untuk data time-series, index idealnya pakai tanggal/waktu asli, bukan angka urutan

### 2. Moving Average (MA)
- Konsep: rata-rata harga bergeser (rolling), meratakan fluktuasi harga biar kelihatan arah trennya
- Implementasi: `df["close"].rolling(window=N).mean()`
- Baris pertama sebanyak (N-1) akan bernilai `NaN` karena data belum cukup untuk mengisi jendela

### 3. RSI (Relative Strength Index) — dihitung manual
Karena `pandas-ta` tidak kompatibel dengan Python 3.10 (butuh Python 3.12+), RSI dihitung manual pakai pandas murni:

1. `df["change"] = df["close"].diff()` — selisih harga vs hari sebelumnya
2. Pisah gain & loss pakai `.where()`:
   ```python
   df["gain"] = df["change"].where(df["change"] > 0, 0)
   df["loss"] = -df["change"].where(df["change"] < 0, 0)
   ```
3. Rolling average dari gain & loss (window = periode, standar 14)
4. RS = avg_gain / avg_loss
5. RSI = `100 - (100 / (1 + RS))`

**Insight penting:** kalau avg_loss mendekati 0 (harga naik terus), RS mendekati infinity, dan RSI mendekati 100 — bukan error, itu representasi matematis dari kondisi "extreme overbought".

**Insight lain:** konsep rolling window itu universal — window yang dipelajari di MA berlaku sama persis di RSI, karena keduanya sama-sama pakai `.rolling()`.

### 4. Data-to-Text Translation
Mengubah angka indikator jadi kalimat, memakai logic if-elif-else (mirip pola threshold di Phase 3-4):
- RSI ≥ 70 → "overbought", RSI ≤ 30 → "oversold", selain itu → "netral"
- Harga di atas MA → "tren naik", di bawah → "tren turun"

## Kendala yang Ditemukan & Solusi

**Masalah:** `pandas-ta` gagal diinstall di Python 3.10 (butuh Python 3.12+), versi lama pun sudah tidak tersedia di PyPI.

**Solusi:** hitung RSI & MA manual pakai pandas polos. Ini dipilih dengan sadar (bukan cuma solusi darurat) karena:
- Fondasi lebih kuat — paham cara kerja indikator, bukan cuma manggil fungsi jadi
- Menghindari dependency rapuh (proyek `pandas-ta` asli sempat terancam diarsipkan)
- Sesuai prinsip roadmap: "jangan pakai abstraksi yang belum dipahami"

## Mini Project: Mp-01 — Market Narrator

Struktur akhir:
- `analisis(data, N, M)` — hitung MA dan RSI, return DataFrame
- `narasi_rsi(rsi_akhir)` — ubah angka RSI jadi teks kondisi
- `narasi_MA(MA_akhir, harga_akhir, N)` — ubah perbandingan harga vs MA jadi teks tren
- `buat_laporan(data, nama_coin, config)` — gabungkan semua jadi satu paragraf narasi utuh

Fitur tambahan yang dikembangkan sendiri (di luar requirement awal):
- `config` dict (`MA_PERIOD`, `RSI_PERIOD`) — periode indikator bisa diatur dari luar, tidak hardcode
- Struktur data nested (`data["coins"]["bitcoin"]["close"]`) — mendekati bentuk data asli dari CoinGecko nantinya
- Format output multi-line dengan separator visual per coin

Berhasil menghasilkan laporan untuk 2 coin (BITCOIN, ETHEREUM) dengan data dummy 20 titik harga masing-masing.

## Status
Phase 5 Day 1 — **SELESAI**