class Baaz:

	def __init__(self):
		self.fv = 0
		self.BAAZ_MAX = 10
		self.BAAZ_MIN = -10
		self.BABA_MAX = 10
		self.BABA_MIN = -10
		self.CONVERT_COST = 10

	def fairvalue(self, book):
		if 'BABA' in book and 'buy' in book['BABA'] and 'sell' in book['BABA'] and \
				'BAAZ' in book and 'buy' in book['BAAZ'] and 'sell' in book['BAAZ'] and \
				len(book['BABA']['buy']) > 0 and len(book['BABA']['sell']) > 0:
			# print("fairvalue: ", book['BABA']['buy'], book['BABA']['sell'])
			buy = buys = 0

			for i in range(min(3, len(book['BABA']['buy']))):
				buy += book['BABA']['buy'][i][0] * book['BABA']['buy'][i][1]
				buys += book['BABA']['buy'][i][1]

			sell = sells = 0
			for i in range(min(3, len(book['BABA']['sell']))):
				buy += book['BABA']['sell'][i][0] * book['BABA']['sell'][i][1]
				buys += book['BABA']['sell'][i][1]
			return (buy + sell) / (buys + sells)
		else:
			return -1

	def baaz2baba(self, book, order_obj, position):
		trades = []
		if 'BAAZ' in book and 'sell' in book['BAAZ'] and len(book['BAAZ']['sell']) > 0 and \
				'BABA' in book and 'buy' in book['BABA'] and len(book['BABA']['buy']) > 0:
			baaz_sell_list = book['BAAZ']['sell']
			baba_buy_list = book['BABA']['buy']
			baaz_sell_price = baaz_sell_list[0][0]
			baba_buy_price = baba_buy_list[0][0]
			trade_size = min(baaz_sell_list[0][1], self.BAAZ_MAX - position['BAAZ'], baba_buy_list[0][1],
											 self.BABA_MAX - position['BABA'])

			print('out trade size ', trade_size)
			if (baaz_sell_price * trade_size + self.CONVERT_COST < baba_buy_price * trade_size):
				print('in trade size ', trade_size)
				trades.append(
					{'type': 'add', 'order_id': order_obj.getOrder(), 'symbol': 'BAAZ', 'dir': 'BUY', 'price': baaz_sell_price,
					 'size': trade_size})
				trades.append(
					{'type': 'convert', 'order_id': order_obj.getOrder(), 'symbol': 'BAAZ', 'dir': 'SELL', 'size': trade_size})
				trades.append(
					{'type': 'add', 'order_id': order_obj.getOrder(), 'symbol': 'BABA', 'dir': 'SELL', 'price': baba_buy_price,
					 'size': trade_size})
		return trades

	def baba2baaz(self, book, order_obj, position):
		trades = []
		if 'BABA' in book and 'sell' in book['BABA'] and len(book['BABA']['sell']) > 0 and \
				'BAAZ' in book and 'buy' in book['BAAZ'] and len(book['BAAZ']['buy']) > 0:
			baba_sell_list = book['BABA']['sell']
			baaz_buy_list = book['BAAZ']['buy']
			baba_sell_price = baba_sell_list[0][0]
			baaz_buy_price = baaz_buy_list[0][0]
			trade_size = min(baba_sell_list[0][1], self.BABA_MAX - position['BABA'], baaz_buy_list[0][1],
											 self.BAAZ_MAX - position['BAAZ'])

			print('out trade size ', trade_size)
			if (baba_sell_price * trade_size + self.CONVERT_COST < baaz_buy_price * trade_size):
				print('in trade size ', trade_size)
				trades.append(
					{'type': 'add', 'order_id': order_obj.getOrder(), 'symbol': 'BABA', 'dir': 'BUY', 'price': baba_sell_price,
					 'size': trade_size})
				trades.append(
					{'type': 'convert', 'order_id': order_obj.getOrder(), 'symbol': 'BAAZ', 'dir': 'BUY', 'size': trade_size})
				trades.append(
					{'type': 'add', 'order_id': order_obj.getOrder(), 'symbol': 'BAAZ', 'dir': 'SELL', 'price': baaz_buy_price,
					 'size': trade_size})
		return trades

	def trade(self, book, order_obj, position, all_trades):
		trades = []
		self.fv = self.fairvalue(book)
		if self.fv == -1:
			# print("no BAAZ in book")
			return trades

		# print("try to order")
		buy_list = book['BAAZ']['buy']
		sell_list = book['BAAZ']['sell']

		index = 0
		trade_size = 0

		# print("BABA debug: ", index, buy_list, position['BAAZ'], self.fv)
		while index < len(buy_list) and position['BAAZ'] > self.BAAZ_MIN and buy_list[index][0] > self.fv:
			if position['BAAZ'] - self.BAAZ_MIN < buy_list[index][1]:
				trade_size = position['BAAZ'] - self.BAAZ_MIN
			else:
				trade_size = buy_list[index][1]
			trades.append(
				{'type': 'add', 'order_id': order_obj.getOrder(), 'symbol': 'BAAZ', 'dir': 'SELL', 'price': buy_list[index][0],
				 'size': trade_size})
			# print("trades: ", trades)
			index += 1

		index = 0
		while index < len(sell_list) and position['BAAZ'] < self.BAAZ_MAX and sell_list[index][0] < self.fv:
			if self.BAAZ_MAX - position['BAAZ']:
				trade_size = self.BAAZ_MAX - position['BAAZ']
			else:
				trade_size = sell_list[index][1]
			trades.append(
				{'type': 'add', 'order_id': order_obj.getOrder(), 'symbol': 'BAAZ', 'dir': 'BUY', 'price': sell_list[index][0],
				 'size': trade_size})
			index += 1

		# for trade in trades:
		#   all_trades[trade['order_id']] = trade

		return trades
