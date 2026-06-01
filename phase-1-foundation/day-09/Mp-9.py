#Mini Project day 9
#Crypto Trading Simulator

class Wallet:
 def __init__(self, nama_trader, saldo):
  self.trader = nama_trader
  self.__saldo = saldo
  
 def deposit(self, saldo):
  self.__saldo += saldo
  print("======================================================================")
  print(f"Deposit sebesar {saldo} berhasil, Total saldo sekarang : Rp.{self.__saldo}")
  print("======================================================================")
 def withdraw(self, saldo):
  if saldo > self.__saldo :
   print("Saldo Tidak Mencukupi")
  else:
   self.__saldo -= saldo
   print(f"Berhasil mengambil saldo sebesar Rp.{saldo}")
 def info(self):
  print("==============================")
  print(f"1. Nama Trader : {self.trader}")
  print(f"2. Total Saldo : {self.__saldo}")
  print("==============================")
  print()
 def get_saldo(self):
  return self.__saldo
 
class Crypto:
 def __init__(self, coin, harga):
  self.coin = coin
  self.__harga = harga
  self.__hargi = harga
 def update_harga(self,harga):
  self.__hargi = harga
  print(f"Harga Baru : {self.__hargi}")
 def info(self):
  print("==============================")
  print(f"1. Nama Coin: {self.coin}")
  print(f"2. Harga Coin: {self.__hargi}")
  print("==============================")
 def get_harga(self):
  return self.__harga
 def get_hargi(self):
  return self.__hargi
class Portofolio(Wallet):
 def __init__(self, nama_trader, saldo):
  super().__init__(nama_trader, saldo)
  self.coins = []
 def beli(self, crypto, total):
    harga_awal = crypto.get_harga()
    harga_sekarang = crypto.get_hargi()
    total_harga = harga_sekarang * total
    if total_harga > self.get_saldo():
     print("Saldo tidak mencukupi")
    else :
     print("====================================================")
     self.withdraw(total_harga)
     self.coins.append({"nama" : crypto.coin, "jumlah" : total})
     print(f"Coin {crypto.coin} berhasil dibeli sejumlah {total}")
     print("====================================================")
     print()
    
 def cek_portofolio(self):
  print("==============================")
  print(f"1. Nama Trader : {self.trader}")
  print(f"2. Total Saldo : {self.get_saldo()}")
  for i, coin in enumerate(self.coins):
   print(f"{i+3}. {coin['nama']} = {coin['jumlah']}")
  print("==============================")
  print()
 def laba(self, crypto):
  harga_awal = crypto.get_harga()
  harga_sekarang = crypto.get_hargi()
  persen  = ((harga_awal - harga_sekarang)/ harga_awal) * 100
  if persen > 0 :
      print(f"Profit +{persen:.2f}%")
  elif persen < 0:
  	print(f"Rugi -{persen:.2f}%")
  else:
  	print("Seimbang")
 def jual(self, crypto, total):
  harga_awal = crypto.get_harga()
  harga_sekarang = crypto.get_hargi()
  for coin in self.coins:
   if coin["nama"] == crypto.coin:
    if coin["jumlah"] > total :
      uang = (coin["jumlah"] - total) * harga_sekarang
      self.deposit(uang)
      coin["jumlah"] -= total
      print(f"Aset {crypto.coin} berhasil dijual seharga {uang}")
    else: 
     print("Jumlah coin Kurang untuk dijual") 


btc = Crypto("BTC", 50000)
eth = Crypto("ETH", 3000)

user1 = Portofolio("Reykhandi", 1000000)
user2 = Portofolio("Claude", 9999999)

user2.deposit(200000)
user1.info()
eth.info()
eth.update_harga(45000)
eth.info()

user1.beli(btc, 2)
user1.beli(eth, 5)
user2.beli(btc, 100)

user2.info()
user1.info()
user1.jual(btc, 1)
user1.info()