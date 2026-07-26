import time
import asyncio
import random
async def ambil_harga_coin(coin_id):
	print(f"mulai fetch {coin_id}")
	await asyncio.sleep(2)
	print(f"selesai fetch {coin_id}")
	return f"{coin_id}: ${int(50000)}"

async def main():
	hasil = await asyncio.gather(
	ambil_harga_coin("HALO DUNIA"),
	ambil_harga_coin("Solana"),
	ambil_harga_coin("Bitcoin"),
	ambil_harga_coin("Ethereum"))
	print(hasil)

asyncio.run(main())
print("===================================================")
#=============================================
#LATIHAN
async def fetch_testing(moo):
	print("FETCH ME THEIR SOUL!")
	print("get :", moo)
	if moo == "bitcoin":
		return {moo : 65000, "type" : "coin langka"}
	else:
		return {moo : 5000, "type" : "coin newbie"}

async def lolol():
	print("berjalan")
	coin = ["bitcoin","ethereum","solana"]
	koo = random.choice(coin)
	print("FETCH ME THEIR SOUL!")
	print("get :", koo)
	await asyncio.sleep(2)
	if koo == "bitcoin":
		return {koo : 65000, "type" : "coin langka"}
	else:
		return {koo : 5000, "type" : "coin newbie"}

async def kk():
	k = []
	for i in range(3):
		lol = await lolol()
		k.append(lol)
	print(k)

async def blabla():
	jjj = await asyncio.gather(
	fetch_testing("bitcoin"),
	fetch_testing("ethereum"),
	fetch_testing("solana"))
	print(jjj)
async def mainn():
	await asyncio.gather(
	kk(),
	blabla())
print("===================================================")
asyncio.run(mainn())