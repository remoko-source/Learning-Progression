#Mini Project day 6
#Mini trading logger

import logging
logger = logging.getLogger("SEMOGA_LANCAR")
logger.setLevel(logging.DEBUG)

file = logging.FileHandler("Mp.log", mode ="w")
visual = logging.StreamHandler()
file.setLevel(logging.DEBUG)
visual.setLevel(logging.INFO)

format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s",datefmt="%d/%m/%Y %H:%M:%S")
file.setFormatter(format)
visual.setFormatter(format)

logger.addHandler(file)
logger.addHandler(visual)


saldo_awal = 100000
jumlah = 0
daftar_order = [
    {"jenis": "BUY", "jumlah": 0.5, "harga": 65000},
    {"jenis": "SELL", "jumlah": 0.3},
    {"jenis": "BUY", "jumlah": 1.0, "harga": 70000},
    {"jenis": "BUY", "jumlah": 0.1, "harga": 65000},
]

for i in daftar_order:
	if i["jenis"] == "BUY":
		try:
			total = i["jumlah"] * i["harga"]
			if saldo_awal >= total:
				saldo_awal -= total
				jumlah += i["jumlah"]
				logger.info(f"Berhasil membeli coin sejumlah {i['jumlah']}")
			else:
				logger.warning(f"Saldo tidak mencukupi - {total - saldo_awal}")
		except KeyError:
			logger.error("Key tidak Lengkap")
			continue
	elif i["jenis"] == "SELL":
		try:
			if i["jumlah"] <= jumlah:
				total = i["jumlah"] * i["harga"]
				saldo_awal += total
				jumlah -= i["jumlah"]
				logger.debug(f"Berhasil menjual coin sejumlah {i['jumlah']}")
				logger.info(f"Berhasil Jual +{total}")
			else:
				logger.error("Jumlah Coin kurang")
		except KeyError:
			logger.error("Key tidak Lengkap")
			continue