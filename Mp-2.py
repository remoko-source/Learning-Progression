
#Mini Project day 2
tugas = ["Matemika","Sains","PJOK"]
while True:
 def tambah_tugas():
  os.system("cls")
  jawa = input("Masukkan nama tugas : ")
  tugas.append(jawa)
  os.system("cls")
 def lihat_tugas():
   os.system("cls")
   for i in range(len(tugas)) :
     print(i+1,tugas[i])
   input()
   os.system("cls")
 print("1. Tambah Tugas")
 print("2. Lihat Tugas")
 print("3. Berhenti")
 b = input("1/2/3? = ")
 if b == "1" :
  tambah_tugas()
 elif b == "2" :
  lihat_tugas()
 elif b == "3" :
  break
 else :
  print("Perintah tidak valid")
  import os