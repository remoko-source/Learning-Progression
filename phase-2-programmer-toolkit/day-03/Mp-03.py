import os

files = ["Foto.jpg","Laporan.pdf","Musik.mp3","Selfie.png","Tugas.docx","Video.mp4"]
if os.path.exists("Folder Mp"):
 pass
else:
 os.mkdir("Folder Mp")
for i, file in enumerate(files):
 nama, eksistensi = os.path.splitext(file)
 if eksistensi == ".jpg" or eksistensi == ".png":
  lol = "gambar"
 elif eksistensi == ".pdf" or eksistensi == ".docx":
  lol = "dokumen"
 else:
  lol = "lainnya"
 print(i+1,".", nama+",", "file berjenis: ", lol)