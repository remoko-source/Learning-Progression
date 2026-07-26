# Phase 4 — Day 3: Discord Webhooks

## Materi Hari Ini

### 1. Webhook vs Bot
Webhook **bukan bot**. Webhook adalah URL endpoint pasif — tidak ada proses yang "hidup" di sisi Discord. Cukup kirim satu HTTP POST request, Discord otomatis memposting isinya sebagai pesan di channel.

Beda dengan Bot yang butuh proses berjalan terus-menerus (login, connect ke Gateway, dengar & balas pesan).

Analogi: webhook itu kotak surat dengan slot masuk saja — bisa dimasukkan surat kapan saja tanpa perlu ada yang berjaga di rumah.

### 2. `requests.post()` vs `requests.get()`
- `requests.get()` → **mengambil** data (dipakai sejak Phase 3 untuk fetch CoinGecko)
- `requests.post()` → **mengirim** data (dipakai hari ini untuk kirim ke Discord)

```python
response = requests.post(WEBHOOK_URL, json=payload)
```
`json=payload` otomatis mengubah dict jadi JSON string + set header yang benar, tidak perlu `json.dumps()` manual.

### 3. Kenapa Payload Harus Dictionary?
Ini bukan syarat dari `requests`, tapi **kontrak API Discord**. Discord mengharapkan JSON object dengan key tertentu:

```python
payload = {
    "content": "isi pesan",
    "username": "opsional",
    "avatar_url": "opsional"
}
```

Kalau cuma string polos, Discord tidak bisa membedakan mana isi pesan, mana nama bot, mana avatar. Dictionary memberi struktur key-value yang jelas.

### 4. Type Hint vs Konversi Tipe
`message: str` **bukan** konversi tipe — itu cuma anotasi/dokumentasi untuk pembaca kode. Python tidak memaksa ini saat runtime.

Beda dengan `str(message)` yang benar-benar mengubah nilai jadi string.

```python
def kirim(message: str):   # anotasi saja, tidak ada aksi
    ...

str(12345)  # aksi nyata, hasil: "12345"
```

### 5. Payload vs Response — Beda Arah Data
- `payload` = data yang **kita kirim** (request)
- `response` = data yang **Discord kirim balik** (hasil dari `requests.post()`)

```python
response = requests.post(WEBHOOK_URL, json=payload)
#          ^ balasan dari Discord      ^ yang kita kirim
```

### 6. Rate Limit Discord
Discord webhook punya batas kira-kira **30 request/menit**. Kalau kelewat, Discord balas status **429 (Too Many Requests)** plus `retry_after` (info berapa detik harus tunggu).

Relevan untuk nanti: kalau Market Scanner mendeteksi banyak sinyal sekaligus, berisiko kena limit. Proteksinya (retry logic dengan `time.sleep(retry_after)`) baru diimplementasikan nanti di capstone **Auto Signal Bot** — belum perlu di Mp-03 ini.

### 7. Format Specifier f-string (`:<8`, `:>8`, `:^8`)
Hanya jalan **di dalam f-string**, bukan `print(var:<8)` langsung (itu SyntaxError).

```python
f"{number:<8}"   # rata kiri, lebar 8
f"{number:>8}"   # rata kanan, lebar 8
f"{number:^8}"   # rata tengah, lebar 8
```

### 8. Kenapa Tabel Tabulate Berantakan di Discord?
`tabulate` menghasilkan tabel rapi dengan asumsi ditampilkan pakai **font monospace** (semua karakter lebar sama — seperti di Notepad++). Discord default pakai **font proporsional** (lebar karakter beda-beda), jadi tabel jadi berantakan meski di editor terlihat rapi.

**Solusi:** bungkus pesan dengan Discord markdown code block (tiga backtick):

```python
payload = {"content": f"```\n{message}\n```"}
```

Ini murni sintaks Discord (bukan Python) yang memaksa Discord merender teks dengan font monospace. Python cuma "menitipkan" instruksi format itu lewat teks — Discord yang benar-benar mengubah tampilannya.

---

## Mini Project: Signal Relay (`Mp-03.py`) — Level 🔴

### Requirement
1. Fetch harga real dari CoinGecko (bitcoin, ethereum, solana)
2. Fungsi `send_signal()` yang format pesannya rapi lalu kirim ke Discord webhook
3. 2 custom exception:
   - `CoinDataError` — gagal fetch dari CoinGecko
   - `SignalDeliveryError` — gagal kirim ke Discord
4. Alur: fetch harga → format tabel → kirim ke Discord

### Kode Final

```python
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
        "ids": ",".join(coin_name),
        "vs_currencies": "usd"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    hasil = response.json()
    return hasil

async def send_signal(data):
    try:
        dictionary = {
            "No": [],
            "Coins": [],
            "Harga": []
        }
        discord_API = os.getenv("WEBHOOK_API_URL")
        for i, (key, value) in enumerate(data.items(), start=1):
            dictionary["No"].append(f'{str(i)}.')
            dictionary["Coins"].append(f"{(key.title()):<8}")
            dictionary["Harga"].append(f'{value["usd"]:<8}')
        message = tabulate(dictionary, headers="keys", tablefmt="grid",
                            colalign=("left", "center", "right"), numalign="right")
        response = requests.post(discord_API, json={"content": f"```\n{message}\n```"})
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

coin = ["bitcoin", "ethereum", "solana"]
asyncio.run(main(coin))
```

### Bug yang Ditemukan & Diperbaiki
1. **`requests.exceptions.RequestsExcept`** (typo) → seharusnya `requests.exceptions.RequestException`
2. **Custom exception class belum didefinisikan** di draft awal → ditambahkan `class CoinDataError(Exception): pass` dan `class SignalDeliveryError(Exception): pass`
3. **`raise CustomError("text", e)`** (dua argumen terpisah koma) → jadi tuple args, bukan kalimat rapi. Diperbaiki jadi `raise CustomError(f"text: {e}")` supaya jadi satu pesan string yang jelas.
4. **Tabel berantakan di Discord** → dibungkus dengan code block Discord markdown (lihat poin 8 di atas).

### Struktur Alur
```
main()
 ├─ trial_error(coin_name)   → wrapper fetch, tangkap RequestException → raise CoinDataError
 │   └─ fetch(coin_name)     → requests.get() ke CoinGecko
 └─ send_signal(hasil)       → format tabulate + kirim webhook, tangkap RequestException → raise SignalDeliveryError
```

Exception ditangani **di dekat sumbernya** (fetch dan send terpisah), lalu di-catch di `main()` secara terpisah juga — supaya kalau ada kegagalan, jelas apakah masalahnya di fetch data atau di kirim sinyal.

### Hasil
✅ Berhasil fetch harga bitcoin, ethereum, solana dari CoinGecko dan mengirim tabel sinyal yang rapi ke channel Discord.

---

## Status
**Day 3 — SELESAI TOTAL ✅**

**Next:** Day 4 — discord.py (full bot: setup bot, event handler, intents, prefix commands), di sesi chat baru.