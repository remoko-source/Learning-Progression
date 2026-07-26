import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
def baca_token(text : str, model : str = "gemini-flash-latest") -> int:
	hasil = client.models.count_tokens(model=model, contents=text)
	return hasil.total_tokens

prompt = """
  =========================== BITCOIN ===========================

  + saat ini berada di harga $67000. RSI menunjukkan 72.0 overbought.
  + Harga saat ini berada di atas MA3, menunjukkan tren naik


  =========================== ETHEREUM ===========================

  + saat ini berada di harga $3620. RSI menunjukkan 71.43 overbought.
  + Harga saat ini berada di atas MA3, menunjukkan tren naik
"""
model = "gemini-flash-latest"
def bandingkan_token(teks : str):
	estimasi = len(teks) / 4
	akurat = baca_token(teks)
	selisih = akurat - estimasi
	
	print(f"Teks			: {teks[:50]}")
	print(f"Estimasi Kasar		: {estimasi} token")
	print(f"Token akurat		: {akurat} token")
	print(f"Selisih			: {selisih} token")

bandingkan_token(prompt)
