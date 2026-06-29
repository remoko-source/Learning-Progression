#BTC ALERT BOT
import time
import winsound
import requests
levels = {
"WARNING" : {"min" : 65000, "max" : 70000, "freq": 500},
"DANGER" : {"min" : 60000, "max" : 65000, "freq": 1000},
"CRITICAL" : {"min" : 0, "max" : 60000, "freq": 2000}
}

try:
	url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd,idr"
	start = time.time()
	last_alert = 0
	durasi = 999999999
	cooldown = 60
	print("========================================")
	print("              BTC ALERT BOT")
	print("========================================")
	i = 0
	while True:
		if time.time() - start >= durasi:
			print("              SESI SELESAI")
			print("========================================")
			break
		else:
			if time.time() - last_alert >= cooldown:
				i += 1
				response = requests.get(url)
				response = response.json()
				harga = response['bitcoin']['usd']
				for level, config in levels.items():
					if config["min"] <= harga < config["max"]:
						print(f"{i}.[{level}] HARGA: {harga}")
						winsound.Beep(config["freq"], 500)
						print("----------------------------------------")
				last_alert = time.time()
		time.sleep(0.1)
except KeyboardInterrupt:
	print("PROGRAM SELESAI")
	print("========================================")