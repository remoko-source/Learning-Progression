#Mini Project day 05 
#Resilient Multi-Coin Price Fetcher
from tabulate import tabulate
import requests
import logging
import time
#========================================================================================================
#LOG
logger = logging.getLogger("KAKAK") ; logger.setLevel(logging.DEBUG)
visual = logging.StreamHandler() ; visual.setLevel(logging.ERROR)
file = logging.FileHandler("log.log") ; file.setLevel(logging.INFO)
form = logging.Formatter("%(asctime)s - %(levelname)s | %(message)s" ,"%Y/%m/%d - %H:%M:%S")
file.setFormatter(form) ; visual.setFormatter(form); logger.addHandler(file) ; logger.addHandler(visual)
#========================================================================================================

coins = ["fih","bitcoin","ethereum"]

def res_test(url, max_retry, base_delay):
	for attempt in range(max_retry):
		try:
			response = requests.get(url)
			response.raise_for_status()
			return response
		except requests.exceptions.HTTPError as e:
			status = response.status_code
			if status in (404,401,403):
				logger.critical(f"ERROR: {status} : {e}")
				return None
			else:
				logger.error(f"ERROR: {e}")
				time.sleep(base_delay *(2 ** attempt))
		except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
			logger.error(f"ERROR: {e}")
			print("MEMULAI ULANG...")
			time.sleep(base_delay *(2 ** attempt))
	return None

def reh_test(coins, max_retry, base_delay):
	url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(coins)}&vs_currencies=usd,idr"
	response = res_test(url, max_retry, base_delay)
	if response is None:
		return {coin: None for coin in coins}
	responses = response.json()
	return {coin: responses.get(coin) for coin in coins}
#TESTING:
test = reh_test(coins, 3, 5)
tabel = []
for key, value in test.items():
	if value is None:
		logger.error(f"GAGAL: {key.title()}")
		tabel.append({"Coin" : key.upper(), "Harga" : "ERROR", "INDONESIA" : "ERROR"})
	else:
		logger.info(f"BERHASIL: {key.title()}")
		tabel.append({"Coin" : key.title(), "Harga" : f'{value["usd"]:,}', "INDONESIA" : f'{value["idr"]:,}'})
print(tabulate(tabel, headers="keys", tablefmt="grid", colalign=("left","center","right"), numalign="right"))