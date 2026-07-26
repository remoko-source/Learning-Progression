import asyncio

async def coin_fetch(coin_name):
	print(f"Mulai Fetch {coin_name}")
	await asyncio.sleep(2)
	
	if coin_name == "Invalid_Coin":
		raise ValueError(f"Coin {Invalid_Coin} Tidak ada")
	
	return f"{coin_name} : 50,000"

async def handling(coin_name):
	try:
		hasil = await coin_fetch(coin_name)
		return hasil
	except ValueError as e:
		print(f"Gagal Fetch : {e}")
		return None

async def main():
	hasil = await asyncio.gather(
	coin_fetch("Bitcoin"),
	coin_fetch("Invalid_Coin")
	)
	print(hasil)
	
asyncio.run(main())