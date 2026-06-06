# Day 03 — os Module

## Apa yang dipelajari
Belajar os module — module bawaan Python untuk manipulasi 
file dan folder via script.

## Fungsi yang dipakai
- `os.getcwd()` — lihat posisi folder sekarang
- `os.mkdir()` — bikin folder baru
- `os.makedirs()` — bikin folder bertingkat
- `os.path.exists()` — cek apakah folder/file ada
- `os.path.join()` — gabungin path dengan aman
- `os.listdir()` — lihat isi folder
- `os.path.splitext()` — pecah nama file dan ekstensinya

## Konsep baru yang ditemuin
- `exist_ok=True` — bikin folder tanpa error walau sudah ada
- Tuple — kayak list tapi isinya gak bisa diubah
- Unpacking — langsung pecah hasil fungsi ke beberapa variabel
- `enumerate` — loop dengan nomor urut sekaligus
- Flag variable — variabel True/False untuk nandain kondisi

## Mini Project
File Organizer — script yang kategorikan file dummy 
berdasarkan ekstensi ke folder gambar, dokumen, dan lainnya