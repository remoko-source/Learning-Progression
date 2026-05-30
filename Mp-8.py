#Mini Project day 8
#To do list Json file
import os
import json

lol = True
try:
 with open("todos.json","r") as file:
  json.load(file)
except FileNotFoundError:
 with open("todos.json","w") as file:
  json.dump([], file) 

def menu():
 print("==============================")
 print("1. Tambah Tugas Baru")
 print("2. Lihat Semua Tugas ")
 print("3. Hapus Tugas (Berdasarkan Nomor)")
 print("4. Keluar")


def tambah():
 with open("todos.json","r") as nope:
  tugas = json.load(nope)
 tam = input("Tambahkan Tugas baru: ")
 tugas.append(tam)
 with open("todos.json","w") as nope:
  json.dump(tugas, nope, indent=2)

def lihat():
 with open("todos.json","r") as nope:
  tugas = json.load(nope)
  if len(tugas) == 0:
   print("Tugas belum tersedia!")
  else:
   print(json.dumps(tugas, indent=2))

def hapus():
 with open("todos.json","r") as file:
  tugas = json.load(file)
 for i in range(len(tugas)):
  print(i+1, tugas[i])
 try:
  man = int(input("Masukkan (Angka) Tugas yang ingin anda hapus: "))
  tugas.pop(man-1)
  with open("todos.json","w") as nope:
   json.dump(tugas, nope, indent=2)
 except ValueError:
  print("Harus berupa angka")
 except:
  print("Tugas tidak ada")

while lol:
 menu()
 kan = input("Apa yang ingin anda lakukan? : ")
 print("==============================")
 if kan == "1":
  os.system("cls")
  tambah()
 elif kan == "2":
  os.system("cls")
  lihat()
 elif kan == "3":
  os.system("cls")
  hapus()
 elif kan == "4":
  os.system("cls")
  print("Berhasil keluar")
  lol = False
 else:
  print("Perintah tidak valid")