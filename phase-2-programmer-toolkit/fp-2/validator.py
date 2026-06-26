#=====================================================================
#CUSTOM EXCEPTION
class TradeValidationError(Exception):			pass
class InvalidCoinError(TradeValidationError):	pass
class InvalidPricesError(TradeValidationError):	pass
class InvalidStatusError(TradeValidationError):	pass
class InvalidPnlError(TradeValidationError):	pass
#=====================================================================
#ERROR CHECK FUNCTION
def validate_coin(coin):
	if len(coin) == 0:
		raise InvalidCoinError("COIN tidak boleh kosong")
def validate_prices(price):
	try:
		price = float(price)
		if price <= 0:
			raise InvalidPricesError("Harga awal tidak boleh kurang atau sama dengan 0")
	except ValueError:
		raise InvalidPricesError("Harga bukanlah Angka")
def validate_status(status):
	if status == "OPEN" or status == "WIN" or status == "LOSS":
		pass
	else:
		raise InvalidStatusError("STATUS tidak Valid")
def validate_pnl(pnl):
	try:
		float(pnl)
	except ValueError:
		raise InvalidPnlError("PnL bukanlah Angka")
def validate_trade(coin, price, status, pnl):
	
	validate_coin(coin)
	validate_prices(price)
	validate_status(status)
	validate_pnl(pnl)
	return True
#=====================================================================