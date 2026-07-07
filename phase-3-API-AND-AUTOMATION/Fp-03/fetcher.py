import time
from logger import get_logger
import requests

def fetch_retry(url, params, max_retries, interval):
	logger = get_logger()
	for i in range(max_retries):
		try:
			response = requests.get(url, params=params)
			response.raise_for_status()
			return response
		except requests.exceptions.HTTPError as e:
			status = response.status_code
			if status in (401, 404, 403):
				logger.critical(f"ERROR: {e}")
				break
			else:
				logger.error(f"ERROR: {e}")
				time.sleep(i+1*(interval**2))
		except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
			logger.error(f"ERROR: {e}")
			time.sleep(i+1*(interval**2))
	return None