#Mini Project day 7
#Resilient Order Validator
class SaldoTidakCukupError(Exception):
	pass
class CoinTidakDitemukanError(Exception):
	pass

def validasi_transaksi(portofolio, nama_coin, saldo, harga, jumlah):
	for i in portofolio.keys():
		if nama_coin == i:
			total = jumlah * harga
			if saldo < total:
				raise SaldoTidakCukupError(f"Saldo anda tidak mencukupi, sebesar {total - saldo}")
			else:
				return total
	else:
		raise CoinTidakDitemukanError(f"Coin {nama_coin} tidak ditemukan")
		
#dummy:
portofolio = {"BTC" : 0.5, "ETH" : 2.0}
saldo = 1000

try:
	kol = validasi_transaksi(portofolio, "BTC", saldo, 500, 1)
except CoinTidakDitemukanError as e:
	print("Error: ",e)
except SaldoTidakCukupError as e:
	print("Error: ", e)
else:
	print("Berhasil! , " + str(kol))
finally:
	print("Validasi Selesai")
	
try:
	kal = validasi_transaksi(portofolio, "SOL", saldo, 100, 1)
except CoinTidakDitemukanError as e:
	print("Error: ",e)
except SaldoTidakCukupError as e:
	print("Error: ", e)
else:
	print("Berhasil! , " + str(kal))
finally:
	print("Validasi Selesai")
	
try:
	kil = validasi_transaksi(portofolio, "ETH", saldo, 2000, 1)
except CoinTidakDitemukanError as e:
	print("Error: ",e)
except SaldoTidakCukupError as e:
	print("Error: ", e)
else:
	print("Berhasil! , " + str(kil))
finally:
	print("Validasi Selesai")