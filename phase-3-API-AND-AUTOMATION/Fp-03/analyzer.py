def calculate_change(current_price, baseline_price):
	if baseline_price is None:
		return None
	return (current_price - baseline_price) / baseline_price * 100

def is_mover(percent_change, threshold):
	if percent_change is None:
		return False
	return abs(percent_change) >= threshold