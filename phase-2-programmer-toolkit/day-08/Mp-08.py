#Mini Project day 8
#PathScout
from pathlib import Path
import sys
import logging
class PathNotFoundError(Exception):
	pass
#python Mp-08.py lopu
logger = logging.getLogger("Bayu")
logger.setLevel(logging.DEBUG)

file = logging.FileHandler("PathScout.log")
file.setLevel(logging.INFO)

visual = logging.StreamHandler()
visual.setLevel(logging.ERROR)

format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt=("%d %m %Y %H:%M:%S"))
file.setFormatter(format)
visual.setFormatter(format)

logger.addHandler(file)
logger.addHandler(visual)

p = Path(sys.argv[1])
try:
	if p.exists():
		logger.info("Ditemukan")
		if p.is_file():
			logger.info(f"Ekstensi berbentuk File: {p.name}")
			print("Nama file: ",p.name)
			print("Ekstensi: ",p.suffix)
			print("File berukuran: ",p.stat().st_size, " KB")
			print("Isi file: ",p.read_text())
		elif p.is_dir():
			logger.info(f"Ekstensi berbentuk Folder: {p.name}")
			folder_jumlah = 0
			file_jumlah = 0
			print("=================")
			for item in p.iterdir():
				if item.is_file():
					print("FILE:")
					file_jumlah += 1
					print(item.name)
					print("=================")
				elif item.is_dir():
					print("FOLDER:")
					folder_jumlah += 1
					print(item.name)
					print("=================")
			print("Jumlah subfolder: ", folder_jumlah)
			print("Jumlah file: ", file_jumlah)
			logger.info(f"Isi file berjumlah: {file_jumlah}")
			logger.info(f"Isi folder berjumlah: {folder_jumlah}")
	else:
		logger.critical("Path tidak ditemukan, Sistem selesai.")
		raise PathNotFoundError("ERROR: Lokasi tidak ditemukan")
except PathNotFoundError as e:
	print(e)