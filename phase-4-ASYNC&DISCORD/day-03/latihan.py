from dotenv import load_dotenv
import requests
import os
import time
def webhook(isi: str):
	try:
		load_dotenv()
		WEBHOOK_URL = os.getenv("WEBHOOK_API_URL")
		param = {"content" : isi}
		response = requests.post(WEBHOOK_URL, json=param)
		response.raise_for_status()
		print("berhasil")
	except Exception as e:
		print("ERROR: ",e)
webhook("WEBHOOK TESTING (IGNORE)")