#Mini Project day 01
#Async Multi-Coin Fetcher
import asyncio ; import random ; import time
async def fetch_coin(coin_id):
	await asyncio.sleep(2)
	if coin_id == "bitcoin":
		return {coin_id : 65000}
	else:
		return {coin_id : 2000}

async def fetch_sequantial(coin_list):
	hasil = []
	for i in range(len(coin_list)):
		tambah = await fetch_coin(coin_list[i])
		hasil.append(tambah)
	return hasil

async def fetch_parallel(coin_list):
	tasks = [fetch_coin(coin_id) for coin_id in coin_list]
	hasil = await asyncio.gather(*tasks)
	return hasil

async def main():
	coins = ["bitcoin", "ethereum", "solana", "xrp", "binance"]
	random.shuffle(coins)
	mulai_seq = time.time()
	hasil_seq = await fetch_sequantial(coins)
	selesai_seq = time.time()
	
	mulai_par = time.time()
	hasil_par = await fetch_parallel(coins)
	selesai_par = time.time()
	
	print(f"Sequential: {selesai_seq - mulai_seq:.2f} detik")
	print(f"Parallel: {selesai_par - mulai_par:.2f} detik")
	
	print(f"HASIL Sequential = {hasil_seq}")
	print(f"HASIL Parallel = {hasil_par}")

asyncio.run(main())