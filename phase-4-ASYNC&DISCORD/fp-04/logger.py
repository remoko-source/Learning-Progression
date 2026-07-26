import logging
from pathlib import Path
def get_logger():
	log_path = Path(__file__).parent / "logs" / "bot.log"
	logger = logging.getLogger("PH_04") ; logger.setLevel(logging.DEBUG)
	file = logging.FileHandler(log_path) ; file.setLevel(logging.INFO)
	visual = logging.StreamHandler() ; visual.setLevel(logging.ERROR)
	
	time_format = logging.Formatter("%(asctime)s - %(levelname)s | %(message)s","%Y/%m/%d %H:%M:%S")
	file.setFormatter(time_format) ; visual.setFormatter(time_format)
	
	logger.addHandler(file) ; logger.addHandler(visual)
	return logger