#!/usr/bin/python

# ~~~~~==============   HOW TO RUN   ==============~~~~~
# 1) Configure things in CONFIGURATION section
# 2) Change permissions: chmod +x test-bot.py
# 3) Run in loop: while true; do ./test-bot.py; sleep 1; done

from __future__ import print_function

import sys
import socket
import json
import bond
import baaz
import shoe
# ~~~~~============== CONFIGURATION  ==============~~~~~
# replace REPLACEME with your team name!
team_name = "Furret"
# This variable dictates whether or not the bot is connecting to the prod
# or test exchange. Be careful with this switch!
test_mode = False

# This setting changes which test exchange is connected to.
# 0 is prod-like
# 1 is slower
# 2 is empty
test_exchange_index = 0
prod_exchange_hostname = "production"

port = 25000 + (test_exchange_index if test_mode else 0)
exchange_hostname = "test-exch-" + team_name if test_mode else prod_exchange_hostname


# ~~~~~============== NETWORKING CODE ==============~~~~~
def connect():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((exchange_hostname, port))
	return s.makefile('rw', 1)


def write_to_exchange(exchange, obj):
	json.dump(obj, exchange)
	exchange.write("\n")


def read_from_exchange(exchange):
	return json.loads(exchange.readline())

class Order:
	def __init__(self):
		self.order = 0

	def getOrder(self):
		ret = self.order
		self.order += 1
		return ret


# ~~~~~============== MAIN LOOP ==============~~~~~

def main():
	exchange = connect()
	write_to_exchange(exchange, {"type": "hello", "team": team_name.upper()})
	hello_from_exchange = read_from_exchange(exchange)

	# A common mistake people make is to call write_to_exchange() > 1
	# time for every read_from_exchange() response.
	# Since many write messages generate marketdata, this will cause an
	# exponential explosion in pending messages. Please, don't do that!

	cash = [0]
	positions = {'BOND': 0, 'BABZ': 0, 'BABA': 0, 'AAPL': 0, 'MSFT': 0, 'GOOG': 0, 'XLK': 0}
	book = {}
	all_trades = {}
	order_obj = Order()

	# print("The exchange replied:", hello_from_exchange, file=sys.stderr)
	# print(type(hello_from_exchange))
	# print(hello_from_exchange.keys())

	for item in hello_from_exchange["symbols"]:
		positions[item['symbol']] = item['position']
	# print(positions)

	bond_obj = bond.Bond()

	# bond_obj.hello()
	trades = bond_obj.trade(order_obj, positions, all_trades)
	for trade in trades:
		all_trades[trade['order_id']] = trade
		write_to_exchange(exchange, trade)


	baaz_obj = baaz.Baaz()
	# trades = baaz_obj.trade(book, order_obj, positions, all_trades)
	# for trade in trades:
	# 	all_trades[trade['order_id']] = trade
	# 	write_to_exchange(exchange, trade)

	trades = baaz_obj.baba2baaz(book, order_obj, positions)
	for trade in trades:
		all_trades[trade['order_id']] = trade
		write_to_exchange(exchange, trade)

	trades = baaz_obj.baaz2baba(book, order_obj, positions)
	for trade in trades:
		all_trades[trade['order_id']] = trade
		write_to_exchange(exchange, trade)

	shoe_obj = shoe.Shoe()
	trades = shoe_obj.trade(book, order_obj, positions, all_trades)
	for trade in trades:
		all_trades[trade['order_id']] = trade
		write_to_exchange(exchange, trade)



	counter = 0

	reply = read_from_exchange(exchange)
	if(reply['type'] == 'reject'):
		return

	book_ctr = 0
	while (1):
		book_ctr += 1
		if (book_ctr % 100 == 0):
			if 'BABA' in book and 'BAAZ' in book and \
				len(book['BABA']['sell']) > 0 and len(book['BABA']['buy']) > 0 and \
				len(book['BAAZ']['sell']) > 0 and len(book['BAAZ']['buy']) > 0 :
				print("BABA: ", 'sell:', book['BABA']['sell'][0][0], ' buy:', book['BABA']['buy'][0][0], ' ', end="")
				print("BAAZ: ", 'sell:', book['BAAZ']['sell'][0][0], ' buy:', book['BAAZ']['buy'][0][0])
			book_ctr = 0

		reply = read_from_exchange(exchange)

		if (reply['type'] == 'book'):
			counter += 1
			# print(1)
			# print("book: ", reply)
			book[reply['symbol']] = {'buy': reply['buy'], 'sell': reply['sell']}
			if counter % 100 == 0:
				# trades = baaz_obj.trade(book, order_obj, positions, all_trades)
				# for trade in trades:
				# 	all_trades[trade['order_id']] = trade
				# 	write_to_exchange(exchange, trade)

				trades = baaz_obj.baba2baaz(book, order_obj, positions)
				for trade in trades:
					all_trades[trade['order_id']] = trade
					write_to_exchange(exchange, trade)

				trades = baaz_obj.baaz2baba(book, order_obj, positions)
				for trade in trades:
					all_trades[trade['order_id']] = trade
					write_to_exchange(exchange, trade)


				trades = shoe_obj.trade(book, order_obj, positions, all_trades)
				for trade in trades:
					all_trades[trade['order_id']] = trade
					write_to_exchange(exchange, trade)
				counter = 0

		elif (reply['type'] == 'fill'):
			# print(2)
			if (reply['dir'] == 'buy'):
				positions[reply['symbol']] += reply['size']
				cash -= reply['size'] * reply['price']
				all_trades[reply['order_id']] -= reply['size']
				if (all_trades[reply['order_id']] == 0):
					all_trades.pop(reply['order_id'])

			elif (reply['dir'] == 'sell'):
				# print(3)
				positions[reply['symbol']] -= reply['size']
				cash += reply['size'] * reply['price']
				all_trades[reply['order_id']] -= reply['size']
				if (all_trades[reply['order_id']] == 0):
					all_trades.pop(reply['order_id'])
			# print("log, fill-reply received: ", reply)

		elif (reply['type'] == 'out'):
			# print(4)
			trades = bond_obj.trade(order_obj, positions, all_trades)
			for trade in trades:
				all_trades[trade['order_id']] = trade
				write_to_exchange(exchange, trade)

		elif (reply['type'] == 'ack'):
			# print("ack", reply)
			pass
		elif (reply['type'] == 'reject'):
			print("reject", reply)
			pass

if __name__ == "__main__":
	main()
