from datetime import datetime ; from pathlib import Path
import json ; import logging ; import os ; import sys
#=================================================================================================
#Log handler
logger = logging.getLogger("BUDI")
logger.setLevel(logging.INFO)

filejh = logging.FileHandler("TESTING.log")
filejh.setLevel(logging.INFO)

format = logging.Formatter("%(asctime)s-%(levelname)s|%(message)s", "%d/%m/%Y %H:%M:%S")
filejh.setFormatter(format)

logger.addHandler(filejh)
#=================================================================================================

def converter(obj):
	if isinstance(obj, datetime):
		return obj.strftime("%d/%m/%Y %H:%M:%S")
		
def tambah():
	kan = True
	while kan:
		print("Masukkan string JSON")
		print('Contoh: "ETH" : {"Harga": 2000, "Jumlah": 1}')
		kzm = input("$ ")
		try:
			data = json.loads("{" + kzm + "}")
			if len(data) != 1:
				raise ValueError
			coin_awal = next(iter(data))
			coin = coin_awal.upper()
			data[coin] = data.pop(coin_awal)
			if not isinstance(data[coin], dict) or "Harga" not in data[coin] or "Jumlah" not in data[coin]:
				raise ValueError
			data[coin]["Tanggal"] = datetime.now()
			print("Format Valid")
			k = Path.cwd() / "Test.json"
			with open(k,"r") as man:
				lama = json.load(man)
				if coin in lama:
					logger.info("Coin update (FORMAT): %s", coin)
				else:
					logger.info("COIN baru (FORMAT): %s", coin)
			lama.update(data)
			with open(k, "w") as file:
				json.dump(lama, file, indent=4, default=converter)
			break
		except json.JSONDecodeError:
			print("Data Corrupt")

user = input("Masukkan nama coin : > ").upper()
if user != "LOOK":
	try:
		harga = int(input("Masukkan harga coin : > "))
		jumlah = int(input("Masukkan jumlah coin : > "))
		k = Path.cwd() / "Test.json"
		try:
			with open(k,"r") as man:
				data = json.load(man)
				if user in data:
					logger.info("COIN update (NORMAL): %s",user)
				else:
					logger.info("COIN baru (NORMAL): %s",user)
		except:
			data = {}
		data[user] = {
			"Harga" : harga,
			"Jumlah" : jumlah,
			"Tanggal" : datetime.now()
			}
		with open(k, "w") as file:
			json.dump(data, file, indent=4, default=converter)
		with open(k, "r") as dan:
			data = json.load(dan)
			for key, value in data.items():
				print("=========================================")
				print(key,"- " "Seharga : ", value["Harga"])
				print("Memiliki sejumlah: ", value["Jumlah"])
				print("Data dibuat pada =", value["Tanggal"])
				print("=========================================")
		aak = input("Lanjut? Y/T: ").upper()
		if aak == "Y":
			os.system("cls")
			tambah()
	except ValueError as e:
		print("ERROR: ", e)
	else:
		try:
			with open("Test.json", "r") as file:
				l = json.load(file)
				k = json.dumps(l, indent=4)
				print(k)
		except json.JSONDecodeError:
			print("ERROR: File Corrupt")
			
elif user == "LOOK":
	try:
		with open("Test.json", "r") as file:
			l = json.load(file)
			k = json.dumps(l, indent=4)
			for key, value in l.items():
				print("=========================================")
				print(key,"- " "Seharga : ", value["Harga"])
				print("Memiliki sejumlah: ", value["Jumlah"])
				print("Data dibuat pada =", value["Tanggal"])
				print("=========================================")
			print(k)
	except FileNotFoundError:
		print("File tidak ada")
	except json.JSONDecodeError as e:
		print("File Corrupt")
	finally:
		aak = input("Lanjut? Y/T: ").upper()
		if aak == "Y":
			os.system("cls")
			tambah()
		print("GOOD LUCK")