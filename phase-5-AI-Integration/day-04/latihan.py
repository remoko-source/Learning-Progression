from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
def ai_ask(chat, history, instructions="Kamu adalah asisten analisis crypto. Jawab singkat dan langsung ke poin, tanpa basa-basi."):
	history.append({"role" : "user", "parts" : [{"text" : chat}]})
	config = types.GenerateContentConfig(
		system_instruction=instructions,
		temperature=0.3,
		max_output_tokens=500
	)
	
	response = client.models.generate_content(
		model = "gemini-flash-latest",
		config = config,
		contents = history
	)
	history.append({"role" : "model", "parts" : [{"text" : response.text}]})
	print(response.candidates[0].finish_reason)
	print(response.usage_metadata.thoughts_token_count)
	return response.text
history = []
while True:
	ask = input(">")
	if ask.lower() in ("exit","close"):
		break
	print(ai_ask(ask, history))