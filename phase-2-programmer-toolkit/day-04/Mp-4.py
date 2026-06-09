import sys
if len(sys.argv) == 4:
 if sys.argv [2] == "+":
  print(f"Hasil : {int(sys.argv[1]) + int(sys.argv[3])}")
 elif sys.argv [2] == "-":
  print(f"Hasil : {int(sys.argv[1]) - int(sys.argv[3])}")
 elif sys.argv [2] == "*":
  print(f"Hasil : {int(sys.argv[1]) * int(sys.argv[3])}")
 elif sys.argv [2] == "/":
  print(f"Hasil : {int(sys.argv[1]) / int(sys.argv[3])}")
else:
 print("Error! Format Salah!")
 print("Harap Masukkan Dengan Format berikut: ")
 print("python Mp-4 (Angka 1) ('+ - * /') (Angka 2)")
sys.exit("Sampai Jumpa!")