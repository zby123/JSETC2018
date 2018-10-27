class Bond:
	def __init__(self):
		pass

	def trade(self, order_obj, positions, all_trades):
		trades = [
			{'type': 'add', 'order_id': order_obj.getOrder(), 'symbol': 'BOND', 'dir': 'BUY', 'price': 999, 'size': 100 - positions['BOND']},
			{'type': 'add', 'order_id': order_obj.getOrder(), 'symbol': 'BOND', 'dir': 'SELL', 'price': 1001, 'size': 100 + positions['BOND']}]
		return trades

	def hello(self):
		print("Bond say hello")
