from dotenv import load_dotenv ; import json
import os ; import requests
load_dotenv()
url = "https://api.coingecko.com/api/v3/simple/price"
def load_config():
	with open("config.json", "r") as file:
		data = json.load(file)
	return data
config = load_config()
api_key = os.getenv("COINGECKO_API_KEY")
coins = ["bitcoin","ethereum"]
params = {
"ids" : ",".join(config["coins"]),
"vs_currencies" : "usd"
}
response = requests.get(url, params=params)
response.raise_for_status()
data_harga = response.json()
for i, m in enumerate(config["coins"]):
	if m in data_harga.keys():
		print(f"{i+1}. {m.title():<8} : ${data_harga[m]['usd']:,}")
	else:
		print(f"{i+1}. {m.title():<8} : HARGA TIDAK ADA")