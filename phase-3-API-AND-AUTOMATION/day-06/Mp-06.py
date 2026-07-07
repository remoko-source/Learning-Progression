#Mini Project day 6
#Resilient Market Config Tracker
import time
import logging
from tabulate import tabulate
from dotenv import load_dotenv
import json
import os
import requests

#=======================================================================================
def get_logger():
	logger = logging.getLogger("Mini") ; logger.setLevel(logging.DEBUG)
	file = logging.FileHandler("Mp.log") ; file.setLevel(logging.INFO)
	visual = logging.StreamHandler() ; visual.setLevel(logging.ERROR)

	form = logging.Formatter("%(asctime)s - %(levelname)s|%(message)s","%Y/%m/%d %H:%M:%S")
	file.setFormatter(form) ; visual.setFormatter(form)

	logger.addHandler(file)
	logger.addHandler(visual)
	return logger
logger = get_logger()
#=======================================================================================
def load_config():
	with open("config.json","r") as file:
		data = json.load(file) 
	return data
def fetch_retry(url, params, max_retry, interval):
	for i in range(max_retry):
		try:
			response = requests.get(url, params=params)
			response.raise_for_status()
			return response
		except requests.exceptions.HTTPError as e:
			status = response.status_code
			if status in (401,403,404):
				logger.critical(f"CRITICAL: {e}")
				break
			else:
				logger.error(f"ERROR: {e}")
				time.sleep((i+1)*interval)
		except (requests.exceptions.ConnectionError,requests.exceptions.Timeout) as e:
			logger.error("ERROR: ",e)
			time.sleep((i+1)*interval)
	return None

def build_table(config, data_harga):
	tabel = []
	for key, value in data_harga.items():
		if value == None:
			tabel.append({"Coins" : key.title(), "Harga" : "ERROR", "Harga Rp" : "ERROR"})
		else:
			tabel.append({"Coins" : key.title(), "Harga" : value["usd"], "Harga Rp" : value["idr"]})
	print(tabulate(tabel, headers="keys", tablefmt="grid", colalign=("left", "center", "right"), numalign="left"))

def main():
	GECKO_API = os.getenv("COINGECKO_API_KEY")
	url = "https://api.coingecko.com/api/v3/simple/price"
	config = load_config()
	params = {
	"ids" : ",".join(config["coins"]),
	"vs_currencies":",".join(config["currencies"])}
	response = fetch_retry(url, params, config["max_retries"], config["check_interval_seconds"])
	if response is None:
		logger.critical("REQUESTS GAGAL TOTAL")
		return
	hasil_fetch = response.json()
	result = {coin : hasil_fetch.get(coin) for coin in config["coins"]}
	build_table(config, result)
if __name__ == "__main__":
	main()