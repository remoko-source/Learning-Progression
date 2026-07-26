import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("BOT_API_KEY")
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def emb(ctx):
    embed = discord.Embed(
        title="HALO",
        description="pesan berisi deskripsi",
        color=discord.Color.blurple()
    )
    label = "YAP"
    teks = "Program ini bertujuan untuk mengembangkan kemampuan anda dalam pengetahuan teknlogi. belakangan ini, banyak isu mengenai blablablabla. oleh karena itu dengan adanya program ini, akan membantu anda lebih memahami materi yang disampaikan, contohnya materi embed yang saya sedang buat sekarang ini."
    label2 = "YIP"
    taks = "YA BEGITULAH, intinya seperti itu. jika anda bisa membaca ini, maka program BERHASIL!!"
    embed.add_field(name=label, value=teks,inline=True)
    embed.add_field(name=label2, value=taks, inline=False)
    embed.add_field(name="pesan", value="sinkat", inline=True)
    embed.add_field(name="singkat", value="person", inline=True)
    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    print("HASU")

bot.run(token)
