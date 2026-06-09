import sys

print(sys.argv)
print("Nama file:", sys.argv[0])
if len(sys.argv) >= 2:
 print("Halo selamat datang", sys.argv[1])
else:
 print("Tolong Masukkan Nama kamu sebagai argumen!")
sys.exit("Error: Argumen tidak diberikan. ")