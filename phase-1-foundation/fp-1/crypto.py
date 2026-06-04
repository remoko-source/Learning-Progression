import os
import json
class Crypto:
   def __init__(self):
       with open("data.json","r") as file:
         data = json.load(file)
       self.daftar = data["crypto"]
       
   def lihat_harga(self):
       for i, (key, value) in enumerate(self.daftar.items()):
           print(i+1,".",value["nama"],":", value ["harga_sekarang"])

       
   def update_harga(self):
       man = input("Masukkan Coin: ").upper()
       jumlah = int(input("Masukkan Harga sekarang: "))
       with open("data.json","r") as file:
             data = json.load(file)
       if man in data["crypto"]:
             data["crypto"][man]["harga"] = data ["crypto"][man]["harga_sekarang"]
             data["crypto"][man]["harga_sekarang"] = jumlah
             with open("data.json","w") as file:
                 json.dump(data, file, indent=2)
                 print(f"Berhasil mengganti harga {man} menjadi {jumlah}")
       else:
             print("Coin tidak ada")

   def analisis(self):
       man = input("Masukkan Coin: ").upper()
       if man in self.daftar:
           with open("data.json","r") as file:
               mana = json.load(file)
           lol = mana["crypto"][man]["harga_sekarang"]
           kol = mana["crypto"][man]["harga"]
           persen = ((lol - kol) / kol) * 100
           print("Perbandingan harga Coin crypto:")
           if persen > 0:
               print(f"Coin mengalami kenaikan harga sebesar {persen:.2f}% dari harga awal")
           elif persen < 0 :
               print(f"Coin mengalami penurunan harga sebesar {persen:.2f}% dari harga awal")
           elif persen == 0 :
               print("Coin stabil")
       else :
           print("Coin tidak ada")