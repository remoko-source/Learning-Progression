 # Phase 3 — Capstone: Mini Market Scanner

**Status:** Selesai (dengan beberapa known issues minor)
**Tanggal:** Juli 2026

---

## Ringkasan Project

Mini Market Scanner adalah integrasi dari seluruh skill Phase 3 (Day 1-6): fetch API dengan retry logic, config eksternal, logging, dan tabulate output — ditambah satu fitur analitik baru: **baseline tracking** untuk deteksi coin yang bergerak signifikan (🔥 MOVER).

Ini adalah versi mini dari komponen `analysis/` di arsitektur final AI Trading Agent — pola "ambil data mentah → bandingkan dengan histori → hasilkan label/sinyal sederhana" yang nanti akan berkembang jauh lebih kompleks di Phase 8.

---

## Struktur Folder

```
phase-3-api/capstone/Fp-03/
├── config.json
├── baseline.json       (auto-generated, persist antar run)
├── data.log             (log file)
├── logger.py
├── fetcher.py
├── baseline_store.py
├── analyzer.py
├── main.py
```

---

## Arsitektur & Alur Program

```
main.py
  ├─→ load_config()          [baseline_store.py]
  ├─→ build_system()
  │     ├─→ load_config()
  │     └─→ fetch_retry()     [fetcher.py]
  └─→ build_table()
        ├─→ load_baseline()   [baseline_store.py] ← baca run sebelumnya
        ├─→ calculate_change()[analyzer.py]
        ├─→ is_mover()        [analyzer.py]
        ├─→ tabulate()        → tampilkan tabel
        └─→ save_baseline()   [baseline_store.py] ← simpan buat run berikutnya
```

**Konsep kunci — Baseline sebagai jembatan waktu:**
Baseline BUKAN untuk membandingkan data dalam satu eksekusi program (itu tugas retry logic). Baseline menjembatani dua *proses program yang terpisah* — harga dari run kemarin (dibaca dari `baseline.json`) dibandingkan dengan harga hari ini (hasil fetch API), lalu di akhir program harga hari ini disimpan lagi jadi baseline run berikutnya.

---

## Fitur per Modul

### `logger.py`
- `get_logger()` — logger dengan 2 handler: `FileHandler` (level INFO ke `data.log`) dan `StreamHandler` (level ERROR ke terminal)
- Library: `logging`

### `fetcher.py`
- `fetch_retry(url, params, max_retries, interval)` — retry dengan exponential backoff, membedakan error permanen (401/403/404 → stop retry) vs sementara (ConnectionError/Timeout/5xx → retry)
- Return `None` kalau semua percobaan gagal (bukan `sys.exit()`) — supaya kegagalan tidak mematikan seluruh program
- Library: `requests`, `time`

### `baseline_store.py`
- `get_paths()` — semua path file (config, storage, logs) pakai `Path(__file__).parent` untuk portabilitas
- `load_config()` — baca `config.json`, exit kalau tidak ditemukan
- `load_baseline()` — baca `baseline.json`; guard `exists()` + `try-except JSONDecodeError` untuk handle file belum ada/kosong
- `save_baseline(data)` — overwrite `baseline.json` dengan data terbaru
- Library: `pathlib`, `json`, `sys`

### `analyzer.py`
- `calculate_change(current, baseline)` — hitung persentase perubahan harga
- `is_mover(percent_change, threshold)` — tandai True/False apakah pergerakan melewati threshold
- Library: tidak ada (murni matematika)

### `main.py`
- `build_system()` — load config, fetch data multi-coin
- `build_table()` — orkestrasi baseline + analisis + tampilkan tabel
- Loop `while True` dengan cooldown + durasi (dari config) untuk scan berkala, plus notifikasi suara (`winsound.Beep`) saat iterasi baru
- Library: `tabulate`, `os`, `copy`, `sys`, `time`, `winsound`, `dotenv`

---

## Struktur `config.json`

```json
{
  "coins": ["bitcoin", "ethereum", "solana"],
  "currencies": ["usd"],
  "base_url": "https://api.coingecko.com/api/v3/simple/price",
  "max_retries": 3,
  "interval": 2,
  "mover_threshold": 3.0,
  "durasi": 3600,
  "cooldown": 60,
  "last_alert": 0
}
```

## Struktur `baseline.json` (auto-generated)

```json
{
  "bitcoin": 62648.0,
  "ethereum": 1778.8,
  "solana": 81.13
}
```

---

## Key Learnings Baru (di luar Day 1-6)

- **Baseline tracking lintas-proses**: beda konsep dari retry logic — retry menangani kegagalan *dalam* satu eksekusi, baseline menjembatani *antar* eksekusi program yang berbeda waktu
- **Circular import**: terjadi kalau dua modul saling import satu sama lain secara langsung/tidak langsung; solusi: pastikan arah dependency searah (modul dasar seperti `logger.py` tidak boleh bergantung ke modul yang lebih tinggi)
- **Conditional expression** (`x if kondisi else y`): urutan baca beda dari urutan eksekusi — kondisi dicek duluan meski ditulis di tengah
- **Dict comprehension** (`{k: v for k in list}`): cara ringkas mengubah list jadi dictionary
- **`json.JSONDecodeError`**: file yang *ada* tapi kosong/corrupt tetap bisa crash `json.load()` — perlu guard tambahan di luar `exists()`
- **Operator precedence**: `i+1*(interval**2)` dieksekusi sebagai `i + (1*(interval**2))`, bukan `(i+1)*(interval**2)` — perlu kurung eksplisit

---

## Known Issues (belum diperbaiki, dicatat sebagai PR/technical debt)

1. **`calculate_change()` return `False` alih-alih `None`** saat `baseline_price is None` — seharusnya `None` karena ini fungsi numerik, bukan boolean. Perlu diperbaiki agar konsisten dengan `is_mover()`.
2. **`is_mover()` return `None` alih-alih `False`** saat `percent_change is None` — sebelumnya sudah pernah diperbaiki ke `False`, lalu ter-revert. Perlu disamakan lagi: fungsi boolean sebaiknya konsisten selalu return `True`/`False`, tidak pernah `None`.
3. **Status code `402`** sempat dipertanyakan relevansinya di `fetch_retry()` — sudah diperbaiki jadi `404` di versi ini, tapi perlu dicek ulang apakah daftar status permanen (401/403/404) sudah sesuai kebutuhan CoinGecko.
4. **`COINGECKO_API_KEY`** di-load lewat `os.getenv()` di `build_system()` tapi tidak pernah dipakai di `params`/`headers` — bisa dihapus kalau CoinGecko public API memang tidak butuh key, atau diintegrasikan kalau memang dibutuhkan.
5. **`logger` di dalam `if __name__ == "__main__":` block** dipakai sebelum didefinisikan di beberapa cabang (`logger.info(...)` di baris pengecekan durasi, padahal `logger = get_logger()` baru dipanggil di cabang lain) — berpotensi `NameError` tergantung urutan eksekusi.

---

## Koneksi ke Roadmap AI Trading Agent

Capstone ini adalah cikal bakal langsung dari:
- `analysis/` — pola `calculate_change()` + `is_mover()` akan berkembang jadi deteksi pattern yang lebih kompleks di Phase 8
- `memory/` — `baseline_store.py` adalah versi sederhana dari trade journal/histori yang nanti pindah ke SQLite di Phase 6.5
- `data/` — `config.json`/`baseline.json` adalah cikal bakal config dan cache di struktur final

---