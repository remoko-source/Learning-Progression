#Mini project Day 03
#AI Advisor CLI / Market Advisor CLI
from dotenv import load_dotenv
from google import genai
import os
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
def tanya_ai(chat : str, instructions : str = "Kamu adalah asisten analisis crypto. Jawab singkat dan langsung ke poin, tanpa basa-basi."):
	response = client.models.generate_content(
	model="gemini-flash-latest",
	config={
		"system_instruction" : instructions,
		"temperature" : 0.3,
		"max_output_tokens" : 1000
		},
	contents = chat
	)
	print("FINISH REASON:", response.candidates[0].finish_reason)
	return response.text
	
while True:
	ask = input(">")
	if ask.split()[0].lower() in ("instructions:","instructions=","instruksi:","instruksi=","instruction:","instruction="):
		ask = ask.split()[1:] ; ask = " ".join(ask)
		alt = input(">")
		print(tanya_ai(alt, ask))
	elif ask.split()[0] in ("instruksi", "instructions","instruction"):
		ask = ask.split()[2:] ; ask = " ".join(ask)
		alt = input(">")
		print(tanya_ai(alt, ask))
	elif ask == "exit":
		print("Program Selesai")
		break
	else:
		print(tanya_ai(ask))
	print()