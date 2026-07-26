#Mini Project day 2
#Resilient Multi-Coin Fetcher
import asyncio ; import random ; from tabulate import tabulate ; import time
async def fetch_coin(nama_coin):
	await asyncio.sleep(1)
	if nama_coin == "scam_coin":
		raise ValueError("COIN SCAM")
	return {"Coin": nama_coin, "Status": "Success", "Price": 65000, "Keterangan" : "AMAN"}
	
async def handling(nama_coin):
	try:
		hasil = await fetch_coin(nama_coin)
		return hasil
	except ValueError as e:
		return {"Coin": nama_coin, "Status": "Failed", "Price" : 0 , "Keterangan": str(e)}
		
async def kerja():
	coins = ["bitcoin", "ethereum", "solana", "scam_coin", "binance"]
	random.shuffle(coins)
	task = []
	for i in coins:
		tasks = asyncio.create_task(handling(i))
		task.append(tasks)	
		
	hasil = await asyncio.gather(*task)
	return hasil
	
async def main():
	hasil = await kerja()
	print(tabulate(hasil, headers="keys", tablefmt="grid", colalign=("left","center","center","right"), numalign="right"))
	
start = time.time()
asyncio.run(main())
print(f"Waktu : {time.time() - start:.2} detik")