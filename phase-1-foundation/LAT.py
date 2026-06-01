class RekeningBank:
    def __init__(self, nama, saldo_awal):
     self.nama = nama
     self.__saldo = saldo_awal
     self.riwayat = []
    def tampil(self):
     print("===================")
     print(F"Nama: {self.nama}")
     print(f"Saldo: {self.__saldo}")
     print("===================")
     self.riwayat.append("Cek")
    def deposit(self, saldo):
     self.__saldo += saldo
     print(f"Jumlah deposit : Rp.{saldo} Berhasil! , Jumlah Rekening sekarang: Rp.{self.__saldo}")
     self.riwayat.append(f"Deposit +{saldo}")
    def withdraw(self, saldo):
     if saldo > self.__saldo:
      print("Uang di saldo anda tidak mencukupi.")
      self.riwayat.append("Gagal Withdraw")
     else:
      self.__saldo -= saldo
      print(f"Pengambilan uang sebesar Rp.{saldo} Berhasil!, Sisa saldo anda : Rp.{self.__saldo}")
      self.riwayat.append(f"Withdraw -{saldo}")
    def transfer(self, akun_lain, saldo):
     if saldo > self.__saldo:
      print("Uang di saldo anda tidak mencukupi.")
      self.riwayat.append(f"Gagal Transfer")
     else :
      self.__saldo -= saldo
      akun_lain.__saldo += saldo
      print(f"Berhasil transfer sebesar Rp{saldo}. Saldo anda tersisa Rp{self.__saldo}")
      self.riwayat.append(f"Transfer -{saldo}")
    def tampil_riwayat(self):
     for i in range(len(self.riwayat)):
      print(i+1,". ", self.riwayat[i])
akun1 = RekeningBank("Reykhandi", 12000)
akun2 = RekeningBank("Claude sensei", 1901000)
akun1.tampil()
akun1.deposit(20000)
akun1.withdraw(5000)
akun2.__saldo = 100000000000000000000000
akun2.tampil()
print(akun2.__saldo)
akun1.transfer(akun2,10000)
akun1.tampil_riwayat()