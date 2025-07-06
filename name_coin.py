import websocket
import json
import datetime
import threading
import time
import pandas as pd
import requests
from flask import Flask, jsonify, request

name_coin = Flask(__name__)

# Khởi tạo biến global
usdt_pairs = []

url = "https://api.bitget.com/api/v2/spot/public/symbols"

try:
    response = requests.get(url, timeout=10)
    data = response.json()

    if response.status_code == 200 and data.get('code') == '00000':
        usdt_pairs = [item['symbol'] for item in data['data']
                      if item['status'] == 'online' and item['symbol'].endswith('USDT')]
        print(usdt_pairs)
    else:
        print(" API trả về lỗi:", data.get('msg', 'Không rõ lỗi'))

except Exception as e:
    print(" Lỗi khi gọi API:", e)

@name_coin.route('/api/v1/coin', methods=['GET'])
def name_coin_list():
    return jsonify({
        'success': True,
        'data': usdt_pairs,
        'count': len(usdt_pairs),
        'message': 'Danh sách các cặp USDT'
    })

if __name__ == '__main__':
   name_coin.run(port=5000, debug=True, host='0.0.0.0')