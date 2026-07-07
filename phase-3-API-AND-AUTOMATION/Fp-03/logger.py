import logging
def get_logger():
	logger = logging.getLogger("PH_03") ; logger.setLevel(logging.DEBUG)
	file = logging.FileHandler("data.log") ; file.setLevel(logging.INFO)
	visual = logging.StreamHandler() ; visual.setLevel(logging.ERROR)
	
	time_format = logging.Formatter("%(asctime)s - %(levelname)s | %(message)s","%Y/%m/%d %H:%M:%S")
	file.setFormatter(time_format) ; visual.setFormatter(time_format)
	
	logger.addHandler(file) ; logger.addHandler(visual)
	return logger