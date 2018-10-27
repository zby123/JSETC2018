class Baaz:

	def __init__(self):
		self.fv = 0
		self.BAAZ_MAX = 10
		self.BAAZ_MIN = -10

	def fairvalue(self, book):
		if 'BABA' in book and 'buy' in book['BABA'] and 'sell' in book['BABA'] and \
			'BAAZ' in book and 'buy' in book['BAAZ'] and 'sell' in book['BAAZ'] and \
				len(book['BABA']['buy']) > 0 and len(book['BABA']['sell']) > 0:
			# print("fairvalue: ", book['BABA']['buy'], book['BABA']['sell'])
			buy = book['BABA']['buy'][0][0]
			sell = book['BABA']['sell'][0][0]
			return (buy + sell) / 2
		else:
			return -1

	def trade(self, book, order_obj, position, all_trades):
		trades = []
		self.fv = self.fairvalue(book)
		if self.fv == -1:
			print("no BAAZ in book")
			return trades

		print("try to order")
		buy_list = book['BAAZ']['buy']
		sell_list = book['BAAZ']['sell']

		index = 0
		trade_size = 0

		print("BABA debug: ", index, buy_list, position['BAAZ'], self.fv)
		while index < len(buy_list) and position['BAAZ'] > self.BAAZ_MIN and buy_list[index][0] > self.fv:
			if position['BAAZ'] - self.BAAZ_MIN < buy_list[index][1]:
				trade_size = position['BAAZ'] - self.BAAZ_MIN
			else:
				trade_size = buy_list[index][1]
			trades.append({'type': 'add', 'order_id': order_obj.getOrder(), 'symbol': 'BAAZ', 'dir': 'SELL', 'price': buy_list[index][0],'size': trade_size})
			print("trades: ", trades)
			index += 1

		index = 0
		while index < len(sell_list) and position['BAAZ'] < self.BAAZ_MAX and sell_list[index][0] < self.fv:
			if self.BAAZ_MAX - position['BAAZ']:
				trade_size = self.BAAZ_MAX - position['BAAZ']
			else:
				trade_size = sell_list[index][1]
			trades.append({'type': 'add', 'order_id': order_obj.getOrder(), 'symbol': 'BAAZ', 'dir': 'BUY', 'price': sell_list[index][0], 'size': trade_size})
			index += 1

		# for trade in trades:
		# 	all_trades[trade['order_id']] = trade

		return trades
