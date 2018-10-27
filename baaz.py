class Baaz:

	def __init__(self):
		self.fv = 0
        self.BAAZ_MAX = 10
        self.BAAZ_MIN = -10
        self.BABA_MAX = 10
        self.BABA_MIN = -10

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
        tpos = position['BAAZ']
		while index < len(buy_list) and tpos > self.BAAZ_MIN and buy_list[index][0] > self.fv:
			if tpos - self.BAAZ_MIN < buy_list[index][1]:
				trade_size = tpos - self.BAAZ_MIN
			else:
				trade_size = buy_list[index][1]
			trades.append({'type': 'add', 'order_id': order_obj.getOrder(), 'symbol': 'BAAZ', 'dir': 'SELL', 'price': buy_list[index][0],'size': trade_size})
            tpos -= trade_size
			print("trades: ", trades)
			index += 1

        baba_pos = position['BABA']
        while index < len(buy_list) and baba_pos > self.BABA_MIN and buy_list[index][0] - (buy_list[index][1] / 10) > self.fv:
            if baba_pos - self.BABA_MIN < buy_list[index][1]:
                trade_size = baba_pos - self.BABA_MIN
            else:
                trade_size = buy_list[index][1]
            trades.append({'type' : 'convert', 'order_id' : order_obj.getOrder(), 'symbol' : 'BAAZ', 'dir' : 'BUY', 'size' : trade_size})
            trades.append({'type': 'add', 'order_id': order_obj.getOrder(), 'symbol': 'BAAZ', 'dir': 'SELL', 'price': buy_list[index][0],'size': trade_size})
            babapos -= trade_size
            print("trades: ", trades)
            index += 1

		index = 0
		while index < len(sell_list) and position['BAAZ'] < self.BAAZ_MAX and sell_list[index][0] < self.fv:
			if self.BAAZ_MAX - position['BAAZ'] < sell_list[index][1]:
				trade_size = self.BAAZ_MAX - position['BAAZ']
			else:
				trade_size = sell_list[index][1]
			trades.append({'type': 'add', 'order_id': order_obj.getOrder(), 'symbol': 'BAAZ', 'dir': 'BUY', 'price': sell_list[index][0], 'size': trade_size})
            tpos += trade_size
			index += 1

        while index < len(buy_list) and baba_pos < self.BABA_MAX and sell_list[index][0] + (sell_list[index][1] / 10) > self.fv:
            if self.BABA_MAX - baba_pos < sell_list[index][1]:
                trade_size =  self.BABA_MAX - baba_pos
            else:
                trade_size = buy_list[index][1]
            trades.append({'type' : 'convert', 'order_id' : order_obj.getOrder(), 'symbol' : 'BAAZ', 'dir' : 'SELL', 'size' : trade_size})
            trades.append({'type': 'add', 'order_id': order_obj.getOrder(), 'symbol': 'BAAZ', 'dir': 'BUY', 'price': sell_list[index][0],'size': trade_size})
            babapos += trade_size
            print("trades: ", trades)
            index += 1

		# for trade in trades:
		# 	all_trades[trade['order_id']] = trade

		return trades
