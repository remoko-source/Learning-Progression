import pandas as pd
data = {
	"close": [
	64000,64230,63980,64500,65000,
	64800,65200,65600,65100,64900,
	65300,65800,66200,66000,65700,
	65500,65900,66300,66700,67000]
}

df = pd.DataFrame(data, index=range(1, len(data["close"])+1))

df["change"] = df["close"].diff()

df["gain"] = df["close"].where(df["change"] > 0, 0)
df["loss"] = -df["close"].where(df["change"] < 0, 0)

period = 14
avg_gain = df["gain"].rolling(window=period).mean()
avg_loss = df["loss"].rolling(window=period).mean()

RS = avg_gain - avg_loss
df["RSI"] = 100 - (100 / (1+RS))
print(df)
rsi = df["RSI"].iloc[-1]

def ma_hitung(data):
	MA3 = data.rolling(window=3).mean()
	if data.iloc[-1] > MA3.iloc[-1]:
		return "atas MA3, Tren naik"
	elif data.iloc[-1] < MA3.iloc[-1]:
		return "bawah MA3, Tren turun"
	else:
		return "Titik MA3, Tren stabil"
def rsi_hitung(rsi):
	if rsi >= 70:
		hasil = "overbought"
	elif rsi <= 30:
		hasil = "oversold"
	else:
		hasil = "stabil"
	return f"RSI {rsi:.4f} ({hasil})."
	
def hasil_akhir(harga_akhir):
	RSI = rsi_hitung(rsi)
	MA = ma_hitung(df["close"])
	return f"BTC saat ini ${harga_akhir} {RSI} Harga berada di {MA}"
	
print(hasil_akhir(df["close"].iloc[-1]))