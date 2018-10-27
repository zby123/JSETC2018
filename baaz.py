class Baaz:

    def __init__(self):
        self.fv = 0
        self.BAAZ_MAX = 10
        self.BAAZ_MIN = -10
    
    def fairvalue(self, book):
        buy = book['BABA']['BUY'][0][0]
        sell = book['BABA']['SELL'][0][0]
        return (buy + sell) / 2
    
    def tradeBAAZ(self, book, order_id, position, all_trades):
        trades = []
        self.fv = fairvalue(book)
        buy_list = book['BAAZ']['BUY']
        sell_list = book['BAAZ']['SELL']
        
        index = 0
        trade_size = 0
        while index < len(buy_list) and position['BAAZ'] > self.BAAZ_MIN and buy_list[index][0] > self.fv:
            if position['BAAZ'] - self.BAAZ_MIN < buy_list[index][1]:
                trade_size = position['BAAZ'] - self.BAAZ_MIN
            else 
                trade_size = buy_list[index][1]
            trades.append({'type':'add', 'order_id':order_id.getID(), 'symbol':'BAAZ', 'dir':'SELL', 'size':trade_size})
            index += 1
        
        index = 0
        while index < len(sell_list) and position['BAAZ'] < self.BAAZ_MAX and sell_list[index][0] < self.fv:
            if self.BAAZ_MAX - position['BAAZ']:
                trade_size = self.BAAZ_MAX - position['BAAZ']
            else 
                trade_size = sell_list[index][1]
            trades.append({'type':'add', 'order_id':order_id.getID(), 'symbol':'BAAZ', 'dir':'BUY', 'size':trade_size})
            index += 1

        for trade in trades:
            all_trades[trade['order_id']] = trade
        
        return trades