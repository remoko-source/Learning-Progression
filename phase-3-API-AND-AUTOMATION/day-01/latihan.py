import requests
try:
	url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
	response = requests.get(url)
	response.raise_for_status()
	k = response.json()
	for key, value in k.items():
		harga = value["usd"]
		print(key,": ", harga)
	print(k)
except requests.exceptions.ConnectionError:
	print("Koneksi Terputus")
except requests.exceptions.Timeout:
	print("Tidak ada respons dari Server")
except requests.exceptions.InvalidURL:
	print("URL tidak valid")
except requests.exceptions.HTTPError:
	print("ERROR code: ", response.status_code)
#except requests.exceptions.RequestsException = untuk semua error