class Bond:
	def __init__(self):
		pass

	def trade(self):
		trades = [{'type': 'add', 'order_id': 0, 'symbol': 'BOND', 'dir': 'BUY', 'price': 999, 'size': 10},
						  {'type': 'add', 'order_id': 1, 'symbol': 'BOND', 'dir': 'SELL', 'price': 1001, 'size': 10}]
		# for trade in trades:
		# 	all_trades[trade['order_id']] = trade
		return trades

	def hello(self):
		print("Bond say hello")