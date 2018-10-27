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

	print("The exchange replied:", hello_from_exchange, file=sys.stderr)
	print(type(hello_from_exchange))
	print(hello_from_exchange.keys())
	positions = hello_from_exchange["symbols"]

	bond_obj = bond.Bond()
	# bond_obj.hello()
	trades = bond_obj.trade(order_obj, all_trades)
	for trade in trades:
		all_trades[trade['order_id']] = trade
		write_to_exchange(exchange, trade)

	while (1):
		reply = read_from_exchange(exchange)
		if (reply['type'] == 'fill'):
			if (reply['dir'] == 'buy'):
				positions[reply['symbol']] += reply['size']
				cash -= reply['size'] * reply['price']
				all_trades[reply['order_id']] -= reply['size']
				if (all_trades[reply['order_id']] == 0):
					all_trades.pop(reply['order_id'])

			elif (reply['dir'] == 'sell'):
				positions[reply['symbol']] -= reply['size']
				cash += reply['size'] * reply['price']
				all_trades[reply['order_id']] -= reply['size']
				if (all_trades[reply['order_id']] == 0):
					all_trades.pop(reply['order_id'])
			print("log, fill-reply received: ", reply)

		print(reply)
		if (reply['type'] == 'out'):
			trades = bond_obj.trade()
			for trade in trades:
				all_trades[trade['order_id']] = trade
				write_to_exchange(exchange, trade)

if __name__ == "__main__":
	main()
