#Mini project day 04
#Context keeper CLI
from google import genai
from google.genai import types, errors
from dotenv import load_dotenv
import os
import time
import logging

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
class AITokenBudgetExceeded(Exception):
	pass
#=
logger = logging.getLogger("Mp-04") ; logger.setLevel(logging.DEBUG)
visual = logging.StreamHandler() ; visual.setLevel(logging.ERROR)
file = logging.FileHandler("Mp-04.log") ; file.setLevel(logging.INFO)

format_message = logging.Formatter("%(asctime)s - %(levelname)s | %(message)s","%d/%m/%Y %H:%M:%S")
visual.setFormatter(format_message) ; file.setFormatter(format_message)

logger.addHandler(visual) ; logger.addHandler(file)
#=

def konsul_market_CLI(chat, history, instruction = "Kamu adalah asisten analisis crypto. Jawab singkat dan langsung ke poin, tanpa basa-basi."):
	config = types.GenerateContentConfig(
		system_instruction = instruction,
		temperature = 0.3,
		max_output_tokens = 1500
	)
	if chat == "":
		raise ValueError("Input tidak boleh kosong")
	if not isinstance(history, list):
		raise TypeError("History bukanlah list, silahkan diubah.")
	history.append({"role" : "user", "parts" : [{"text" : chat}]})
	response = client.models.generate_content(
		model = "gemini-flash-latest",
		config = config,
		contents = history
	)
	print("====================================== AI ======================================")
	print(response.text)
	print("==================================== TOKENS ====================================")
	print("Jumlah token yang dipakai untuk Prompt: ",response.usage_metadata.prompt_token_count)
	print("Jumlah token yang dipakai untuk Output text: ",response.usage_metadata.candidates_token_count)
	print("Jumlah token yang dipakai untuk Thinking module: ",response.usage_metadata.thoughts_token_count)
	print("Jumlah total token yang dipakai untuk Prompt: ",response.usage_metadata.total_token_count)
	print("================================================================================")
	if response.candidates[0].finish_reason == "MAX_TOKEN":
		raise AITokenBudgetExceeded()
	if abs(config.max_output_tokens - (int(response.usage_metadata.candidates_token_count) + int(response.usage_metadata.thoughts_token_count))) <= 50:
		logger.warning("Token mendekati batas maksimal.")
	history.append({"role" : "model", "parts" : [{"text" : response.text}]})

def main():
	running = True
	history = []
	while running:
		try:
			for i in range(3):
				ask = input(">")
				if ask.lower() in ("exit","stop","close"):
					running = False
					break
				konsul_market_CLI(ask, history)
			history = history[-6:]
		except TypeError as e:
			logger.critical(f"ERROR {e}")
			break
		except ValueError as e:
			logger.error(f"ERROR: {e}")
		except AITokenBudgetExceeded:
			logger.error(f"Penggunaan token melebihi batas, menyebabkan terpotongnya output.")
		except errors.ClientError as e:
			if e.code in (400,401,403,404):
				logger.critical(f"ERROR code({e.code}, {e})")
				break
			else:
				logger.error(f"ERROR code({e.code}, {e})")
		except errors.ServerError as e:
			logger.error(f"ERROR code({e.code}, {e})")
		except (ConnectionError,TimeoutError):
			logger.error("Jaringan tidak stabil, skip iterasi")
		time.sleep(5)
if __name__== "__main__":
	try:
		os.system("cls")
		main()
		logger.info("PROGRAM SELESAI")
	except KeyboardInterrupt:
		logger.info("PROGRAM DIMATIKAN")