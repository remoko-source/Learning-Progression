import logging
from datetime import datetime, timedelta
import time
import random

logging.basicConfig(
    level=logging.DEBUG,
    filename="trading_bot_full.log",
    filemode="w", 
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S")
def ambil_harga_btc():
    """Simulasi ambil harga BTC dari API (kadang gagal)"""
    if random.random() < 0.2: 
        raise ConnectionError("Timeout saat menghubungi exchange")
    harga = round(random.uniform(64000, 66000), 2)
    return harga

def hitung_rsi(harga):
    """Simulasi hitung indikator RSI (asal aja untuk demo)"""
    return round(random.uniform(20, 80), 2)

def cek_sinyal(rsi):
    """Tentukan sinyal trading berdasarkan RSI"""
    if rsi < 30:
        return "BUY"
    elif rsi > 70:
        return "SELL"
    else:
        return "HOLD"

def jalankan_bot(jumlah_siklus=5):
    logging.info("=== Bot Trading Dimulai ===")
    waktu_terakhir = None
    for siklus in range(1, jumlah_siklus + 1):
        logging.debug(f"--- Siklus #{siklus} dimulai ---")

        waktu_sekarang = datetime.now()
        if waktu_terakhir is not None:
            selisih = waktu_sekarang - waktu_terakhir
            logging.debug(f"Selisih waktu dari siklus sebelumnya: {selisih}")
        waktu_terakhir = waktu_sekarang
        try:
            harga = ambil_harga_btc()
            logging.info(f"Harga BTC: ${harga}")
        except ConnectionError as e:
            logging.error(f"Gagal ambil harga: {e}")
            logging.info("Menunggu 2 detik sebelum retry...")
            time.sleep(2)
            continue  
        rsi = hitung_rsi(harga)
        logging.debug(f"RSI saat ini: {rsi}")
        if rsi < 25 or rsi > 75:
            logging.warning(f"RSI ekstrem terdeteksi: {rsi}")
        sinyal = cek_sinyal(rsi)
        logging.info(f"Sinyal: {sinyal} (RSI: {rsi})")
        if sinyal in ("BUY", "SELL"):
            logging.info(f"--> Eksekusi order: {sinyal} BTC di harga ${harga}")
        else:
            logging.debug("Tidak ada aksi, HOLD")
        time.sleep(1)
    logging.info("=== Bot Trading Selesai ===")
if __name__ == "__main__":
    jalankan_bot(jumlah_siklus=5)