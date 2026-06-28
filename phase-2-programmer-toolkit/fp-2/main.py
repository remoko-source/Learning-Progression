#TradeDesk CLI
from logger import setup_logging ; from validator import validate_trade, TradeValidationError
from storage import load_trades, update_trade, add_trade ; import time
from scanner import check ; import sys ; import os
check()
logger = setup_logging()
logger.info("PROGRAM DIJALANKAN")
def menu():
	print("=================================================")
	print("    Selamat datang di aplikasi TradeDesk CLI!")
	print("=================================================")
	print("[1] Add Trade")
	print("[2] View Trade")
	print("[3] Update Trade")
	print("[0] Exit")

def add():
	while True:
		coin = input("Masukkan nama coin: ").upper()
		entry_price = input("Masukkan harga awal: ")
		status = input("Masukkan status (OPEN/WIN/LOSS) : ").upper()
		if status == "OPEN":
			pnl = 0
		else:
			pnl = input("Masukkan PnL: ")
		try:
			if validate_trade(coin, entry_price, status, pnl):
				break
		except TradeValidationError as e:
			print("ERROR:", e)
			logger.error(str(e))
			time.sleep(2)
			os.system("cls")

	add_trade(coin, float(entry_price), status, float(pnl))
	print(f"TRADE {coin} Berhasil ditambahkan!")
	logger.info("BERHASIL TAMBAH TRADE!")
	time.sleep(1)
	
def view():
	trades = load_trades()
	for value in trades:
		print("==============================")
		print("  ID :", value["id"])
		print("  Nama coin: ", value["coin"])
		print("  Entry Price: ", value["entry_price"])
		print("  Status: ", value["status"])
		print("  PnL: ", value["pnl"])
		print("==============================")
	input("> ")
	logger.info("BERHASIL lihat trades")
		
def update():
	trades = load_trades()
	for value in trades:
		if value["status"] == "OPEN":
			print("==============================")
			print("  ID :", value["id"])
			print("  Nama coin: ", value["coin"])
			print("  Entry Price: ", value["entry_price"])
			print("  Status: ", value["status"])
			print("  PnL: ", value["pnl"])
			print("==============================")
			print()
		
	while True:
		try:
			id = int(input("Masukkan id trade yang ingin anda ubah: "))
			if id > len(trades):
				print("ID tidak Valid")
				continue
			elif trades[id-1]["status"] != "OPEN":
				print("Trade sudah selesai.")
				return
			sell = float(input("Masukkan harga jual: "))
			break
		except ValueError:
			print("ERROR: Harus berupa angka")
			logger.error("Bentuk ID/HARGA bukanlah Angka")
	update_trade(sell, id)
	print("BERHASIL update Trade")
	logger.info("BERHASIL update Trade")
	time.sleep(2)

while True:
	os.system("cls")
	menu()
	ui = input("> ")
	print("=================================================")
	time.sleep(2)
	if ui == "1":
		os.system("cls")
		add()
	elif ui == "2":
		os.system("cls")
		view()
	elif ui == "3":
		os.system("cls")
		update()
	elif ui ==  "0":
		logger.info("PROGRAM SELESAI")
		sys.exit()
	else:
		print("Input tidak valid")
		time.sleep(2)
		