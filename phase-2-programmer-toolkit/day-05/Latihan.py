from datetime import datetime, timedelta
laihan = datetime.now()
print(laihan)
print(type(laihan))
print(laihan.strftime("%d-%m-%Y"))
print(laihan.strftime("%H:%M:%S"))
print(laihan.strftime("%A, %d %B %Y"))
latihan = "12-May-2026"
Latihan_baru= datetime.strptime(latihan, "%d-%B-%Y")
print(Latihan_baru + timedelta(hours=5, minutes=34, seconds=32))
Waktu = datetime.strptime("21 May 2025 10:34:10", "%d %B %Y %H:%M:%S")
Time = datetime.strptime("21 May 2026 13:08:12", "%d %B %Y %H:%M:%S")

wow = Time - Waktu
print(wow)
print(type(wow))