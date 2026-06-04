import os
import json
class Wallet:
   def __init__(self,nama):
       with open("data.json","r") as file:
         data = json.load(file)
       for akun in data["akun"]:
           if nama == akun["nama"]:
               self.trader = akun["nama"]
               self.saldo = akun["saldo"]
               self.portofolio = akun["portofolio"]
               break
       else:
               print(f"User {nama} tidak ditemukan")

   def lihat(self):
       print(f"Selamat Datang {self.trader}!")
       print(f"Sisa saldo anda : {self.saldo}")
       print(f"Anda memiliki:")
       for i, (coin, jumlah) in enumerate(self.portofolio.items()):
           print(f"{i+1}.{coin} Sejumlah :{jumlah:.3f}")
       
   def simpan(self):
       with open("data.json","r")  as file:
           data = json.load(file)
       for akun in data["akun"]:
           if akun["nama"] == self.trader:
               akun["saldo"] = self.saldo
               akun["portofolio"] = self.portofolio
               break
               
       with open("data.json","w") as file:
           json.dump(data, file, indent=2)
           
   def deposit(self, jumlah):
      try:
       self.saldo += jumlah
       print(f"Berhasil deposit sebesar {jumlah}!")
       print(f"Total saldo anda sekarang adalah: {self.saldo}")
       self.simpan()
      except ValueError:
       print("Input harus berupa angka!")
       
   def withdraw(self, jumlah):
      try:
       if jumlah <= self.saldo:
           self.saldo -= jumlah
           print(f"Berhasil mengambil sebesar {jumlah}!")
           print(f"Total saldo anda sekarang adalah: {self.saldo}")
           self.simpan()
       else: 
           print("Saldo tidak mencukupi.")
      except ValueError:
          print("Input harus berupa angka!")
          
   def beli(self, c):
       man = input("Masukkan nama coin: ").upper()
       with open("data.json","r") as file:
           data = json.load(file)
       if man in c.daftar:
           tran = int(input("Masukkan nominal Pembelian: "))
           if tran <= self.saldo:
            harga = c.daftar[man]["harga_sekarang"]
            dapat = tran / harga
            if man in self.portofolio:
                self.portofolio[man] += dapat
            else:
                self.portofolio[man] = (dapat)
            self.saldo -= tran
            self.simpan()
           else:
            print("Saldo tidak mencukupi")
           print(f"Berhasil membeli {man} sebesar {dapat:.3f}!")
   def jual(self, c):
       man = input("Masukkan nama coin: ").upper()
       with open("data.json","r") as file:
           data = json.load(file)
       if man in c.daftar:
           tran = float(input("Masukkan Jumlah coin yang ingin dijual: "))
           if man in self.portofolio and self.portofolio[man] >= tran :
            harga = c.daftar[man]["harga_sekarang"]
            dapat = tran * harga
            self.portofolio[man] -= tran
            self.saldo += dapat
            print(f"Berhasil menjual {man} sebesar {dapat:.3f}!")
            self.simpan()
           else:
            print("Jumlah Coin tidak mencukupi")