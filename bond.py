class Bond:
	def __init__(self):
		pass

	def trade(self, order_obj, all_trades):
		trades = [
			{'type': 'add', 'order_id': order_obj.getOrder(), 'symbol': 'BOND', 'dir': 'BUY', 'price': 999, 'size': 85},
			{'type': 'add', 'order_id': order_obj.getOrder(), 'symbol': 'BOND', 'dir': 'BUY', 'price': 998, 'size': 10},
			{'type': 'add', 'order_id': order_obj.getOrder(), 'symbol': 'BOND', 'dir': 'BUY', 'price': 997, 'size': 5},
			{'type': 'add', 'order_id': order_obj.getOrder(), 'symbol': 'BOND', 'dir': 'SELL', 'price': 1001, 'size': 85},
			{'type': 'add', 'order_id': order_obj.getOrder(), 'symbol': 'BOND', 'dir': 'SELL', 'price': 1002, 'size': 10},
			{'type': 'add', 'order_id': order_obj.getOrder(), 'symbol': 'BOND', 'dir': 'SELL', 'price': 1003, 'size': 5}]
		return trades

	def hello(self):
		print("Bond say hello")
