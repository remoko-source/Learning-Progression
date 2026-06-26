from pathlib import Path ; from datetime import datetime
import json ; from scanner import get_paths
paths = get_paths()
def load_trades():
	with open(paths["trades"], "r") as file:
		data = json.load(file)
	return data
def save_trades(trades):
	with open(paths["trades"], "w") as file:
		json.dump(trades, file, indent=4)
def add_trade(coin, entry_price, status, pnl):
	trades = load_trades()
	if len(trades) == 0:
		id = 1
	else:
		id = trades[-1]["id"] + 1
	new = {
	"id" : id,
	"coin" : coin,
	"entry_price" : entry_price,
	"status" : status,
	"pnl" : pnl,
	"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	}
	trades.append(new)
	save_trades(trades)
	
def update_trade(sell, id):
	list = load_trades()
	pnl = sell - list[id-1]["entry_price"]
	if pnl > 0:
		status = "WIN"
	else:
		status = "LOSS"
	new = {
	"id" : id,
	"coin" : list[id-1]["coin"],
	"entry_price" : list[id-1]["entry_price"],
	"status" : status,
	"pnl" : pnl,
	"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	}
	trades = load_trades()
	trades[id-1] = new
	save_trades(trades)