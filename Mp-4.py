#Mini Project Day 4
#Calculator Modular
kal = True
import os
def menu():
 angka = int(input("Masukkan angka pertama : "))
 angki = int(input("Masukkan angka kedua : "))
 print()
 print("1. Penjumlahan")
 print("2. Pengurangan")
 print("3. Perkalian")
 print("4. Pembagian")
 print("5. Berhenti")
 return angka, angki

def kurang(a, b):
 print("Hasil : ", a - b)
 input()
 os.system("cls")
def tambah(a, b):
 print("Hasil : ", a + b)
 input()
 os.system("cls")
def bagi(a, b):
 print("Hasil : ", a // b)
 input()
 os.system("cls")
def kali(a, b):
 print("Hasil : ", a * b)
 input()
 os.system("cls")

while kal:
 a, b = menu()
 K = input("Input Operasi: ")
 if K == "1" :
     os.system("cls")
     tambah(a, b)
 elif K == "2" :
     os.system("cls")
     kurang(a, b)
 elif K == "3" :
     os.system("cls")
     kali(a, b)
 elif K == "4" :
     os.system("cls")
     bagi(a, b)
 elif K == "5" :
     os.system("cls")
     kal = False
 else :
     print("Tidak Valid")
     input()
     os.system("cls")
