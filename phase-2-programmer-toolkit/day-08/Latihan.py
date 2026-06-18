from pathlib import Path
p = Path.cwd()
try:
	if p.exists():
		print("Lol")
	else:
		p.mkdir(parents=True, exist_ok=True)
finally:
	print("Selesai")
	print(p.name) #nama dan gelar cnth Dr. Bayu
	print(p.stem) #nama cnth bayu
	print(p.suffix) #gelar Dr.
	print(p.parent) #keturunan whatsapp/bayu.dr
i = 0
p.mkdir(parents=True, exist_ok=True)
for item in p.iterdir():
	if item.is_file():
		print(f"FILE: {item.name}")
	elif item.is_dir():
		print(f"FOLDER: {item.name}")
for file in p.glob("*.py"):
	i += 1
	print(str(i)+".", "", file.name)
testing = "test.py"
p = (p) / testing
p.write_text("print('Hello World')")
print(p.read_text())
#===================================
from datetime import datetime
man = input("Masukkan nama file: ")
if man != "skip":
	k = Path.cwd() / "latihan" / man
	k.parent.mkdir(parents=True, exist_ok=True)
	k.write_text("Halo")
else:
	pass
o = Path.home()
#Change directory
while True:
	mana = input("Masukkan nama folder (atau 'stop' untuk selesai): ").lower()
	if mana == "stop":
		mana2 = input("Masukkan nama file: ")
		o = o / mana2
		break
	o = o / mana
	
o.parent.mkdir(parents=True, exist_ok=True)
o.write_text("")
dtime = o.stat().st_mtime
print(datetime.fromtimestamp(dtime))