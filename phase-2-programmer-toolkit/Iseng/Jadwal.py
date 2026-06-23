import logging ; import os ; import time
import json ; from datetime import datetime ; import random
man = True
#=================================================================================================
#Log handler
logger = logging.getLogger("Ibnu")
logger.setLevel(logging.DEBUG)

file = logging.FileHandler("jadwal.log")
visual = logging.StreamHandler()

prompt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%d %m %Y %H:%M:%S")
file.setFormatter(prompt)
visual.setFormatter(prompt)

file.setLevel(logging.INFO)
visual.setLevel(logging.ERROR)

logger.addHandler(file)
logger.addHandler(visual)
#=================================================================================================

def menu():
	print("=======================================")
	print("   Selamat datang di sistem Jadwal")
	print("=======================================")
	print("1. Ubah status jadwal")
	print("2. Lihat jadwal")
	print("3. Shuffle jadwal")
	print("4. Keluar")

def shuffle():
	lol = ["Chest","Arm","Leg"]
	random.shuffle(lol)
	print("SHUFFLE: ", lol)
	d1 = lol[0]
	d2 = lol[1]
	d3 = lol[2]
	d4 = lol[random.randint(1, 2)]
	d5 = random.choice(lol)
	d6 = lol[random.randint(0, 1)]
	print("Hari pertama: ", d1)
	print("Hari kedua: ", d2)
	print("Hari ketiga: ", d3)
	print("Hari keempat: ", d4)
	print("Hari kelima: ", d5)
	print("Hari keenam: ", d6)
	logger.info("Berhasil diacak")
	input()
	return [d1, d2, d3, d4, d5, d6]

def simpan():
	hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jum'at", "Sabtu"]
	jadwal = shuffle()
	jadwal_dict = {}
	with open("Jadwal.json", "w") as f:
		for nama, latihan in zip(hari, jadwal):
			jadwal_dict[nama] = {
			"latihan" : latihan,
			"status" : "belum"
			}
		json.dump(jadwal_dict, f, indent=2)
def lihat():
	olahraga = {
	"1":{
	"Wall Push-Up" : "3 x 15",
	"Incline Push-up" : "3 x 8-12", #Chest
	"Knee Push-up" : "3 x 5-10",
	"Istirahat" : "60-90 detik"
	},
	"2":{
	"Wall Push-Up" : "3 x 15",
	"Chair Dips" : "3 x 8",
	"Diamond Knee Push-Up" : "3 x 5", #Arm
	"Istirahat" : "60 - 90 detik"
	},
	"3":{
	"Calf Raise" : "3 x 15",
	"Chair Dips" : "3 x 12", #Leg
	"Glute Bridge" : "3 x 12",
	"Istirahat" : "90 detik"
	}
	}
	hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jum'at", "Sabtu"]
	m = hari[datetime.now().weekday()]
	with open("Jadwal.json", "r") as file:
		data = json.load(file)
		if data[str(m)]["status"] == "belum":
			print("========= ",str(m)," =========")
			if data[str(m)]["latihan"] == "Chest":
				kl = olahraga["1"]
				for i, value in kl.items():
					print(f"- {i}: {value}")
			elif data[str(m)]["latihan"] == "Arm":
				kl = olahraga["2"]
				for i, value in kl.items():
					print(f"- {i}: {value}")
			elif data[str(m)]["latihan"] == "Leg":
				kl = olahraga["3"]
				for i, value in kl.items():
					print(f"- {i}: {value}")
			print("===========================")
		else:
			print("Tugas Hari ini sudah selesai!")
		input(">")
		logger.info("Cek List")
def status():
	with open("Jadwal.json", "r") as f:
		data = json.load(f)
		i = 0
		for key, value in data.items():
			i += 1
			print("================")
			print(str(i)+".",key)
			print("Latihan: ",value["latihan"])
			print("Status: ", value["status"])
			print("================")
			print()
		lop = int(input("Mana yang ingin diubah?: "))
		hari = ["Senin", "Selasa", "Rabu", "Kamis", "Jum'at", "Sabtu"]
		if lop in range(1, len(data)+1) and data[hari[lop - 1]]["status"] == "belum":
			data[hari[lop-1]]["status"] = "Selesai"
			with open("Jadwal.json", "w") as fi:
				json.dump(data, fi, indent=2)
			logger.info("Berhasil update status")
		elif data[hari[lop - 1]]["status"] == "Selesai":
			print()

while man:
	os.system("cls")
	menu()
	kan = input("Apa yang ingin kamu lakukan?: ")
	if kan == "1":
		os.system("cls")
		status()
	elif kan == "2":
		os.system("cls")
		lihat()
	elif kan == "3":
		os.system("cls")
		simpan()
	elif kan == "4":
		print("=======================================")
		print("            Sampai Jumpa!")
		print("=======================================")
		time.sleep(3)
		man = False
	else:
		print("Perintah tidak valid")
		time.sleep(3)