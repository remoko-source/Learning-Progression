# Day 05 — datetime Module

## Apa yang dipelajari
Belajar datetime module — module bawaan Python untuk
manipulasi tanggal, jam, dan durasi waktu.

## Fungsi yang dipakai
- `datetime.now()` — ambil waktu sekarang dari jam sistem
- `strftime()` — ubah datetime jadi string sesuai format
- `strptime()` — ubah string jadi datetime (kebalikan strftime)
- `timedelta()` — representasi durasi/selisih waktu

## Konsep baru yang ditemuin
- f-string — gabungin teks dan variabel pakai `f"..."` dan `{ }`
- `is None` — cek apakah variabel masih kosong/belum diisi
- `datetime ± timedelta = datetime`
- `datetime - datetime = timedelta`
- `strftime` cuma bisa dipakai di `datetime`, gak bisa di `timedelta`

## Mini Project
Activity Logger — script yang catat timestamp untuk tiap
aktivitas dalam list, lalu hitung total durasi dari aktivitas
pertama sampai terakhir

## Bonus - Time Comparator (Candle Checker) 
### Tujuan
Cek apakah waktu sekarang sudah melewati jadwal "candle baru"
atau masih dalam candle yang sama

candle_baru = candle_buka + timedelta(hours=1)
if waktu >= candle_baru:
"Candle baru sudah dibentuk"
else:
"Masih dalam candle yang sama, sisa waktu: candle_baru-waktu"

### Insight Penting
- `waktu > candle` (jam sekarang > jam mulai candle) selalu 'True'
  → gak relevan buat nentuin candle baru atau enggak
- Perbandingan yang benar adalah `waktu` vs `candle_baru`
  (jam tutup candle), bukan `waktu` vs `candle` (jam mulai)
- Dua datetime bisa dibandingkan langsung pakai `>`, `<`, `>=`, `<=`
  — sama seperti membandingkan angka biasa

### Testing dengan 2 skenario
- `sekarang = 15:30`, `candle_baru = 15:00` → sudah lewat → "Candle baru sudah dibentuk"
- `sekarang = 14:30`, `candle_baru = 15:00` → belum lewat → "Masih dalam candle yang sama, sisa waktu: 0:30:00"

### Relevansi ke AI Trading Agent
Bot perlu tau apakah data candle yang dia simpan masih valid
atau sudah harus ambil candle baru — ini logic dasarnya.





