# Phase 4 — Day 1: Asyncio Dasar

**Tanggal:** 14 Juli 2026
**Status:** ✅ Selesai (teori + Mp)

---

## Kenapa Asyncio Sebelum Discord Bot?

`discord.py` dibangun total di atas asyncio. Tanpa fondasi ini, kode bot nanti cuma jadi hafalan syntax tanpa paham alurnya. Asyncio juga jadi dasar buat WebSocket (materi optional post-MVP).

---

## Konsep yang Dipelajari

### 1. Blocking vs Non-blocking
- **Blocking** (`time.sleep()`): program berhenti TOTAL selama delay, tidak bisa kerjain apa-apa lain.
- **Non-blocking** (`asyncio.sleep()`): program "istirahat" tapi event loop tetap bisa kerjain tugas lain.
- Analogi: blocking = berdiri diam depan kompor nunggu air mendidih. Non-blocking = pasang timer, sambil nunggu potong sayur dulu.

### 2. `async def` — Coroutine
- `async def` bikin **coroutine**, bukan function biasa.
- Coroutine yang dipanggil tanpa `await`/`asyncio.run()` **tidak jalan** — cuma bikin objek "nunggu dieksekusi".
- Python bakal warning `coroutine was never awaited` kalau lupa.

### 3. `await`
- `await` = "eksekusi coroutine ini SEKARANG, tunggu sampai selesai, tapi kasih ruang ke tugas lain buat jalan di background."
- Cuma bisa dipakai **di dalam** `async def` lain.
- Berlaku juga untuk built-in seperti `asyncio.sleep()` — bukan cuma coroutine buatan sendiri.

### 4. `asyncio.sleep()` vs `time.sleep()`
- **BAHAYA:** pakai `time.sleep()` di dalam `async def` itu bug fatal — kode tetap jalan tanpa error, tapi merusak seluruh tujuan asyncio (jadi blocking lagi).
- Selalu pakai `await asyncio.sleep()` di konteks async.

### 5. `asyncio.run()`
- "Tombol power" — nyalain event loop, jalankan satu coroutine utama (`main()`), tunggu selesai, matikan lagi.
- **Hanya dipanggil sekali**, di baris paling bawah file, di luar `async def` manapun.
- Bukan coroutine, jadi dipanggil tanpa `await`.

### 6. `asyncio.gather()`
- Menjalankan banyak coroutine **benar-benar bersamaan**, bukan bergantian.
- `await` satu-satu tetap sequential — HARUS pakai `gather()` untuk paralel.
- Return value: list hasil sesuai **urutan input**, bukan urutan selesai.
- **Untuk list dinamis:** pakai list comprehension + unpacking `*`:
  ```python
  tasks = [fetch_coin(coin_id) for coin_id in coin_list]
  hasil = await asyncio.gather(*tasks)
  ```
- `gather()` bisa dipakai berlapis di level manapun (termasuk gather beberapa fungsi besar sekaligus, bukan cuma coroutine individual).
- Level kesulitan 🔴 karena: mikirnya harus paralel (bukan linear), return value urutan sering disalahpahami, dan efeknya baru kelihatan lewat perbandingan langsung.

### 7. Event Loop
- "Manajer lalu lintas" tunggal yang terus tanya "coroutine mana yang siap lanjut sekarang?"
- Tetap jalan di **satu thread** — ini concurrency, BUKAN multi-threading/parallelism beneran.
- Analogi: satu pelayan restoran yang gesit gantian ke banyak meja, bukan banyak pelayan sekaligus.

---

## Mini Project: Async Multi-Coin Fetcher

**File:** `Mp-01.py` — folder `phase-4-ASYNC&DISCORD/Day-01/`

**Requirement:**
- `fetch_coin(coin_id)` — simulasi fetch pakai `asyncio.sleep()`
- `fetch_sequential(coin_list)` — fetch satu-satu pakai `await` dalam loop
- `fetch_parallel(coin_list)` — fetch bersamaan pakai `gather(*tasks)`
- Ukur & bandingkan waktu keduanya pakai `time.time()` — **dipanggil terpisah**, bukan di-gather bareng, supaya angka pembanding valid

**Hasil real:**
```
Sequential: 10.02 detik
Parallel: 2.05 detik
```
Untuk 5 coin. Bukti nyata: fetch paralel 5 coin ≈ secepat fetch 1 coin.

---

## Insight Tambahan (Eksplorasi Mandiri)

Sempat coba nested gather — gather dua fungsi besar (`kk()` sequential + `blabla()` paralel) sekaligus. Hasilnya: fungsi yang lebih cepat (`blabla`) selesai duluan meski dipanggil bareng fungsi yang lebih lambat (`kk`). Bukti bahwa `gather()` benar-benar menjalankan startnya bersamaan, bukan cuma "keliatan" bersamaan.

---

## Next: Day 2

Materi tambahan yang sudah disepakati, belum diajarkan:

| Materi | Kesulitan |
|---|---|
| `asyncio.create_task()` | 🟡 |
| Exception handling di coroutine (`try-except` + `await`) | 🟡 |
| `return_exceptions=True` di `gather()` | 🔴 |

Setelah itu lanjut **Day 3: Discord Webhooks**.