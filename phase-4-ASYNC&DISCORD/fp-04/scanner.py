import json
from datetime import datetime, timezone
import requests
import time
import logging
logger = logging.getLogger(__name__)


def fetch_prices(coins : list, currencies : list, demo_key, max_retry, interval):
	for i in range(1, max_retry + 1):
		try:
			url = "https://api.coingecko.com/api/v3/simple/price"
			params = {
				"vs_currencies" : ",".join(currencies),
				"ids" : ",".join(coins),
				"x_cg_demo_api_key" : demo_key
			}
			response = requests.get(url, params=params)
			response.raise_for_status()
			data = response.json()

			missing_coins = [coin for coin in coins if coin not in data]
			if missing_coins:
				raise ValueError(
					f"Coin ID tidak dikenali oleh CoinGecko: {missing_coins}"
					f"Cek penulisan di config.json"
				)
			return data
		except requests.exceptions.HTTPError:
			status = response.status_code
			if status == 429:
				logger.warning(f"Rate limit kena (percobaan ke - {i}/{max_retry})")
				time.sleep(i * interval)
			elif status in (500, 502, 503):
				logger.warning(f"Server error {status} (percobaan ke - {i}/{max_retry}), tunggu {i*5} detik")
				time.sleep(i * interval)
			elif status in (400, 404):
				raise ValueError (
					f"Request ditolak API status {status}."
					f"Kemungkinan coins = {coins} atau currencies = {currencies} tidak valid"
					f"Cek di config.json"
				)
			else:
				logger.warning(f"HTTP error {status} tidak dikenali (percobaan ke - {i}/{max_retry})")
				time.sleep(i * interval)
		except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
			logger.warning(f"Timeout/koneksi gagal (percobaan ke - {i}/{max_retry})")
			time.sleep(i * interval)
		except requests.exceptions.InvalidURL as e:
			logger.critical("INVALID URL -- cek kode, URL API salah ketik")
			return None
		except requests.exceptions.RequestException as e:
			logger.warning(f"Request error tidak dikenali: {e} (percobaan ke - {i}/{max_retry})")
			time.sleep(i * interval)
	logger.error(f"Gagal fetch setelah {max_retry} percobaan")
	return None

def hitung_persen(harga_sekarang: float, baseline: float):
	persen = (harga_sekarang - baseline) / baseline * 100
	return persen

def cek_trigger(coin : str ,harga_sekarang : float, baseline : dict, cooldown_until : dict, threshold_percent : float):
	baseline_coin = baseline.get(coin)

	if baseline_coin is None:
		return {"trigger": False, "perubahan_persen": None}
	persen = hitung_persen(harga_sekarang, baseline_coin)
	cooldown_time = cooldown_until.get(coin)
	sedang_cooldown = cooldown_time is not None and datetime.now(timezone.utc) < cooldown_time
	if abs(persen) >= threshold_percent and not sedang_cooldown:
		return {"trigger": True, "perubahan_persen": f'{persen:.2f}%'}
	return {"trigger": False, "perubahan_persen": f'{persen:.2f}%'}

def update_state(coin, harga_sekarang, baseline : dict):
	baseline[coin] = harga_sekarang		