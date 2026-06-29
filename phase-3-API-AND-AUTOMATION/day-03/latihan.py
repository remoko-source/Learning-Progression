import time , winsound ; from datetime import datetime
i = 0
while True:
	try:
		i += 1
		if i == 10:
			print("SELESAI")
			winsound.Beep(5000, 500)
			break
		print("TESTING", "[",i,"]")
		winsound.Beep(1000, 200)
		for m in range(i):
			winsound.Beep(3000, 500)
		winsound.Beep(1000, 200)
		time.sleep(0.5)
	except KeyboardInterrupt:
		print("SELESAI")
		break
		
start = time.time()
last_alert = 0
durasi = 10
while True:
	try:
		if time.time() - last_alert >= durasi:
			print("Waktu Habis")
			winsound.Beep(1000, 500)
			last_alert = time.time()
	except KeyboardInterrupt:
		print("SELESAI")
		break