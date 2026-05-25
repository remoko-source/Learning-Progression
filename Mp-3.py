#Mini Project day 3
#Simple choice game

import os
game = bool
current = 0
inventory = {
"gold" : 10,
"potion" : 5,
"stample" : 20,
"item" :[
"Pedang",
"Jubah dasar",
"Helm kesatria"
]
}

mental = {
"exp" : 25,
"HP" : 100,
"power": 11
}

def lanjut() :
 cek= input("Berhenti? y/t: ")  
 if cek == "y" :
  return False
 os.system("cls")
 return True
 
def man1():
 print("+10 Gold")
 inventory["gold"] += 10
 print("+3 Potion")
 inventory["potion"] += 3
 print("+ Venomshank")
 inventory["item"].append("Venomshank")
 input()
 os.system("cls")
 return
  
def lihat():
 pass
  
def man2():
 if mental["power"] >= 10 :
  print("Kamu menang!")
  print("+25 EXP")
  mental["exp"]+= 25
  return
 else :
  print("Anda kalah")
  print("-25 HP")
  mental["HP"] -= 25
  return

def mon():
 inp = input("Check stats dan inventory? 1/2 = ")
 if inp == "1" :
  os.system("cls")
  menu()
  return
 else :
  os.system("cls")
  return
 
def lol() :
 pilihan = input("Mau kiri atau kanan? ")
 if pilihan == "kiri":
  print("Ketemu harta")
  man1()
 else:
  print("Ketemu monster")
  man2()

def hutan():
 print("Kamu masuk Hutan")
 lol()

def gua():
 print("Kamu masuk Gua")

def kastil():
 print("Kamu masuk Kastil")
 pass
 
def padang_pasir():
 print("Kamu masuk Padang Pasir")
 pass
 
area = [
hutan,
kastil,
gua,
padang_pasir
]

def menu():
 print("1. Cek item")
 print("2. Cek peralatan")
 print("3. Cek status")
 print("4. Skip ")
 cok = input("Mana yang mau anda lakukan? : ")
 if cok == "1" :
  print()
  for key, value in inventory.items():
   if key != "item":
    print(key, ":", value)
  input()
 elif cok == "2":
  print()
  for key, value in inventory.items():
   if key == "item":
    for i in range(len(inventory["item"])) :
     print(i+1,".",value[i])
  input()

 elif cok == "3" :
  for key, value in mental.items() :
   print(key, ":", value)
 elif cok == "4" :
  os.system("cls")
  return
 else :
  print("Tidak valid")
 
while game and current < len(area):
  area[current]()
  mon()
  game = lanjut()
  current += 1