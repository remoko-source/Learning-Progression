"""
LATIHAN REVIEW - Phase 4 Day 6
================================
Kerjakan semua TODO di bawah TANPA bantuan AI.
Urutan soal: nested structure -> JSON safe load/save -> exception -> asyncio.

Jalankan file ini langsung untuk cek jawaban kamu (ada test sederhana di paling bawah).
"""

import asyncio
import json
from pathlib import Path


# =========================================================
# SOAL 1 (Nested structure - dasar)
# =========================================================
# Diberikan struktur berikut:
scan_results = {
    "BTC": [],
    "ETH": []
}

# TODO 1:
# Tambahkan hasil scan {"signal": "BUY", "confidence": 80} ke dalam BTC.
# Tulis kode di bawah ini:

scan_results["BTC"].append({"signal": "BUY", "confidence": 80})


# =========================================================
# SOAL 2 (Nested structure - akses langsung, bukan loop)
# =========================================================
trade_journal = {
    "BTC": [
        {"entry": 65000, "exit": 66000, "result": "win"},
        {"entry": 64000, "exit": 63500, "result": "loss"}
    ],
    "ETH": [
        {"entry": 3200, "exit": 3350, "result": "win"}
    ]
}

# TODO 2:
# Ambil (akses langsung, JANGAN pakai loop) nilai "entry" dari trade BTC
# yang KEDUA (index 1). Simpan ke variabel bernama `btc_entry_kedua`.

btc_entry_kedua = trade_journal["BTC"][1]["entry"]

# =========================================================
# SOAL 3 (Nested structure - level dalam, dict di dalam list di dalam dict)
# =========================================================
market_scan = {
    "session_id": "scan_002",
    "results": {
        "BTC": {
            "signals": [
                {"type": "BUY", "confidence": 80, "tags": ["breakout"]},
            ]
        },
        "SOL": {
            "signals": []
        }
    }
}

# TODO 3a:
# Tambahkan tag baru "high_volume" ke signal BTC index 0.
market_scan["results"]["BTC"]["signals"][0]["tags"].append("high_volume")

# TODO 3b:
# Tambahkan signal baru {"type": "SELL", "confidence": 55, "tags": ["resistance"]}
# ke SOL (yang signals-nya masih kosong).

market_scan["results"]["SOL"]["signals"].append({"type": "SELL", "confidence": 55, "tags": ["resistance"]})

# =========================================================
# SOAL 4 (List/dict comprehension - transform sederhana)
# =========================================================
prices = {"BTC": 65000, "ETH": 3200, "SOL": 140}

# TODO 4:
# Buat DICT comprehension baru bernama `prices_up_10` yang isinya sama
# seperti `prices` tapi semua value dikali 1.1 (simulasi naik 10%).

prices_up_10 = {key : (value * 1.1) for key, value in prices.items()}

# =========================================================
# SOAL 5 (Comprehension vs loop biasa - harus bisa pilih yang tepat)
# =========================================================
raw_signals = [
    {"coin": "BTC", "confidence": 85},
    {"coin": "ETH", "confidence": 40},
    {"coin": "SOL", "confidence": 72}
]

# TODO 5:
# Ambil coin-coin yang confidence-nya > 60 SAJA, hasilnya list biasa
# berisi nama coin saja (bukan dict). Contoh hasil: ["BTC", "SOL"]
# Pikirkan: ini cocok pakai comprehension atau loop biasa? Kerjakan sesuai keputusanmu.
# Simpan ke variabel `strong_signals`.
strong_signals = [coin["coin"] for coin in raw_signals if coin["confidence"] > 60]


# =========================================================
# SOAL 6 (JSON - safe load pattern)
# =========================================================
# TODO 6:
# Lengkapi fungsi load_journal di bawah ini.
# Syarat:
# - Kalau file belum ada -> return list kosong []
# - Kalau file ada tapi isinya corrupt/invalid JSON -> return list kosong []
#   (JANGAN sampai program crash)
# - Kalau normal -> return isi JSON-nya

def load_journal(filepath):
	if not Path(filepath).exists():
		return []
	try:
		with open(filepath, "r") as data:
			hasil = json.load(data)
		return hasil
	except json.JSONDecodeError as e:
		return []


# =========================================================
# SOAL 7 (JSON - alur load -> ubah -> dump, BUKAN append langsung ke file)
# =========================================================
# TODO 7:
# Lengkapi fungsi add_trade di bawah ini.
# Fungsi ini harus:
# 1. Load journal dari file (pakai load_journal yang sudah kamu buat di Soal 6)
# 2. Tambahkan `new_trade` ke list tersebut
# 3. Tulis ULANG seluruh journal ke file (bukan append teks ke file)

def add_trade(filepath, new_trade):
	hasil = load_journal(filepath)
	hasil.append(new_trade)
	with open(filepath, "w") as file:
		json.dump(hasil, file)


# =========================================================
# SOAL 8 (Custom Exception - kapan bikin custom vs pakai built-in)
# =========================================================
# TODO 8:
# Buat SATU custom exception class bernama `ConfidenceTerlaluRendah`
# yang akan di-raise kalau confidence sebuah signal < 50.
# (Cukup definisikan class-nya saja di sini, class Exception biasa)

class ConfidenceTerlaluRendah(Exception):
	pass

# TODO 8b:
# Buat fungsi `validasi_signal(signal)` yang menerima dict signal
# (contoh: {"coin": "BTC", "confidence": 30})
# - Jika confidence < 50 -> raise ConfidenceTerlaluRendah dengan pesan
#	yang menyebutkan nama coin dan confidence-nya
# - Jika >= 50 -> return signal apa adanya

def validasi_signal(signal):
	if signal["confidence"] < 50:
		raise ConfidenceTerlaluRendah(f"Coin : {signal['coin']} Confidence : {signal['confidence']}")
	else:
		return signal


# =========================================================
# SOAL 9 (on_command_error style - simulasi tanpa Discord)
# =========================================================
# Bayangkan ini adalah simulasi sederhana dari on_command_error, TANPA discord.py,
# supaya kamu bisa latihan logic isinstance-nya tanpa perlu jalankan bot beneran.
#
# TODO 9:
# Lengkapi fungsi `handle_error(error)` di bawah ini.
# - Jika error adalah ValueError -> return string "Input tidak valid"
# - Jika error adalah KeyError -> return string "Data tidak ditemukan"
# - Jika error adalah ConfidenceTerlaluRendah (dari Soal 8) -> return
#	string berisi pesan error tersebut (str(error))
# - Selain itu -> return string "Error tidak diketahui"
#
# Gunakan isinstance(), BUKAN banyak except terpisah.


def handle_error(error):
	if isinstance(error, ValueError):
		return "Input tidak valid"
	elif isinstance(error, KeyError):
		return "Data tidak ditemukan"
	elif isinstance(error, ConfidenceTerlaluRendah):
		return(str(error))
	else:
		return "Error tidak diketahui"


# =========================================================
# SOAL 10 (asyncio - create_task vs sleep, paling sulit)
# =========================================================
# Skenario: kamu punya 2 fungsi async di bawah ini yang MENIRU perilaku
# scanner_loop (jalan terus di background, cetak progress tiap 1 detik,
# sebanyak 3 kali) dan proses_command (mensimulasikan user manual trigger,
# butuh waktu 0.5 detik untuk selesai, lalu cetak hasil).
#
# TODO 10:
# Lengkapi fungsi `main()` di bawah supaya:
# - `background_scanner()` berjalan DI BACKGROUND (tidak boleh memblokir)
# - `proses_command()` tetap bisa jalan dan selesai duluan meskipun
#	background_scanner belum selesai 3 putarannya
# - Program menunggu keduanya benar-benar selesai sebelum keluar dari main()
#	(hint: kamu butuh menyimpan hasil create_task ke variabel, lalu await
#	variabel itu di akhir, atau gunakan asyncio.gather untuk sebagian saja)

async def background_scanner():
	for i in range(3):
		print(f"[scanner] putaran {i+1}")
		await asyncio.sleep(1)
	print("[scanner] selesai 3 putaran")

async def proses_command():
	await asyncio.sleep(0.5)
	print("[command] hasil sudah siap")

async def main():
	task_backscan = asyncio.create_task(background_scanner())
	await proses_command()
	await task_backscan


# =========================================================
# AREA TEST - jangan diubah, jalankan file ini untuk cek jawabanmu
# =========================================================
if __name__ == "__main__":
	print("=== Cek Soal 1-3 (manual, lihat print di bawah) ===")
	print("scan_results:", scan_results)
	print("market_scan BTC signals:", market_scan["results"]["BTC"]["signals"])
	print("market_scan SOL signals:", market_scan["results"]["SOL"]["signals"])

	print("\n=== Cek Soal 2 ===")
	try:
		print("btc_entry_kedua:", btc_entry_kedua)
	except NameError:
		print("btc_entry_kedua belum didefinisikan")

	print("\n=== Cek Soal 4 ===")
	try:
		print("prices_up_10:", prices_up_10)
	except NameError:
		print("prices_up_10 belum didefinisikan")

	print("\n=== Cek Soal 5 ===")
	try:
		print("strong_signals:", strong_signals)
	except NameError:
		print("strong_signals belum didefinisikan")

	print("\n=== Cek Soal 6 & 7 (JSON) ===")
	test_file = "test_journal.json"
	Path(test_file).unlink(missing_ok=True)	 # mulai bersih
	print("load journal (file belum ada):", load_journal(test_file))
	add_trade(test_file, {"coin": "BTC", "result": "win"})
	print("isi journal setelah add_trade:", load_journal(test_file))
	Path(test_file).unlink(missing_ok=True)	 # bersihkan lagi

	print("\n=== Cek Soal 8 & 9 (Exception) ===")
	try:
		validasi_signal({"coin": "BTC", "confidence": 30})
	except Exception as e:
		print("handle_error hasil:", handle_error(e))

	print("handle_error(ValueError()):", handle_error(ValueError()))
	print("handle_error(KeyError()):", handle_error(KeyError()))
	print("handle_error(RuntimeError()):", handle_error(RuntimeError()))

	print("\n=== Cek Soal 10 (asyncio) ===")
	asyncio.run(main())
	
#TRAINING BY CLAUDE