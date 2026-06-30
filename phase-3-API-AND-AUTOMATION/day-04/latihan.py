from tabulate import tabulate
k = {
"bitcoin" :{"Harga" : 32000, "Change" : "+2.5%"},
"ethereum" :{"Harga" : 2000, "Change" : "-1.25%"},
"solana" :{"Harga" : 100, "Change" : "+1.28%"},
"binance coin" :{"Harga" : 100, "Change" : "+7.7%"},
"xrp" : {"Harga" : 2000, "Change" : "+5.2%"}
}
while True:
	lol = []
	inf = input("masukan")
	if inf == "1":
		for coin, info in k.items():
			lol.append({"Coin" : coin.title(), "Harga" : info["Harga"], "Change" : info["Change"]})
		print(tabulate(lol, headers="keys", tablefmt="grid"))
	elif inf == "2":
		for coin, info in k.items():
			lol.append([coin.title(), info["Harga"], info["Change"]])
		head = ["COINS","PRICES","CHANGE"]
		print(tabulate(lol, headers=head, tablefmt="grid"))
	else:
		break
	print(lol)
#perbandingan