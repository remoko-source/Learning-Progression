# Day 04 — sys Module

## Apa yang dipelajari

Belajar sys module — module bawaan Python yang jadi
jembatan antara program Python dan sistem operasi.

## Fungsi yang dipakai

- `sys.argv` — ambil argumen dari terminal
- `sys.exit()` — menghentikan program secara paksa

## Konsep baru yang ditemuin

- `sys.argv` berbentuk list
- Semua isi `sys.argv` bertipe string
- Harus pakai `int()` kalau mau dipakai untuk perhitungan
- Guard clause — cek kondisi di awal lalu langsung stop kalau gagal
- Perbedaan `sys.exit()` vs `else`
- Refactor — ubah struktur kode tanpa mengubah hasil program
- Command `touch` tanpa `/` di depan untuk bikin file
- Command `mv` untuk rename file

## Mini Project

Kalkulator terminal (`Mp-4.py`) — kalkulator yang menggunakan
sys module, sehingga input diambil melalui terminal
saat user menjalankan program.

Contoh penggunaan:
```
python Mp-4.py 10 + 5  → Hasil: 15
python Mp-4.py 20 - 3  → Hasil: 17
python Mp-4.py 6 * 7   → Hasil: 42
python Mp-4.py 10 / 2  → Hasil: 5.0
```