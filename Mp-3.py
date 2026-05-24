#Mini Project day 3
#Simple choice game

import os
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
def man1():
 print("+10 Gold")
 inventory["gold"] += 10
 print("+3 Potion")
 inventory["potion"] += 3
 print("+ Venomshank")
 inventory["item"].append("Venomshank")
 input()
 os.system("cls")
  
def lihat():
 pass
  
def man2():
 if mental["power"] >= 10 :
  print("Kamu menang!")
  print("+25 EXP")
  mental["exp"]+= 25
 else :
  print("Anda kalah")
  print("-25 HP")
  mental["HP"] -= 25
 input()
 os.system("cls")

def awal(): 
 print("Kamu masuk gua")
 pilihan = input("Mau kiri atau kanan? ")
 if pilihan == "kiri":
  print("Ketemu harta")
  man1()
 else:
  print("Ketemu monster")
  man2()

def lanjut() :
 cek= input("Berhenti? y/t: ")  
 if cek == "y" :
  return False
 return True
 
def menu():
 print("1. Cek item")
 print("2. Cek peralatan")
 print("3. Cek status")
 print("4. Skip ")
 cok = input("Mana yang mau anda lakukan? : ")
 if cok == "1" :
  for key, value in inventory.items():
   if key != "item":
    print(key, ":", value)
 elif cok == "2":
  for key, value in inventory.items():
   if key == "item":
    for i in range(len(inventory["item"])) :
     print(i+1,".",value[i])

 elif cok == "3" :
  for key, value in mental.items() :
   print(key, ":", value)
 elif cok == "4" :
  pass
 else :
  print("Tidak valid")
 
while True:  
  awal()
  menu()
  if not lanjut():
   break