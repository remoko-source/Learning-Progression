from google import genai
import os
import logging
from dotenv import load_dotenv
#=======================================================================
logger = logging.getLogger("MP-02") ; logger.setLevel(logging.DEBUG)
visual = logging.StreamHandler() ; visual.setLevel(logging.INFO)

formats = logging.Formatter()
logger.addHandler(visual)
#=======================================================================
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

class TokenBudgetExceededError(Exception):
	pass
def cek_token(text : str, model : str = "gemini-flash-latest"):
	hitung = client.models.count_tokens(model=model, contents=text)
	if hitung.total_tokens <= 10:
		pass
	elif hitung.total_tokens > 10 and hitung.total_tokens <= 15:
		potong = text.split()
		kali = []
		for i in potong:
			kali.append(i)
			hitung = client.models.count_tokens(model=model, contents=" ".join(kali))
			if hitung.total_tokens <= 10:
				continue
			else:
				kali.remove(i)
				text = " ".join(kali)
				logger.warning("TEKS DIPOTONG")
	else:
		raise TokenBudgetExceededError("Token melebihi batas, Operasi gagal") 
	logger.info("AMAN")
	return text
	
def ai_input(text : str, model : str = "gemini-flash-latest"):
	try:
		teks = cek_token(text)
		response = client.models.generate_content(
		model = model,
		contents = teks
		)
		hasil = client.models.count_tokens(model=model, contents=teks)
		return response, hasil.total_tokens
	except TokenBudgetExceededError as e:
		logger.critical("MELEBIHI BATAS TOKEN")
prompt = input(">")
response = ai_input(prompt)
try:
	print(response[0].text)
	print(response[1])
except Exception as e:
	print("MELEBIHI batas")