# Phase 4 - Day 2: Asyncio Lanjutan

## Materi

### 1. `asyncio.create_task()`
- Menjadwalkan coroutine supaya mulai jalan **sekarang juga** di background, tanpa harus di-`await` dulu.
- Kamu pegang "tiket" (Task object) yang bisa di-`await` belakangan kapan saja.
- Beda dengan `gather()`: `gather()` = "jalankan semua + tunggu semua" dalam satu baris. `create_task()` = kasih jeda, bisa start duluan, ngapain-ngapain dulu, baru `await` belakangan.

**Pola yang benar untuk banyak task:**
```python
tasks = []
for i in coins:
    task = asyncio.create_task(handling(i))  # start SEMUA duluan
    tasks.append(task)

hasil = await asyncio.gather(*tasks)  # baru tunggu SEMUA bareng
```

**BUG PENTING yang ditemukan hari ini:** kalau `await asyncio.gather(*tasks)` ke-indent **di dalam** `for` loop, dia kepanggil berkali-kali (tiap iterasi), dan tiap kali cuma nungguin isi `tasks` yang baru nambah 1 item. Efeknya jadi nunggu 1-1-1-1-1 (sequential), bukan nunggu 5 sekaligus di akhir. Pastikan `gather()` sejajar dengan `for`, alias di luar loop.

**Cara ketahuan bug ini:** ukur waktu total. 5 coin x sleep(1 detik) kalau paralel beneran = ~1 detik. Kalau muncul ~5 detik, berarti balik jadi sequential meski sudah pakai `create_task()`.

### 2. Exception handling di coroutine (try-except + await)
- Try-except di dalam coroutine membungkus `await`, karena error baru "muncul" pas coroutine benar-benar dieksekusi di titik `await`, bukan saat dipanggil.
- Return dictionary yang jelas statusnya saat gagal (bukan cuma `None`), supaya info kenapa gagal (reason) tidak hilang — penting untuk retry logic nanti.

```python
async def handling(nama_coin):
    try:
        hasil = await fetch_coin(nama_coin)
        return hasil
    except ValueError as e:
        return {"Coin": nama_coin, "Status": "Failed", "Price": 0, "Keterangan": str(e)}
```

### 3. `return_exceptions=True` di `gather()`
- Default `gather()`: begitu 1 task raise error, `gather()` langsung crash total dan melempar error ke atas. Task lain yang belum selesai tetap jalan di background, tapi hasilnya **tidak pernah ditangkap**.
- `return_exceptions=True` mengubah itu: semua task tetap ditunggu sampai selesai, dan error yang terjadi dibungkus jadi item `Exception` di dalam list hasil (bukan di-raise).
- **Dua strategi berbeda untuk masalah yang sama — pilih satu, jangan campur tanpa alasan:**

| Strategi | Tempat handle error | Kapan cocok |
|---|---|---|
| A. Try-except di dalam coroutine | Return dict/None saat gagal, sebelum sampai `gather()` | Butuh kontrol detail per jenis error (retry, log spesifik) — **cocok untuk Market Scanner** |
| B. `return_exceptions=True` | Di level `gather()`, exception jadi item list | Malas nulis try-except di tiap coroutine, cukup cek `isinstance(r, Exception)` belakangan |

- Kalau sudah pakai Strategi A di semua coroutine, `return_exceptions=True` jadi tidak berpengaruh (dead parameter) — karena tidak ada exception yang lolos sampai ke `gather()`.
- **Bukan untuk debugging.** Ini soal *production behavior* — bagaimana sistem tetap jalan normal saat sebagian gagal (resilience), bukan proses cari bug saat development.

### Koreksi konsep penting
- `asyncio.sleep()` BUKAN untuk mengukur waktu. Fungsinya cuma "berhenti sebentar tapi kasih kesempatan coroutine lain jalan". Yang dipakai ukur waktu tetap `time.time()`.
- `asyncio.sleep()` dipakai di latihan sebagai simulasi "nunggu API respond" tanpa koneksi internet asli (supaya bebas rate limit saat testing).
- Kalau sebuah `async def` tidak punya `await` sama sekali di dalamnya, dia tidak punya "titik nunggu" — jadi paralelisme lewat `create_task()` tidak akan kelihatan efeknya walaupun strukturnya benar.

## Mini Project: Resilient Multi-Coin Fetcher

File: `Mp-02.py`

Menggabungkan `create_task()`, try-except di dalam coroutine (Strategi A), dan `gather()` untuk fetch 5 coin (1 sengaja invalid: `scam_coin`) secara paralel. Output ditampilkan pakai `tabulate`, dan waktu total diukur dengan `time.time()`.

**Hasil pembuktian:**
- Sebelum fix (gather di dalam loop): ~5.1 detik → sequential
- Setelah fix (gather di luar loop, sejajar `for`): **1.0 detik** → paralel beneran

## Key takeaway hari ini

Klaim "kode sudah benar" harus dibuktikan dengan angka hasil run, bukan cuma keyakinan. Teknik `print(time.time())` di beberapa titik kunci (sebelum loop, setelah semua task dibuat, setelah gather) adalah cara cepat menemukan di titik mana delay terjadi — dipakai lagi nanti untuk Discord bot dan Market Scanner.