# Phase 3 — Day 5: Retry Logic & Resilience 🟡

## Konsep Inti

Program yang bergantung pada network call (`requests.get()`) harus tahan terhadap kegagalan sementara — koneksi putus, timeout, server down sesaat. Tanpa retry logic, program langsung crash di kegagalan pertama, padahal di dunia nyata kegagalan network itu wajar dan sering pulih sendiri dalam hitungan detik.

## Kategori Error

**Worth di-retry (sementara):**
- `ConnectionError` — koneksi putus sesaat
- `Timeout` — server lambat merespon
- Status code 5xx — error di sisi server, biasanya pulih sendiri

**Jangan di-retry (permanen):**
- Status code 404 — endpoint/ID salah, retry tidak mengubah apa-apa
- Status code 401/403 — API key salah/tidak ada akses
- `InvalidURL` — format URL cacat dari awal

**Di luar kendali retry logic:**
- PC mati / program di-kill paksa — retry hanya berlaku selama proses masih hidup

## Exponential Backoff

Jeda antar percobaan retry harus makin lama, bukan konstan — supaya tidak memperparah server yang sedang overload.

```python
time.sleep(delay * (2 ** attempt))
```

`attempt=0` → 1 detik, `attempt=1` → 2 detik, `attempt=2` → 4 detik. Naik dua kali lipat tiap percobaan, beda dengan linear backoff (`(attempt+1) * delay`) yang naik konstan.

## Struktur Fungsi Retry (reusable)

Retry logic dipisah jadi fungsi standalone (`fetch_retry` / `res_test`), bukan ditempel langsung di kode yang manggil API. Alasannya: logic ini akan dipakai ulang di banyak tempat ke depan (Day 6 config fetch, Phase 3 capstone, nanti panggil LLM API di Phase 5) — kalau nempel di satu fungsi, harus copy-paste terus tiap butuh.

```python
def fetch_retry(url, max_retries=3, base_delay=1):
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            status = response.status_code
            if status in (404, 401, 403):
                # fatal — stop retry, tapi jangan matikan seluruh program
                return None
            else:
                time.sleep(base_delay * (2 ** attempt))
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            time.sleep(base_delay * (2 ** attempt))
    return None
```

## Bug yang Ditemukan & Diperbaiki

1. **`response` vs `reponse`** — typo variabel, `raise_for_status()` dipanggil ke nama yang salah.
2. **Delay pertama = 0** — rumus awal `attempt * 5` bikin percobaan pertama tidak ada jeda sama sekali.
3. **Rumus campur linear + exponential** — `(attempt+1) * 2 ** attempt` bukan exponential murni, harusnya cukup `delay * (2 ** attempt)`.
4. **`^` bukan pangkat di Python** — itu operator XOR (bitwise). Pangkat pakai `**`.
5. **`sys.exit()` di error fatal** — mematikan seluruh program hanya karena 1 request gagal permanen. Diganti `return None` supaya cuma request itu yang berhenti, bukan seluruh sistem.

## `break` vs `return`

`break` cuma keluar dari loop terdekat, kontrol lanjut ke baris setelah loop — tidak otomatis mengembalikan nilai apapun. Beda dengan `return`, yang langsung menghentikan seluruh fungsi di titik itu juga, tidak peduli ada kode lain setelahnya.

## Status Code 200 ≠ Data Valid

Pelajaran penting dari Mp-05: `raise_for_status()` cuma mendeteksi error di level HTTP (4xx/5xx). Kalau API dikasih parameter yang salah (misal ID coin tidak ada) tapi tetap balas status 200 dengan body kosong `{}`, itu **tidak akan ketangkep** sebagai error HTTP — harus dicek manual di level aplikasi (`if value == {}`).

## Mini Project 05 — Resilient Multi-Coin Price Fetcher 🔴

**Requirement:**
- Fetch beberapa coin sekaligus, tiap coin request terpisah (bukan 1 request gabungan) — supaya kegagalan 1 coin tidak menggagalkan semua
- Hasil ditampung di dict `{coin: data_atau_None}`, bukan list — supaya tiap hasil tetap terhubung ke nama coin-nya
- Coin yang gagal tetap tampil di tabel (ditandai FAILED), tidak hilang begitu saja
- Logging dibedakan level: `WARNING`/`ERROR` untuk retry sementara, `CRITICAL` untuk fatal

**Bug yang ditemukan selama pengerjaan:**
- Sempat nyampur 2 pendekatan (1 request gabungan vs request per-coin) dalam satu fungsi — bikin `url` tidak berubah tiap iterasi loop
- `return response` di dalam loop coin menghentikan seluruh fungsi, bukan lanjut ke coin berikutnya — solusinya pisah fungsi retry (1 request) dari fungsi loop (banyak coin)
- Cek kondisi gagal sempat salah target (`if key is not None` — padahal `key` itu nama coin yang tidak pernah `None`, yang bisa `None`/kosong itu `value`)
- Struktur JSON CoinGecko nested — hasil per coin masih dibungkus 1 layer nama coin di dalamnya (`{"ethereum": {"usd": ..., "idr": ...}}`), perlu akses `value[key]["usd"]`, bukan `value["usd"]` langsung

**Hasil akhir:** berhasil fetch Bitcoin & Ethereum dengan retry+backoff teruji nyata (simulasi mode pesawat), coin dengan ID salah (`"bih"`) tertangani sebagai FAILED tanpa mematikan program.

---

**Next:** Day 6 — Config Eksternal & Credential Handling