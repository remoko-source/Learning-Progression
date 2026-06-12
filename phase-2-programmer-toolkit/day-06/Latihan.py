import logging

logger = logging.getLogger("latihan")
file = logging.FileHandler("test1.log", mode="w")
visual = logging.StreamHandler()

format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file.setFormatter(format)
visual.setFormatter(format)

logger.setLevel(logging.DEBUG)
file.setLevel(logging.INFO)
visual.setLevel(logging.WARNING)

logger.addHandler(file)
logger.addHandler(visual)

logger.info("BTC Naik 3000 USD")
logger.debug("BTC 2000,00 to 2999,99 USD")
logger.warning("kondisi API sedikit terganggu")
logger.critical("sambungan API terputus")
logger.error("API tidak ditemukan")