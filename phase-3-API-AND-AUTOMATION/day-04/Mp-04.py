#Multi Coin-Price Tracker
from tabulate import tabulate 
import winsound
import time 
import requests
import copy


try:
	coins = ["bitcoin","solana","ethereum"]
	url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(coins)}&vs_currencies=usd,idr"
	cooldown = 60
	i = 0
	durasi = float("inf")
	last_alert = 0
	start = time.time()
	lol = []
	while True:
		if time.time() - start >= durasi:
			print("PROGRAM SELESAI")
			break
		else:
			if time.time() - last_alert >= cooldown:
				winsound.Beep(1000,500)
				i += 1
				response = requests.get(url)
				response.raise_for_status()
				response = response.json()
				if i > 1:
					print("ITERASI KE -",i)
					for l, (key, value) in enumerate(response.items()):
						persen = ((value['usd'] - lol[l]['Harga_awal']) / lol[l]['Harga_awal']) * 100
						lol[l]["Harga"] = value["usd"]
						lol[l]["Change"] = str(persen) + "%"
					print(tabulate(lol, headers="keys", tablefmt="grid" , floatfmt=(".2f", "g"), colalign=("left","center","center","right"), numalign="right"))
					for l, (key, value) in enumerate(response.items()):
						lol[l]["Harga_awal"] = value["usd"]
				else:
					for key, value in response.items():
						lol.append({"Coin" : key.title(), "Harga_awal" : value["usd"], "Harga" : value["usd"], "Change" : 0})
					tampil = copy.deepcopy(lol)
					for key in range(len(lol)):
						tampil[key].pop("Harga_awal")
					print(tabulate(tampil, headers="keys", tablefmt="grid", colalign=("left","center","right"), numalign="right"))
				last_alert = time.time()
except KeyboardInterrupt:
	print("PROGRAM SELESAI")
except requests.exceptions.InvalidURL:
	print("URL tidak valid")
except requests.exceptions.ConnectionError:
	print("Koneksi Terputus")
except requests.exceptions.Timeout:
	print("Tidak ada respons dari Server")
except requests.exceptions.HTTPError as e:
	print("ERROR code: ", response.status_code)