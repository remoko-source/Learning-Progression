import os
if os.path.exists("Hasil_latihan"):
 print("Folder sudah ada")
else:
  os.mkdir("Hasil_latihan")
  os.makedirs("Hasil_latihan/data")
  os.makedirs("Hasil_latihan/log")
  print(os.listdir("Hasil_latihan"))
prit = os.path.join("Hasil_latihan", "data")
print(prit)