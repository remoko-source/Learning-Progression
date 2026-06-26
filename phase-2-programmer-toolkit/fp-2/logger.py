from pathlib import Path
import logging ; from scanner import get_paths
def setup_logging():
#==========================================================================================
	#GET PATH
	paths = get_paths()
#==========================================================================================
	#LOGGER
	logger = logging.getLogger("main") ; logger.setLevel(logging.DEBUG)
	files = logging.FileHandler(paths["log_file"]) ; files.setLevel(logging.INFO)
	
	#FORMAT
	format = logging.Formatter("%(asctime)s %(levelname)s|%(message)s", "%d/%m/%Y - %H:%M:%S")
	files.setFormatter(format)

	#ADD HANDLER
	logger.addHandler(files)
#==========================================================================================
	return logger