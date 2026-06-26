#test login dengan log dan json
import json
import os
import logging
A = True
current_user = None
logger = logging.getLogger("latihan")
file = logging.FileHandler("international.log")
visual = logging.StreamHandler()

format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file.setFormatter(format)
visual.setFormatter(format)

logger.setLevel(logging.DEBUG)
file.setLevel(logging.INFO)
visual.setLevel(logging.WARNING)

logger.addHandler(file)
logger.addHandler(visual)

def menu2():
	print("LOL")
def login():
	with open("data.json", "r") as dih:
		data = json.load(dih)
	akun = input("Masukkan username akunmu: ").upper()
	try:
		pasw = int(input("Masukkan password: "))
	except ValueError:
		print("Harus berupa angka!")
		return
	for user in data:
		if akun == user["usn"] and pasw == user["pass"]:
			logger.info(f"{akun} Login")
			print(f"Berhasil login - selamat datang kembali, {akun+'!'}")
			global current_user
			current_user = akun
			menu2()
			return
	print("Username atau Password Invalid")
def menu():
	if os.path.exists("data.json"):
		pass
	else:
		with open("data.json", "w") as file:
			json.dump(file, "")
	
	print("====================================")
	print("  Selamat datang di PROGRAM LOGIN !!")
	print("====================================")
	print("1. LOGIN ke akun yang sudah ada")
	print("2. Buat akun baru")
	print("3. Keluar")
while A:
	menu()
	kok = input("Apa yang ingin anda lakukan? : ")
	if kok == "1":
		os.system("cls")
		login()
	elif kok == "2":
		os.system("cls")
		buat()
	elif kok == "3":
		print("Sampai Jumpa!")
		A = False
	else:
		print("Tidak valid!")



















