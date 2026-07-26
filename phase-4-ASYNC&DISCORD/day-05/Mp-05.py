from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
import aiohttp
from tabulate import tabulate
from datetime import datetime, timezone

load_dotenv()
URL = os.getenv("URL_COIN_API")
BOT_KEY = os.getenv("BOT_API_KEY")
#=================================================
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def fetch(url, params):
	async with aiohttp.ClientSession() as session:
		async with session.get(url, params=params) as response:
			response.raise_for_status()
			return await response.json()

class SalahFormat2(Exception):
	pass
class SalahFormat1(Exception):
	pass

async def table_maker(ctx,coins,data):
	hasil = []
	for i, coin in enumerate(coins, start=1):
		if coin not in data:
			hasil.append({"No" : i,"Coins": coin.title(), "Harga": "INVALID"})
		else:
			hasil.append({
			"No" : i,
			"Coins" : coin.title(),
			"Harga" : f'{data[coin]["usd"]}'
			})
	embed = discord.Embed(
		title = "YUM COINS",
		timestamp = datetime.now(timezone.utc),
		color = discord.Color.green()
		)
	for coin in hasil:
		embed.add_field(name=f'{coin["No"]}.{coin["Coins"]}',value= f'${coin["Harga"]}', inline=True)
	embed.set_footer(text="Data by CoinGecko ofc")
	await ctx.send(embed=embed)
		

@bot.command()
async def prices(ctx, *coin_names):
	if len(coin_names) <= 1:
		raise SalahFormat2()
	params = {
	"ids" : ",".join(coin_names),
	"vs_currencies" : "usd"
	}
	hasil = await fetch(URL,params)
	await table_maker(ctx,coin_names,hasil)
	

@bot.command()
async def price(ctx, coin_name=None):
	if coin_name is None:
		raise SalahFormat1()
	params = {
	"ids" : coin_name,
	"vs_currencies" : "usd"
	}
	hasil = await fetch(URL,params)
	await table_maker(ctx,[coin_name],hasil)

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandInvokeError):
		embed = discord.Embed(
            title = "[ERROR]",
	    	timestamp = datetime.now(timezone.utc),
	    	color = discord.Color.green()
	    	)
		if isinstance(error.original, SalahFormat1):
			embed.add_field(name="Salah Format", value="HARAP MASUKKAN DENGAN FORMAT : !price (coin)", inline=False)
		elif isinstance(error.original, SalahFormat2):
			embed.add_field(name="Salah Format", value="HARAP MASUKKAN DENGAN FORMAT : !prices (coin1 coin2 dst)", inline=False)
		embed.set_footer(text="try again.")
		await ctx.send(embed=embed)
@bot.event
async def on_message(message):
	if message.author == bot.user:
		return
	await bot.process_commands(message)

@bot.event
async def on_ready():
	print("BOT DIJALANKAN")

bot.run(BOT_KEY)