class Shoe:

	def __init__(self):
		self.fv = 0
		self.SHOE_MAX = 100
		self.SHOE_MIN = -100
		self.BOND_MAX = 100
		self.BOND_MIN = -100
		self.NIKE_MAX = 100
		self.NIKE_MIN = -100
		self.ADID_MAX = 100
		self.ADID_MIN = -100
		self.FYUE_MAX = 100
		self.FYUE_MIN = -100
		self.CONVERT_COST = 100

	def fairvalue(self, book):
		if 'BOND' in book and 'buy' in book['BOND'] and 'sell' in book['BOND'] and \
		'NIKE' in book and 'buy' in book['NIKE'] and 'sell' in book['NIKE'] and \
		'ADID' in book and 'buy' in book['ADID'] and 'sell' in book['ADID'] and \
		'FYUE' in book and 'buy' in book['FYUE'] and 'sell' in book['FYUE'] and \
			'SHOE' in book and 'buy' in book['SHOE'] and 'sell' in book['SHOE'] and \
				len(book['BOND']['buy']) > 0 and len(book['BOND']['sell']) > 0 and \
				len(book['NIKE']['buy']) > 0 and len(book['NIKE']['sell']) > 0 and \
				len(book['ADID']['buy']) > 0 and len(book['ADID']['sell']) > 0 and \
				len(book['FYUE']['buy']) > 0 and len(book['FYUE']['sell']) > 0:
			# print("fairvalue: ", book['SHOE']['buy'], book['SHOE']['sell'])
			buy = 3000
			tbuy = tbuys = 0
			for i in range(min(3, len(book['NIKE']['buy']))):
				tbuy += book['NIKE']['buy'][0][0] * 2 * book['NIKE']['buy'][0][1]
				tbuys += book['NIKE']['buy'][0][1]
			buy += tbuy / tbuys

			tbuy = tbuys = 0
			for i in range(min(3, len(book['ADID']['buy']))):
				tbuy += book['ADID']['buy'][0][0] * 3 * book['ADID']['buy'][0][1]
				tbuys += book['ADID']['buy'][0][1]
			buy += tbuy / tbuys

			tbuy = tbuys = 0
			for i in range(min(3, len(book['FYUE']['buy']))):
				tbuy += book['FYUE']['buy'][0][0] * 2 * book['FYUE']['buy'][0][1]
				tbuys += book['FYUE']['buy'][0][1]
			buy += tbuy / tbuys

			sell = 3000
			tsell = tsells = 0
			for i in range(min(3, len(book['NIKE']['sell']))):
				tsell += book['NIKE']['sell'][0][0] * 2 * book['NIKE']['sell'][0][1]
				tsells += book['NIKE']['sell'][0][1]
			sell += tsell / tsells

			tsell = tsells = 0
			for i in range(min(3, len(book['ADID']['sell']))):
				tsell += book['ADID']['sell'][0][0] * 3 * book['ADID']['sell'][0][1]
				tsells += book['ADID']['sell'][0][1]
			sell += tsell / tsells

			tsell = tsells = 0
			for i in range(min(3, len(book['FYUE']['sell']))):
				tsell += book['FYUE']['sell'][0][0] * 2 * book['FYUE']['sell'][0][1]
				tsells += book['FYUE']['sell'][0][1]
			sell += tsell / tsells
			
			return (buy + sell) / 20
		else:
			return -1

	def trade(self, book, order_obj, position, all_trades):
		trades = []
		self.fv = self.fairvalue(book)
		if self.fv == -1:
			# print("no SHOE in book")
			return trades

		# print("try to order")
		buy_list = book['SHOE']['buy']
		sell_list = book['SHOE']['sell']

		index = 0
		trade_size = 0

		# print("SHOE debug: ", index, buy_list, position['SHOE'], self.fv)
		while index < len(buy_list) and position['SHOE'] > self.SHOE_MIN and buy_list[index][0] > self.fv:
			if position['SHOE'] - self.SHOE_MIN < buy_list[index][1]:
				trade_size = position['SHOE'] - self.SHOE_MIN
			else:
				trade_size = buy_list[index][1]
			trades.append({'type': 'add', 'order_id': order_obj.getOrder(), 'symbol': 'SHOE', 'dir': 'SELL', 'price': buy_list[index][0],'size': trade_size})
			# print("trades: ", trades)
			index += 1

		index = 0
		while index < len(sell_list) and position['SHOE'] < self.SHOE_MAX and sell_list[index][0] < self.fv:
			if self.SHOE_MAX - position['SHOE']:
				trade_size = self.SHOE_MAX - position['SHOE']
			else:
				trade_size = sell_list[index][1]
			trades.append({'type': 'add', 'order_id': order_obj.getOrder(), 'symbol': 'SHOE', 'dir': 'BUY', 'price': sell_list[index][0], 'size': trade_size})
			index += 1

		# for trade in trades:
		# 	all_trades[trade['order_id']] = trade

		return trades

	def shoe2other(self, book, order_obj, position):
		trades = []
		if 'SHOE' in book and 'BAAZ' in book and 'NIKE' in book and 'ADID' in book and 'FYUE' in book and 'BOND' in book and \
				len(book['BOND']['sell']) > 0 and len(book['BOND']['buy']) > 0 and \
				len(book['SHOE']['sell']) > 0 and len(book['SHOE']['buy']) > 0 and \
				len(book['BAAZ']['sell']) > 0 and len(book['BAAZ']['buy']) > 0 and \
				len(book['NIKE']['sell']) > 0 and len(book['NIKE']['buy']) > 0 and \
				len(book['ADID']['sell']) > 0 and len(book['ADID']['buy']) > 0 and \
				len(book['FYUE']['sell']) > 0 and len(book['FYUE']['buy']) > 0:
			shoe_sell_price = book['SHOE']['sell'][0][0]
			bond_buy_price = book['BOND']['buy'][0][0]
			nike_buy_price = book['NIKE']['buy'][0][0]
			adid_buy_price = book['ADID']['buy'][0][0]
			fyue_buy_price = book['FYUE']['buy'][0][0]

			trade_size = min(book['SHOE']['sell'][0][1] / 10, (self.BOND_MAX - position['BOND']) / 3,
											 (self.NIKE_MAX - position['NIKE']) / 2, (self.ADID_MAX - position['ADID']) / 3,
											 (self.FYUE_MAX - position['FYUE']) / 2)
			# print('out trade size ', trade_size)
			if shoe_sell_price * 10 * trade_size + self.CONVERT_COST < (3 * (bond_buy_price - 1) + 2 * (nike_buy_price - 1) + 3 * (adid_buy_price - 1) +  \
				2 * (fyue_buy_price - 1)) * trade_size:
				# print('in trade size ', trade_size)
				trades.append(
					{'type': 'add', 'order_id': order_obj.getOrder(), 'symbol': 'SHOE', 'dir': 'BUY', 'price': shoe_sell_price,
					 'size': trade_size * 10})
				trades.append(
					{'type': 'convert', 'order_id': order_obj.getOrder(), 'symbol': 'SHOE', 'dir': 'SELL', 'size': trade_size * 10})
				trades.append(
					{'type': 'add', 'order_id': order_obj.getOrder(), 'symbol': 'BOND', 'dir': 'SELL', 'price': bond_buy_price - 1,
					 'size': trade_size * 3})
				trades.append(
					{'type': 'add', 'order_id': order_obj.getOrder(), 'symbol': 'NIKE', 'dir': 'SELL', 'price': nike_buy_price - 1,
					 'size': trade_size * 2})
				trades.append(
					{'type': 'add', 'order_id': order_obj.getOrder(), 'symbol': 'ADID', 'dir': 'SELL', 'price': adid_buy_price - 1,
					 'size': trade_size * 3})
				trades.append(
					{'type': 'add', 'order_id': order_obj.getOrder(), 'symbol': 'FYUE', 'dir': 'SELL', 'price': fyue_buy_price - 1,
					 'size': trade_size * 2})
		return trades


	def other2shoe(self, book, order_obj, position):
		trades = []
		if 'SHOE' in book and 'BAAZ' in book and 'NIKE' in book and 'ADID' in book and 'FYUE' in book and 'BOND' in book and \
				len(book['BOND']['sell']) > 0 and len(book['BOND']['buy']) > 0 and \
				len(book['SHOE']['sell']) > 0 and len(book['SHOE']['buy']) > 0 and \
				len(book['BAAZ']['sell']) > 0 and len(book['BAAZ']['buy']) > 0 and \
				len(book['NIKE']['sell']) > 0 and len(book['NIKE']['buy']) > 0 and \
				len(book['ADID']['sell']) > 0 and len(book['ADID']['buy']) > 0 and \
				len(book['FYUE']['sell']) > 0 and len(book['FYUE']['buy']) > 0:
			shoe_buy_price = book['SHOE']['buy'][0][0]
			bond_sell_price = book['BOND']['sell'][0][0]
			nike_sell_price = book['NIKE']['sell'][0][0]
			adid_sell_price = book['ADID']['sell'][0][0]
			fyue_sell_price = book['FYUE']['sell'][0][0]

			trade_size = min(self.SHOE_MAX - position['SHOE'] / 10, book['BOND']['sell'][0][1] / 3,
											 book['NIKE']['sell'][0][1] / 2, book['ADID']['sell'][0][1] / 3,
											 book['FYUE']['sell'][0][1] / 2)

			# print('out trade size ', trade_size)
			if (shoe_buy_price - 1) * 10 * trade_size > (3 * bond_sell_price + 2 * nike_sell_price + 3 * adid_sell_price +  \
				2 * fyue_sell_price) * trade_size + self.CONVERT_COST:
				# print('in trade size ', trade_size)
				trades.append(
					{'type': 'add', 'order_id': order_obj.getOrder(), 'symbol': 'BOND', 'dir': 'BUY', 'price': bond_sell_price,
					 'size': trade_size * 3})
				trades.append(
					{'type': 'add', 'order_id': order_obj.getOrder(), 'symbol': 'NIKE', 'dir': 'BUY', 'price': nike_sell_price,
					 'size': trade_size * 2})
				trades.append(
					{'type': 'add', 'order_id': order_obj.getOrder(), 'symbol': 'ADID', 'dir': 'BUY', 'price': adid_sell_price,
					 'size': trade_size * 3})
				trades.append(
					{'type': 'add', 'order_id': order_obj.getOrder(), 'symbol': 'FYUE', 'dir': 'BUY', 'price': fyue_sell_price,
					 'size': trade_size * 2})
				trades.append(
					{'type': 'convert', 'order_id': order_obj.getOrder(), 'symbol': 'SHOE', 'dir': 'BUY', 'size': trade_size * 10})
				trades.append(
					{'type': 'add', 'order_id': order_obj.getOrder(), 'symbol': 'SHOE', 'dir': 'SELL', 'price': shoe_buy_price - 1,
					 'size': trade_size * 10})
		return trades

