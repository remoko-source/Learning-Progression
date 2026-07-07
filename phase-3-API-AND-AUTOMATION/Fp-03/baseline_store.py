from pathlib import Path
from logger import get_logger
import json
import sys
def get_paths():
	base = Path(__file__).parent
	return {
	"logs_path" : base / "system.log" , "config" : base / "config.json", 
	"storage" : base / "baseline.json"
	}
	
def load_config():
	paths = get_paths()
	if not paths["config"].exists():
		logger = get_logger()
		logger.critical("ERROR: config tidak ditemukan")
		sys.exit()
	with open(paths["config"], "r") as file:
		data = json.load(file)
	return data

def load_baseline():
	paths = get_paths()
	if not paths["storage"].exists():
		return {}
	try:
		with open(paths["storage"], "r") as file:
			data = json.load(file)
		return data
	except json.JSONDecodeError :
		return {}
	
def save_baseline(save_data):
	paths = get_paths()
	with open(paths["storage"], "w") as file:
		json.dump(save_data, file, indent=4)