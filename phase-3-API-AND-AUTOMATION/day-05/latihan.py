import time
import requests

def fetch_retry(url, maxret=3, delay=1):
	for attempt in range(maxret):
		try:
			response = requests.get(url)
			response.raise_for_status()
			return response
			
		except requests.exceptions.HTTPError as e:
			status = response.status_code
			if status == 404 or status == 401 or status == 403:
				print("ERROR FATAL ", status)
				print("SISTEM OFF")
				break
			else:
				print("ERROR: ", e)
				time.sleep(delay*(2**attempt))
		except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
			print("ERROR: ", e)
			time.sleep((delay*(2**attempt))
	return None
	
result = fetch_retry("https://api.coingecko.com/api/v3/ping")
print(result.json())