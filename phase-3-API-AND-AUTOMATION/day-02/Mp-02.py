#FEARS AND GREEDS
import requests ; from datetime import datetime ; import logging
logger = logging.getLogger("HAHA") ; logger.setLevel(logging.DEBUG)
file = logging.FileHandler("Mp.log") ; file.setLevel(logging.INFO)

prompt = logging.Formatter("%(asctime)s|%(levelname)s %(message)s", "%Y/%m/%d - %H:%M:%S")
file.setFormatter(prompt)
logger.addHandler(file)

logger.info("PROGRAM DIJALANKAN")
url = "https://api.alternative.me/fng/?limit=7"
try:
	response = requests.get(url)
	response.raise_for_status()
	data = response.json()
	print("--------------------------------------------------")
	print(data['name'])
	print("==================================================")
	sebelum = 0
	for index,i in enumerate(data['data']):
		tanggal = int(i['timestamp'])
		tanggal = datetime.fromtimestamp(tanggal).strftime("%Y/%m/%d")
		if index == 0:
			left = int(i['time_until_update'])
			left = datetime.fromtimestamp(left).strftime("%H:%M:%S")
			print(f"{tanggal:<8} | {i['value']} | {i['value_classification']:<8} | UPDATE: {left}")
			print("--------------------------------------------------")
		else:
			print(f"{tanggal:<8} | {i['value']} | {i['value_classification']:<8}")
		sebelum += int(i['value'])
	print("--------------------------------------------------")
	logger.info("PROGRAM BERHASIL")
	rata_rata =  sebelum / len(data['data'])
	if rata_rata < 50:
		kesimpulan = "FEAR"
	elif rata_rata >= 50:
		kesimpulan = "GREED"
	print("RATA RATA: ", int(rata_rata))
	print("PASAR 7 Hari Terakhir Dominan ", kesimpulan)
	print("==================================================")

except requests.exceptions.InvalidURL:
	print("URL tidak valid")
	logger.error("URL tidak valid")
except requests.exceptions.ConnectionError:
	print("Koneksi Terputus")
	logger.error("UNABLE TO CONNECT, LOST CONNECTION")
except requests.exceptions.Timeout:
	print("Tidak ada respons dari Server")
	logger.error("ERROR: TIMEOUT")
except requests.exceptions.HTTPError as e:
	print("ERROR code: ", response.status_code)
	if response.status_code >= 500:
		logger.critical("SISTEM FRIED, TURNING OFF...")
	else:
		logger.error("HTTP Error")