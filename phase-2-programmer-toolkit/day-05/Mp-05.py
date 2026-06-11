#Mini project day 5
#Activity Logger

from datetime import datetime, timedelta
waktu_pertama = None
aktivitas = ["Cek harga BTC", "Analisa chart", "Catat Sinyal"]
for i in aktivitas:
	mana = datetime.now()
	print("=============================================")
	print(f"    {mana.strftime('%d %B %Y, %H:%M:%S')} {i}")
	print("=============================================")
	input()
	if waktu_pertama is None:
		waktu_pertama = mana
waktu_terakhir = mana
waktu = waktu_terakhir - waktu_pertama
print(waktu)