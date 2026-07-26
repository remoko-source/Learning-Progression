import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from tabulate import tabulate
from datetime import datetime,timedelta, timezone
import scanner
import asyncio
import time
import json
import os
from logger import get_logger
load_dotenv()
async def get_config():
	with open("config.json", "r") as file:
		return json.load(file)

BOT_KEY = os.getenv("BOT_API_KEY")
CHANNEL_ID = int(os.getenv("BOT_CHANNEL_ID"))
DEMO_KEY = os.getenv("COINGECKO_API_KEY")
baseline = {}
cooldown_until = {}
logger = get_logger()
i = 0

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
async def embed_post(embed):
	embed.set_footer(text="Data by CoinGecko")
	channel = bot.get_channel(CHANNEL_ID)
	await channel.send(embed=embed)

@tasks.loop(seconds=240)
async def scanner_loop():
	try:
		global i
		i += 1
		config = await get_config()
		hasil = await asyncio.to_thread(
			scanner.fetch_prices,
			config["coins"],
			config["currencies"],
			DEMO_KEY,
			config["max_retry_attempts"],
			config["interval_seconds"]
			)
			
		if hasil is None:
			logger.warning(f"Fetch gagal di iterasi {i}, skip iterasi ini")
			return
		if i == 1:
			for key, value in hasil.items():
				scanner.update_state(key, value["usd"], baseline)
		else:
			trigger = {}
			for key, value in hasil.items():
				trigger[key] = scanner.cek_trigger(key, value["usd"], baseline, cooldown_until, config["threshold_percent"])
				scanner.update_state(key, value["usd"], baseline)
			if any(value["trigger"] for value in trigger.values()):
				semua_persen = [float(v["perubahan_persen"].replace("%","")) for v in trigger.values() if v["trigger"]]
				
				ada_kenaikan = any(p > 0 for p in semua_persen)
				ada_penurunan = any(p < 0 for p in semua_persen)
				
				if ada_kenaikan and not ada_penurunan:
					color = discord.Color.gold()
				elif ada_penurunan and not ada_kenaikan:
					color = discord.Color.red()
				else:
					color = discord.Color(0xC0C0C0)
				
				embed = discord.Embed(
					title = "DAFTAR COINS",
					timestamp = datetime.now(timezone.utc),
					color = color
					)

				for key,value in trigger.items():
					if value["trigger"]:
						persen_float = float(value["perubahan_persen"].replace("%",""))
						prefix = "[UP]" if persen_float > 0 else "[DOWN]" if persen_float < 0 else "[FLAT]"
						embed.add_field(name=f"{prefix} {key.upper()}", value=f'Mover: {value["perubahan_persen"]}\nHarga: ${hasil[key]["usd"]}', inline=True)
						cooldown_until[key] = datetime.now(timezone.utc) + timedelta(minutes=config["cooldown_minutes"])
				await embed_post(embed)
			else:
				logger.info(f"Iterasi {i}: tidak ada yang trigger")
			put = []
			for key, value in trigger.items():
				put.append({
				"Coins" : key,
				"Harga" : hasil[key]["usd"],
				"Trigger" : value["trigger"],
				"Persenan" : value["perubahan_persen"]})
			print(tabulate(put, headers="keys", tablefmt="grid", colalign=("left","center","center","right")))
	except ValueError as e:
		logger.critical(f"Config error, bot dihentikan: {e}")
		await bot.get_channel(CHANNEL_ID).send(f"BOT Berhenti: {e}")
		scanner_loop.stop()
		return
	except KeyboardInterrupt:
		scanner_loop.stop()
		return

@bot.command()
async def price(ctx, coin):
	try:
		config = await get_config()
		hasil = await asyncio.to_thread(
		scanner.fetch_prices,
		[coin.lower()],
		config["currencies"],
		DEMO_KEY,
		config["max_retry_attempts"],
		config["interval_seconds"]
		)
	except ValueError:
		await ctx.send(f"Coin `{coin}` tidak dikenali. Coba cek penulisan Contoh: `!price bitcoin`")
		
	if hasil is None:
		await ctx.send("Gagal mengambil harga, Coba lagi.")
		return
		
	embed = discord.Embed(
		title = f"{coin.title()}",
		timestamp = datetime.now(timezone.utc),
		color = discord.Color.blurple()
	)
	if coin not in hasil.keys:
		embed.add_field(name="Coin tidak ada", inline=True)
		
	else:
		if len(hasil[coin]) >= 2:
			embed.add_field(name="Harga IDR:", value=f"Rp{hasil[coin]['idr']:,}", inline=True)
			embed.add_field(name="Harga USD:", value=f"${hasil[coin]['usd']:,}", inline=True)
			
		else:
			embed.add_field(name="Harga USD:", value=f"${hasil[coin]['usd']:,}", inline=False)
			
	await embed_post(embed)

@bot.command()
async def status(ctx):
	config = await get_config()
	
	embed = discord.Embed(
		title="- BOT STATUS -",
		description=f"Live Coins pricing BOT, dijalankan pada {start}",
		color = discord.Color.blue())
	
	embed.add_field(name="Coin yang terpantau:",value=f"{', '.join(coin.title() for coin in config['coins'])} \n", inline=True)
	jarona = "\n".join(f"{i}. {key.title()} : ${value:,}" for i, (key, value) in enumerate(baseline.items(), start=1))
	embed.add_field(name="Baseline Terakhir", value=jarona, inline=False)
	cooldown_text = ""
	not_cooldown_text = ""
	for i, coin in enumerate(config["coins"], start=1):
		waktu_cooldown = cooldown_until.get(coin)
		
		if waktu_cooldown is not None and waktu_cooldown > datetime.now(timezone.utc):
			sisa = waktu_cooldown - datetime.now(timezone.utc)
			menit, detik = divmod(int(sisa.total_seconds()), 60)
			cooldown_text += f'{i}. {coin.title()}, waktu tersisa : {menit:02d}:{detik:02d}\n'
			
		else:
			not_cooldown_text += f'{i}. {coin.title()}\n'
			
	if cooldown_text == "":
		cooldown_text = "Tidak ada"
		
	if not_cooldown_text == "":
		not_cooldown_text = "Semua coin sedang Cooldown"
		
	embed.add_field(name="\nSedang Cooldown", value=f'{cooldown_text}', inline = False)
	embed.add_field(name="\nSiap Trigger", value=f'{not_cooldown_text}', inline = False)
	await embed_post(embed)
	
@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("Argumen kurang. Cth : `!price bitcoin`")
	elif isinstance(error, commands.CommandNotFound):
		await ctx.send("Command tidak ada, coba `!price` atau `!status`")
	elif isinstance(error, commands.BadArgument):
		await ctx.send("Argumen tidak valid")
	else:
		logger.error(f"Unhandled command error: {error}")
		await ctx.send(f"Terjadi error yang tidak tersedia, Silahkan cek log.")

@bot.event
async def on_ready():
	scanner_loop.start()

if __name__ == "__main__":
	start = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
	bot.run(BOT_KEY)