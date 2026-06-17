#lat 1:
def validasi_order(harga, jumlah):
	try:
		a = int(harga) * int(jumlah)
		print(f"Total harga : {a}")
	except ValueError as e:
		print("Input harus angka", e)
	else:
		print(a)
		return a
	finally:
		print("Validasi Selesai")
		
validasi_order("100", "5")
validasi_order("abc","5")
validasi_order("100","xyz")

#lat 2:
def cek_saldo(saldo, total_harga):
	if total_harga > saldo:
		raise ValueError(f"Saldo tidak cukup, butuh {total_harga}, tersedia {saldo}")
	return saldo - total_harga

try:		
	so = cek_saldo(1000, 500)
	print(so)
except ValueError as e:
	print("Error :", e)
try:
	so2 = cek_saldo(1000, 1500)
	print(so2)
except ValueError as e:
	print("Error :", e)