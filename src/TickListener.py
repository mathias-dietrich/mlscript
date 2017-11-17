from flask import Flask
import logging
from pymongo import MongoClient
from datetime import datetime
from flask import request
import time
import json 
import pika

client = MongoClient("db.pip.financial")
db = client.piptick
colBTCUSD = db.BTC_USD
colETHUSD = db.ETH_USD

print(db)
app = Flask(__name__)

# http://api.bitcoincharts.com/v1/csv/

parameters = pika.URLParameters('amqp://pip:pip@10.0.0.5')
connection = pika.BlockingConnection(parameters)
channel = connection.channel()


@app.route('/')
def index():
	symbol = request.args.get('symbol')
	period = request.args.get('period')
	bid = float(request.args.get('bid'))
	ask = float(request.args.get('ask'))
	volume = float(request.args.get('volume'))
	time = request.args.get('time')
	'''
    open = float(request.args.get('open'))
    high = float(request.args.get('high'))
    low = float(request.args.get('low'))
    close = float(request.args.get('close'))
    macd = float(request.args.get('MACD'))
    macda = float(request.args.get('MACDA'))
    macdSignal = float(request.args.get('MACDSignal'))
    cci = float(request.args.get('cci'))
    time = request.args.get('time')
    ima9 = float(request.args.get('ima9'))
    ima26 = float(request.args.get('ima26'))
    ima200 = float(request.args.get('ima200'))
   '''

	post = {
		"bid": bid,
        "ask": ask,
		"volume": volume,
		"time": time,
	}

	# send to RabbitMQ
	str = json.dumps(post)
	print(str)
	channel.basic_publish(exchange='',
                      routing_key='pip',
                      body=str)

	if symbol == 'BTCUSD':
		post_id = colBTCUSD.insert_one(post).inserted_id
	if symbol == 'ETHUSD':
		post_id = colETHUSD.insert_one(post).inserted_id
	print(post_id)
	return "OK"

if __name__ == '__main__':
    app.run(debug=True,host= '10.0.0.3',port=80)