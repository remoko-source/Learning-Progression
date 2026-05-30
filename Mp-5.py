#Mini Project day 5
#Database siswa
kal = True
import os
database = {
"Rey" : {
"umur" : 17,
"jurusan" : "IPA"
  },

"Akmal" : {
"umur" : 18,
"jurusan" : "AGAMA"
  },

"Azral" : {
"umur" : 18,
"jurusan" : "IPS"
  }
}

def tambah() :
 nama = input("Masukkan Nama siswa : ")
 umr = int(input("Masukkan Umur Siswa: "))
 jur = input("Masukkan Jurusan Siswa: ")
 
 database[nama] = {
 "umur" : umr,
 "jurusan" : jur
 }
 print("Siswa berhasil ditambahkan!")
 input()
 
def hapus():
 mana= input("Tuliskan nama siswa yang mau dihapus : ")
 if mana in database:
  del database[mana]
 else :
  print("Tidak Valid")
 input()

def lihat():
 no = 1
 for key, value in database.items():
   print(no,".", key," Umur : ", value["umur"]," Jurusan : ", value["jurusan"])
   no += 1
 input()

def jumlah() :
 os.system("cls")
 print("Jumlah Siswa sekarang adalah : ",len(database))
 input()

def ganti() :
 tes = input("Masukkan Nama siswa yang ingin diganti: ")
 if tes in database:
  print("1. Ganti Umur")
  print("2. Ganti Jurusan")
  m = input("Apa yang ingin anda lakukan? ")
  if m == "1":
   g = int(input("Masukkan Umur Baru: "))  
   database[tes]["umur"] = g
  elif m == "2":
   g = input("Masukkan Jurusan Baru: ")
   database[tes]["jurusan"] = g
  else:
   print("Tidak valid")

 else:
    print("Siswa tidak ditemukan")

def menu():
 print("=== DATABASE SISWA ===")
 print()
 print("1. Tambah Siswa")
 print("2. Lihat Siswa")
 print("3. Edit data Siswa")
 print("4. Hapus Siswa")
 print("5. Cek Jumlah Siswa")
 print("6. Keluar")


while kal:
 os.system("cls")
 menu()
 k = input("Mana yang ingin anda lakukan? : ")
 if k == "1":
  os.system("cls")
  tambah()
 elif k == "2":
  os.system("cls")
  lihat()
 elif k == "3":
  os.system("cls")
  ganti()
 elif k == "4":
  os.system("cls")
  hapus()
 elif k == "5":
  os.system("cls")
  jumlah()
 elif k == "6":
  kal = False
 else :
  print("Tidak valid")
  input()












