#Mini Project day 03
#Signal Relay
from tabulate import tabulate
from dotenv import load_dotenv
import os
import requests
import asyncio

load_dotenv()
class SignalDeliveryError(Exception):
	pass
class CoinDataError(Exception):
	pass

async def fetch(coin_name):
	url = os.getenv("URL_COIN_API")
	params = {
	"ids" : ",".join(coin_name),
	"vs_currencies" : "usd"}
	response = requests.get(url, params=params)
	response.raise_for_status()
	hasil = response.json()
	return hasil
	
async def send_signal(data):
	try:
		dictionary = {
		"No" : [],
		"Coins" : [],
		"Harga" : []
		}
		discord_API = os.getenv("WEBHOOK_API_URL")
		for i, (key, value) in enumerate(data.items(), start=1):
			dictionary["No"].append(f'{str(i)}.')
			dictionary["Coins"].append(f"{(key.title()):<8}")
			dictionary["Harga"].append(f'{value["usd"]:<8}')
		message = tabulate(dictionary, headers="keys", tablefmt="grid", colalign=("left","center","right"), numalign="right")
		response = requests.post(discord_API, json={"content" : f"```\n{message}\n```"})
		response.raise_for_status()
		print("berhasil")
	except requests.exceptions.RequestException as e:
		raise SignalDeliveryError(f"ERROR DISCORD : {e}")
	
	
async def trial_error(coin_name):
	try:
		hasil = await fetch(coin_name)
		return hasil
	except requests.exceptions.RequestException as e:
		raise CoinDataError(f"ERROR COIN: {e}")

async def main(coin_name):
	try:
		hasil = await trial_error(coin_name)
		discord = await send_signal(hasil)
	except SignalDeliveryError as e:
		print(e)
	except CoinDataError as e:
		print(e)

coin = ["bitcoin","ethereum","solana"]
asyncio.run(main(coin))
