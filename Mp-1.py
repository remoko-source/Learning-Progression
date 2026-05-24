#Mini Project day 1
import os
angka = int(input("Masukkan Angka Pertama : "))
op = input("Masukan Operator ({+},{x},{-},{:}) : ")
angki = int(input("Masukkan Angka Kedua : "))

if op == "+" :
 print(f"Hasil : {angka + angki}")
elif op == "x" :
 print(f"Hasil : {angka * angki}")
elif op == "-" :
 print(f"Hasil : {angka - angki}")
elif op == ":" :
 print(f"Hasil : {angka // angki}")
else :
 print("Tidak valid")
input()
os.system("cls")