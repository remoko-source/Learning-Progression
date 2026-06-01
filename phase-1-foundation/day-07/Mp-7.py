#Mini Project day 7
#Crypto Tracker
import os
ALHAMDULILLAH_KANG = True
portofolio ={
"BTC":{
"Harga_Beli":105000,
"Harga_Jual":105100,
"Jumlah": 0.1
},

"ETH":{
"Harga_Beli": 2500,
"Harga_Jual": 2600,
"Jumlah": 2
},

"SOL":{
"Harga_Beli": 170,
"Harga_Jual": 200,
"Jumlah": 21
}
}

def menu():
 print("============================")
 print("1. Lihat Coin")
 print("2. Tambah Coin")
 print("3. Hapus Coin")
 print("4. Ganti Harga Coin")
 print("5. Hitung profit / loss Coin")
 print("6. Keluar")

def tambah():
 man = input("Masukkan nama Coin: ")
 har = int(input("Masukkan Harga: "))
 jum = int(input("Masukkan Jumlah Coin: "))
 
 portofolio[man] = {
 "Harga_Beli": har,
 "Harga_Jual": har,
 "Jumlah": jum
 }
 print("Coin berhasil ditambahkan")
 input()

def lihat():
 i = 0
 for key, value in portofolio.items():
  print()
  print("============================")
  print(i+1,".","Nama Coin: ",key)
  print("Harga Beli: ", value["Harga_Beli"])
  print("Harga Jual: ", value["Harga_Jual"])
  print("Jumlah saat ini: ", value["Jumlah"])
  print("============================")
  i+=1
 input()
  
def update():
 Man = input("Masukkan Nama Coin: ")
 if Man in portofolio:
  lol = int(input("Masukkan Harga terkini: "))
  portofolio[Man]["Harga_Jual"] = lol
  print("Sukses!")
 else:
  print("Coin Tidak Ada")
 input()

def hapus():
 nam = input("Masukkan nama Coin yang ingin dihapus: ")
 if nam in portofolio:
  del portofolio[nam]
  print("Berhasil!")
 input()
def banding():
 i = 0
 for a, b in portofolio.items():
  print()
  print("============================")
  print(i+1,".","Nama Coin: ",a)
  print("Harga Beli: ", b["Harga_Beli"])
  print("Harga Jual: ", b["Harga_Jual"])
  k = b["Harga_Jual"] - b["Harga_Beli"]
  if k <= 0 :
   print("Kerugian dan loss: -", k)
  elif k >=1 :
      print("Keuntungan dan profit: +", k)
  print("============================")
  i += 1
 input()
  
while ALHAMDULILLAH_KANG:
 os.system("cls")
 menu()
 k = input("Mana yang ingin anda lakukan? : ")
 print("============================")
 if k == "1":
  os.system("cls")
  lihat()
 elif k == "2":
  os.system("cls")
  tambah()
 elif k == "3":
  os.system("cls")
  hapus()
 elif k == "4":
  os.system("cls")
  update()
 elif k == "5":
  os.system("cls")
  banding()
 elif k == "6":
  ALHAMDULILLAH_KANG = False
 else :
  print("Tidak valid")
  input()