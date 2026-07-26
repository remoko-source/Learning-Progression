#Mini project day 1
#Market narrator
import pandas as pd
def analisis(data, N, M):
	df = pd.DataFrame(data, index=range(1, len(data["close"])+1))
	
	#bagian RSI
	df["change"] = df["close"].diff()
	df["gain"] = df["change"].where(df["change"] > 0, 0)
	df["loss"] = df["change"].where(df["change"] < 0, 0)
	
	periode=M
	avg_gain = df["gain"].rolling(window=periode).mean()
	avg_loss = -df["loss"].rolling(window=periode).mean()
	df["rsi"] = 100 - (100 / (1 + (avg_gain / avg_loss)))
	
	#bagian MA
	df["MA"] = df["close"].rolling(window=N).mean()
	return df
	
def narasi_rsi(rsi_akhir):
	if rsi_akhir > 70:
		return "overbought"
	elif rsi_akhir < 30:
		return "oversold"
	else:
		return "netral"
def narasi_MA(MA_akhir, harga_akhir, N):
	if harga_akhir > MA_akhir:
		return f"di atas MA{N}, menunjukkan tren naik"
	elif harga_akhir < MA_akhir:
		return f"di bawah MA{N}, menunjukkan tren turun"
	else:
		return f"tepat di MA{N}, menunjukkan tren stabil"

def buat_laporan(data, nama_coin, config):
	df = analisis(data, config["MA_PERIOD"], config["RSI_PERIOD"])
	
	return f"""
	=========================== {nama_coin.upper()} ===========================
	
	+ saat ini berada di harga ${data['close'][-1]}. RSI menunjukkan {df['rsi'].iloc[-1]:.4} {narasi_rsi(df['rsi'].iloc[-1])}.
	+ Harga saat ini berada {narasi_MA(df['MA'].iloc[-1], data['close'][-1], config['MA_PERIOD'])}
	"""
if __name__ == "__main__":
	data = {
	"coins":{
		"bitcoin" :{
			"close": [
				64000,64230,63980,64500,65000,
				64800,65200,65600,65100,64900,
				65300,65800,66200,66000,65700,
				65500,65900,66300,66700,67000
					]
			},
		"ethereum" :{
			"close": [
				3400,3380,3420,3390,3450,
				3470,3440,3460,3500,3480,
				3520,3510,3540,3560,3530,
				3550,3580,3600,3590,3620
					]
			}
		},
	"config":{
		"MA_PERIOD" : 3,
		"RSI_PERIOD" : 14
		}
	}
	hasil = [buat_laporan(key, value, data["config"]) for value, key in data["coins"].items()]
	print("\n".join(hasil))