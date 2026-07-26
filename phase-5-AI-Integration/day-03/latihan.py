import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
	model="gemini-flash-latest",
	config={
	"system_instruction" : "Kamu adalah asisten analisis crypto. Jawab singkat dan langsung ke poin, tanpa basa-basi.",
	"temperature" : 0.3,
	"max_output_tokens" : 1000
	},
	contents="Bagaimana kondisi BTC hari ini"
)


print(response.text)