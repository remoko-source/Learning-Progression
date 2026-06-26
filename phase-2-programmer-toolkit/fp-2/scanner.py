from pathlib import Path
import json
def get_paths():
	base = Path(__file__).parent
	return {
	"logs" : base / "logs", "data" : base / "data",
	"trades" : base / "data" / "trades.json", "log_file" : base / "logs" / "tradedesk.log"
	}
def check():
	paths = get_paths()
	paths["logs"].mkdir(parents=True, exist_ok=True)
	paths["data"].mkdir(parents=True, exist_ok=True)
	l = []
	if not paths["log_file"].exists():
		with open(paths["log_file"],"w") as file:
			file.write("")
		print("tradedesk.log berhasil dibuat")
	if not paths["trades"].exists():
		with open(paths["trades"], "w") as file:
			json.dump(l, file)
		print("trades.json berhasil dibuat")