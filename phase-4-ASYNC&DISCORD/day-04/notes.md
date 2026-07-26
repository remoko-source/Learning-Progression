# Phase 4 — Day 4: discord.py (Full Bot) 🔴

## Tujuan Hari Ini
Naik level dari webhook (kirim satu arah, Day 3) ke **bot yang online 24 jam**, bisa dengar & bereaksi ke pesan/command secara dua arah.

---

## 1. Setup Bot di Discord Developer Portal

Langkah manual (bukan kode) sebelum bisa coding:

1. https://discord.com/developers/applications → **New Application**
2. Tab **Bot** → Reset Token → copy (simpan di `.env`, JANGAN commit ke Git)
3. Aktifkan **Message Content Intent** di "Privileged Gateway Intents" (wajib, tanpa ini bot gak bisa baca isi pesan)
4. Tab **OAuth2 → URL Generator** → centang scope `bot`, permission `Send Messages`, `Read Message History`, `View Channel`
5. Buka URL yang di-generate → invite bot ke server testing

⚠️ Bot token = akses penuh ke bot. Beda dari webhook URL yang cuma bisa kirim pesan doang.

---

## 2. Kerangka Dasar Bot

```python
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # wajib buat baca isi pesan

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot berhasil online sebagai {bot.user}")

bot.run(TOKEN)
```

**Kenapa `commands.Bot`, bukan `discord.Client`?**
`commands.Bot` sudah include sistem command bawaan — dari awal langsung pakai ini biar gak perlu refactor nanti.

---

## 3. Event Handler — Konsep Inti

`on_ready`, `on_message`, dll itu **nama wajib**, dikenali otomatis oleh `discord.py`. Kamu **tidak pernah manggil** fungsi ini sendiri — library yang manggil otomatis saat event terjadi (mirip bel pintu otomatis, bukan bel yang kamu bunyiin sendiri).

Urutan proses `on_ready`:
1. `bot.run(TOKEN)` → trigger asyncio buka koneksi WebSocket ke Discord
2. Handshake (login → connect → session established)
3. Begitu selesai, `discord.py` otomatis panggil `on_ready`

### Event Relevan untuk Trading Bot

| Event | Kapan jalan | Kegunaan |
|---|---|---|
| `on_ready` | Sekali, saat bot connect | Start scheduler/background task |
| `on_message` | Setiap ada pesan baru | Fondasi command manual |
| `on_command_error` | Command error/salah format | Kasih feedback jelas ke user |
| `on_disconnect` | Koneksi putus | Logging untuk bot 24 jam |
| `on_resumed` | Koneksi nyambung lagi | Pasangan `on_disconnect` |

Skip: `on_member_join`, `on_reaction_add`, `on_voice_state_update` — gak relevan buat trading bot.

---

## 4. `on_message` Manual — Dua Bug Klasik

```python
@bot.event
async def on_message(message):
    if message.author == bot.user:   # BUG 1 fix: cegah infinite loop
        return
    
    if message.content == "ping":     # ambil isi teks lewat .content
        await message.channel.send("pong")
    
    await bot.process_commands(message)  # BUG 2 fix: wajib, atau command gak kedetect
```

**Bug 1 — Infinite loop:** Bot ikut "dengar" pesannya sendiri. Tanpa `if message.author == bot.user: return`, bot bisa balas pesannya sendiri berulang-ulang tanpa henti.

**Bug 2 — Command gak kedetect:** `on_message` **override** default behavior deteksi command. Tanpa `await bot.process_commands(message)` di akhir, semua `@bot.command()` gak akan pernah kepanggil — dan gak ada error, bot cuma "diem aja".

**Bug 3 — `command_prefix=""`:** Prefix kosong bikin SEMUA pesan dianggap "mungkin command" → spam error `CommandNotFound`. Selalu pakai prefix jelas (`"!"`).

---

## 5. Sistem Command Formal — `@bot.command()`

Lebih rapi dari `on_message` manual untuk banyak command.

```python
@bot.command()
async def ping(ctx):
    await ctx.send("pong")
```

| `on_message` manual | `@bot.command()` |
|---|---|
| Parameter `message` | Parameter `ctx` (context) |
| `message.channel.send()` | `ctx.send()` |
| Nama fungsi bebas | Nama fungsi = nama command |

⚠️ **Typo klasik:** `@bot.commands()` (pakai s) ≠ `@bot.command()`. `bot.commands` (dengan s) adalah **attribute** berupa `set` (daftar command terdaftar), bukan method. Manggil `bot.commands()` → `TypeError: 'set' object is not callable`.

⚠️ **Penting:** `on_message` dan `@bot.command()` adalah **dua event yang jalan paralel**, tidak saling menggantikan otomatis. Kalau ada logic lama di `on_message`, harus dihapus manual — nambah command baru gak otomatis "mematikan" logic lama.

---

## 6. Command dengan Argumen

**Argumen tunggal:**
```python
@bot.command()
async def price(ctx, coin_name):
    await ctx.send(f"Harga {coin_name}")
```

**Argumen fleksibel (`*args`) — untuk jumlah gak tetap:**
```python
@bot.command()
async def prices(ctx, *coin_names):
    # coin_names jadi tuple: ("bitcoin", "ethereum", "solana")
    await ctx.send(f"{coin_names}")
```

`*coin_names` menampung **berapa pun** argumen jadi satu tuple — beda dari `coin1, coin2` yang slotnya terbatas dan bakal error `MissingRequiredArgument` kalau kurang/lebih.

---

## 7. Error Handling Command

```python
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Argumen kurang! Contoh: `!price bitcoin`")
    elif isinstance(error, commands.CommandInvokeError):
        if isinstance(error.original, SalahFormat1):
            await ctx.send("Format salah!")
    else:
        await ctx.send("Terjadi error, coba lagi.")
```

Pola `isinstance()` ini sama seperti custom exception di Phase 2/3 — bedanya sekarang error datang dari `discord.py`, bukan buatan sendiri.

⚠️ **Gotcha:** `MissingRequiredArgument` sudah fired **sebelum** command body dieksekusi. Jadi guard manual seperti `if not coin_name: raise SalahFormat1()` **tidak akan pernah tercapai** untuk kasus argumen kosong — karena discord.py sudah cegat duluan sebelum masuk fungsi.

---

## 8. `aiohttp` — Async HTTP Request

**Kenapa gak pakai `requests` biasa?**
`requests.get()` itu **blocking**, walau ditaruh di dalam `async def`. Selama request jalan, **seluruh bot freeze** — user lain gak bisa dapat respon apapun. `aiohttp` didesain non-blocking, cocok untuk Discord bot yang harus tetap responsif ke banyak user.

**GET:**
```python
async def fetch(url, params):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            response.raise_for_status()
            return await response.json()
```

**POST:**
```python
async def send_to_discord(webhook_url, contents):
    payload = {"content": contents}
    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, json=payload) as response:
            response.raise_for_status()
            # skip response.json() — webhook Discord sering return 204 No Content
```

⚠️ **Wajib** `params=params` (keyword argument), bukan `session.get(url, params)` — kalau tanpa nama, Python anggap itu positional argument yang salah slot.

`async with` bersarang: buka `ClientSession` dulu (kayak buka "kantor cabang"), baru `session.get()/.post()` (kirim satu request lewat situ). Dua-duanya perlu "ditutup" otomatis, makanya pakai `async with`.

---

## Mp-04 "Live Price Bot" 🔴🔴

### Spesifikasi
- `!price <coin>` — fetch harga satu coin
- `!prices <coin1> <coin2> ...` — fetch banyak coin sekaligus (pakai `*args`)
- Batching: satu request ke CoinGecko (`ids=","-joined`), bukan `gather()` per-coin
- Custom exception `SalahFormat1`/`SalahFormat2` + `on_command_error` kirim pesan jelas ke Discord
- **Hard constraint:** partial failure (satu coin invalid) gak boleh gagalkan seluruh command

### Bug Kunci yang Ditemukan & Solusi

**Bug: `ctx` tidak dikenal di `table_maker`**
```python
async def table_maker(data):
    ...
    await ctx.send(hasil)  # NameError! ctx gak ada di parameter fungsi ini
```
Fix: kirim `ctx` sebagai parameter eksplisit, bukan berharap ia "ikutan" otomatis dari fungsi pemanggil.

**Bug konsep: Deteksi coin invalid**

CoinGecko **tidak** mengembalikan key dengan value `None` untuk coin yang gak exist — key itu **hilang total** dari response.

```python
# SALAH — loop dari hasil API, coin invalid gak akan pernah kedeteksi
for key, value in data.items():
    if key is None:  # never True, karena key invalid gak pernah ADA di data
        ...
```

```python
# BENAR — loop dari INPUT USER, cek keberadaannya di data
for i, coin in enumerate(coin_names, start=1):
    if coin not in data:
        hasil.append({"No": i, "Coins": coin.title(), "Harga": "INVALID"})
    else:
        hasil.append({"No": i, "Coins": coin.title(), "Harga": data[coin]["usd"]})
```

**Prinsip:** kalau mau tau semua yang diminta (termasuk yang gagal), loop harus berdasarkan **input**, bukan **hasil** — karena yang gagal itu "tidak ada" di hasil, jadi gak akan pernah muncul kalau loop dari situ.

### Final Kode (Mp-04.py)

```python
from dotenv import load_dotenv
from tabulate import tabulate
from discord.ext import commands
import os
import discord
import aiohttp

load_dotenv()
WEBHOOK = os.getenv("WEBHOOK_API_URL")
URL = os.getenv("URL_COIN_API")
BOT_KEY = os.getenv("BOT_API_KEY")

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

async def table_maker(ctx, coins, data):
    hasil = []
    for i, coin in enumerate(coins, start=1):
        if coin not in data:
            hasil.append({"No": i, "Coins": coin.title(), "Harga": "INVALID"})
        else:
            hasil.append({"No": i, "Coins": coin.title(), "Harga": f'{data[coin]["usd"]}'})
    
    contents = tabulate(hasil, headers="keys", tablefmt="grid", colalign=("left","center","right"))
    async with aiohttp.ClientSession() as session:
        async with session.post(WEBHOOK, json={"content": f"```\n{contents}\n```"}) as response:
            response.raise_for_status()

@bot.command()
async def prices(ctx, *coin_names):
    if len(coin_names) <= 1:
        raise SalahFormat2()
    params = {"ids": ",".join(coin_names), "vs_currencies": "usd"}
    hasil = await fetch(URL, params)
    await table_maker(ctx, coin_names, hasil)

@bot.command()
async def price(ctx, coin_name):
    if not coin_name:
        raise SalahFormat1()
    params = {"ids": coin_name, "vs_currencies": "usd"}
    hasil = await fetch(URL, params)
    await table_maker(ctx, [coin_name], hasil)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        if isinstance(error.original, SalahFormat1):
            await ctx.send("HARAP MASUKKAN DENGAN FORMAT : !price (coin)")
        elif isinstance(error.original, SalahFormat2):
            await ctx.send("HARAP MASUKKAN DENGAN FORMAT : !prices (coin1 coin2 dst)")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

@bot.event
async def on_ready():
    print("BOT DIJALANKAN")

bot.run(BOT_KEY)
```

---

## Key Takeaways Hari Ini

- Event handler (`on_ready`, `on_message`) dipanggil otomatis oleh library, bukan manual
- Dua event bisa jalan paralel tanpa saling menggantikan — bersihkan logic lama secara eksplisit
- `MissingRequiredArgument` fired sebelum command body jalan — guard manual gak akan tercapai untuk kasus itu
- `aiohttp` wajib untuk operasi network di Discord bot, karena `requests` blocking bikin bot freeze
- Saat mendeteksi data yang "hilang" dari API, loop harus berbasis **input**, bukan **output**

---

## Status Roadmap

Phase 4: Day 1 ✅ | Day 2 ✅ | Day 3 ✅ | Day 4 ✅ + Mp-04 ✅

**Next:** Day 5 (materi belum ditentukan) atau lanjut ke capstone **Auto Signal Bot** — konfirmasi di sesi chat baru.