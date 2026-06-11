#Mini Project Bonus!
#Time Comparator
from datetime import datetime, timedelta
candle_buka = "11-06-2026 14:00:00"
sekarang_simulasi = "11-06-2026 14:30:00"
candle = datetime.strptime(candle_buka, "%d-%m-%Y %H:%M:%S")
waktu = datetime.strptime(sekarang_simulasi, "%d-%m-%Y %H:%M:%S")
candle_baru = candle + timedelta(hours=1)
if waktu >= candle_baru:
 print("Candle baru sudah dibentuk")
else:
 print(f"Masih dalam candle yang sama, Sisa waktu : {waktu-candle}")