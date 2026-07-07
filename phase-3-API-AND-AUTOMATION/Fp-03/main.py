#PHASE 3 Project
#Mini Market Scanner
#===============================================================
from baseline_store import get_paths, load_config, load_baseline, save_baseline
from analyzer import calculate_change, is_mover
from logger import get_logger
from fetcher import fetch_retry

from dotenv import load_dotenv
from tabulate import tabulate
import os
import copy
import sys
import time
import winsound
#===============================================================
def build_system():
	config = load_config()
	COINGECKO_API = os.getenv("COINGECKO_API_KEY")
	params = {
	"ids" : ",".join(config["coins"]),
	"vs_currencies" : ",".join(config["currencies"])}
	response = fetch_retry(config["base_url"], params, config["max_retries"], config["interval"])
	if response is None:
		logger.critical("ERROR: Fetch Gagal total")
		return (None, config)
	return (response.json(), config)

def build_table(response, config):
	baseline = load_baseline()
	new_baseline = {}
	data = []

	for key, value in response.items():
		if value is None:
			data.append({"Coins": key.title(), "Harga_Awal": "INVALID", "Harga": "INVALID", "Change": "INVALID"})
			continue

		harga_sekarang = value["usd"]
		harga_awal = baseline.get(key)

		persen = calculate_change(harga_sekarang, harga_awal)
		mover = is_mover(persen, config["mover_threshold"])
		data.append({
			"Coins": key.title(),
			"Harga_Awal": f"{harga_awal:,}" if harga_awal is not None else "N/A",
			"Harga": f"{harga_sekarang:,}",
			"Change": f"{persen:.2f}%" if persen is not None else "N/A",
			"Status": "[MOVER]" if mover else "-"
		})
		new_baseline[key] = harga_sekarang
		if mover:
			winsound.PlaySound("siren.wav", winsound.SND_FILENAME)

	print(tabulate(data, headers="keys", tablefmt="grid", colalign = ("left","center","center","center","center","right"), numalign=("right")))
	save_baseline(new_baseline)

def main():
	response = build_system()
	build_table(response[0], response[1])
	

if __name__ == "__main__":
	configu = load_config()
	start = time.time()
	last_alert = configu["last_alert"]
	durasi = configu["durasi"]
	cooldown = configu["cooldown"]
	p = 1
	print("""
===================  MINI MARKET SCANNER =================== """)
	while True:
		try:
			if time.time() - start >= durasi: 
				logger.info("PROGRAM SELESAI")
				break
			else:
				if time.time() - last_alert >= cooldown:
					winsound.Beep(1000,500)
					logger = get_logger()
					print("ITERASI KE -", p)
					main()
					last_alert = time.time()
					p += 1
		except KeyboardInterrupt:
			logger.info("PROGRAM SELESAI")
			break