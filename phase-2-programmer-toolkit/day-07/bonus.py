import random
#1 Shuffle
kan = ["kel","sunny","mari"]
random.shuffle(kan)
print(kan)

#2 Randint
hasil = random.randint(1, 10)
print(hasil)

#3 Random
nilai = random.random()
if nilai > 51:
	print("Harga naik")
elif nilai <= 50:
	print("Harga turun")
print(nilai)

#4 Choice
lek = random.choice(kan)
print(lek)

#5 Uniform
lol = random.uniform(1, 10.0)
print(f"{lol:.2f}")

#Latihan:
import logging
class FailedPurchaseError(Exception):
	pass
logger = logging.getLogger("DIMAS")
logger.setLevel(logging.DEBUG)

data = logging.FileHandler("LOG.txt")
data.setLevel(logging.INFO)
visual = logging.StreamHandler()
visual.setLevel(logging.WARNING)

prompt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
data.setFormatter(prompt)
visual.setFormatter(prompt)

logger.addHandler(data)
logger.addHandler(visual)
#dummy btc 5 10000, eth 2 15000
uanh = random.randint(1, 200000)
listt = {
	"BTC": (60000, 70000),
	"ETH": (3000, 4000),
	"SOL": (100, 200)
}
cust = ["1", "2", "3", "4", "5"]
print(uanh)
import time
import sys
for key in range(5):
	try:
		luck_check = random.random()
		if luck_check < 0.1:
			logger.critical("sampai jumpa o7")
			sys.exit()
		elif luck_check > 0.1 and luck_check < 0.2:
			logger.error("SYSTEM OVERLOAD")
			time.sleep(5)
		elif luck_check > 0.2 and luck_check < 0.4:
			logger.error("Kesalahan pembayaran, Silahkan membeli ulang")
		elif luck_check > 0.4:
			print("Memulai proses pembelian (GACHA)...")
			coin = random.choice(list(listt.keys()))
			harga = random.uniform(*listt[coin])
			time.sleep(3)
			if uanh >= harga:
				print("Sukses membeli!")
				random.shuffle(cust)
				print(f"Selamat {cust[0]}! anda berhasil membeli {coin}")
				cust.pop(0)
				uanh -= harga
			else:
				raise FailedPurchaseError(f"Uang anda kurang sebesar: {harga - uanh}")
	except FailedPurchaseError as e:
		print("ERROR: ", e)
print("Program sukses")
print(uanh)