import logging ; import requests
#=========================================================================================
logger = logging.getLogger("RUDI") ; logger.setLevel(logging.DEBUG)
file = logging.FileHandler("Mp.log") ; file.setLevel(logging.INFO)

prompt = logging.Formatter("%(asctime)s|%(levelname)s %(message)s", "%Y/%m/%d - %H:%M:%S")
file.setFormatter(prompt)
logger.addHandler(file)
#=========================================================================================
logger.info("SISTEM DIJALANKAN")
try:
	coins = input("Masukkan nama coin (pakai koma jika double): ").lower()
	coins = [c.strip() for c in coins.split(",")]
	url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(coins)}&vs_currencies=usd,idr"
	response = requests.get(url)
	response.raise_for_status()
	response_json = response.json()
	print()
	print("DATA BERHASIL DIAMBIL")
	logger.info("SISTEM SELESAI")
	print()
	
	for key,value in response_json.items():
		print(f"{key.upper():<8} : ${value['usd']:<8,} | Rp{value['idr']:,}")
except requests.exceptions.ConnectionError:
	print("Koneksi Terputus")
	logger.error("UNABLE TO CONNECT, LOST CONNECTION")
except requests.exceptions.Timeout:
	print("Tidak ada respons dari Server")
	logger.error("ERROR: TIMEOUT")
except requests.exceptions.InvalidURL:
	print("URL tidak valid")
	logger.error("URL tidak valid")
except requests.exceptions.HTTPError as e:
	print("ERROR code: ", response.status_code)
	if response.status_code >= 500:
		logger.critical("SISTEM FRIED, TURNING OFF...")
	else:
		logger.error("HTTP Error")