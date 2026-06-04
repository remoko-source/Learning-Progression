import os
import json
from crypto import Crypto
from wallet import Wallet

KOK = True
KAK = False
KIK = False
tanda = ""
def menu():
    print("=================================================")
    print("    Selamat datang di aplikasi Crypto Vault!")
    print("=================================================")
    print()
    print("1. Login Ke akun yang sudah ada")
    print("2. Buat akun baru")
    print("3. Keluar")

def menu2():
    print("=================================================")
    print(f"    Selamat datang kembali {tanda}!")
    print("=================================================")
    print()
    print("1. Cek Wallet")
    print("2. Deposit Saldo")
    print("3. Withdraw Wallet")
    print("4. Lihat Harga Crypto")
    print("5. Ubah Harga Coin")
    print("6. Analisis Perubahan Harga Coin")
    print("7. Beli coin")
    print("8. Jual coin")
    print("9. Keluar")

def lanjut():
 global KOK
 global KAK
 
 KOK = False
 KAK = True

def baru():
 with open("data.json","r") as file:
  data = json.load(file)
 kon = True
 while kon:
  os.system("cls")
  kama = input("Masukkan username: ")
  pasa = input("Masukkan Password: ")
  sudah_ada = False
  for akun in data["akun"]:
     if akun["nama"] == kama:
         sudah_ada = True
         break
  if not sudah_ada:
   akun_baru = {
   "nama" : kama,
   "pass" : pasa,
   "saldo": 0,
   "portofolio":{
   
    }
   }
   data["akun"].append(akun_baru)
   with open("data.json","w") as file:
      json.dump(data, file, indent=2)
   print("Akun berhasil dibuat!")
   input("YAY")
   os.system("cls")
   kon = False
  else :
   print("Username sudah ada")
   print("Lanjut?")
   koll = input("Ya/Tidak : ").upper()
   if koll == "YA" or koll == "Y":
       kon = True
   elif koll == "TIDAK" or koll == "T":
       kon = False

def akun():
 with open("data.json","r") as file:
     man = json.load(file)
 nama = input("Masukkan nama mu: ")
 pasw = input("Masukkan Password akun mu: ")
 for akun in man["akun"]:
     if akun["nama"] == nama and akun["pass"] == pasw:
         os.system("cls")
         print(f"Anda berhasil login.")
         global w
         global cryp
         cryp = Crypto()
         w = Wallet(nama)
         global tanda
         tanda = nama
         lanjut()
         break
 else:
         print("Nama atau Password tidak valid.")

while KOK:
 menu()
 print("=================================================")
 lol = input("Apa yang ingin anda lakukan? : ")
 if lol == "1":
  os.system("cls")
  akun()
 elif lol == "2":
  baru()
 elif lol == "3":
  print("Good Luck!")
  KOK = False
 else:
  print("Input tidak valid")
  
while KAK :
 menu2()
 print("=================================================")
 lol = input("Apa yang ingin anda lakukan? : ")
 if lol == "1":
  os.system("cls")
  w.lihat()
 elif lol == "2":
  os.system("cls")
  try:
   Kan = int(input("Masukkan jumlah Saldo: "))
   w.deposit(Kan)
  except ValueError:
   print("Harus berupa angka!")
 elif lol == "3":
  os.system("cls")
  try:
   maan = int(input("Masukkan jumlah Saldo: "))
   w.withdraw(maan)
  except ValueError:
   print("Harus berupa angka!")
 elif lol == "4":
  os.system("cls")
  cryp.lihat_harga()
 elif lol == "5":
  os.system("cls")
  cryp.update_harga()
 elif lol == "6":
  os.system("cls")
  cryp.analisis()
 elif lol == "7":
  w.beli(cryp)
 elif lol == "8":
  w.jual(cryp)
 elif lol == "9":
  print("Good Luck!")
  KAK = False
 else:
  print("Input tidak valid")