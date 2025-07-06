import websocket
import json
import datetime
import threading
import time
import pandas as pd
import requests
from flask import Flask, jsonify, request
import os
import logging

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

name_coin = Flask(__name__)

# Khởi tạo biến global
usdt_pairs = []

def fetch_usdt_pairs():
    """Hàm lấy danh sách các cặp USDT từ Bitget API"""
    global usdt_pairs
    url = "https://api.bitget.com/api/v2/spot/public/symbols"
    
    try:
        logger.info("Đang lấy danh sách cặp USDT từ Bitget...")
        response = requests.get(url, timeout=10)
        data = response.json()

        if response.status_code == 200 and data.get('code') == '00000':
            usdt_pairs = [item['symbol'] for item in data['data']
                          if item['status'] == 'online' and item['symbol'].endswith('USDT')]
            logger.info(f"Đã lấy được {len(usdt_pairs)} cặp USDT")
            return True
        else:
            logger.error(f"API trả về lỗi: {data.get('msg', 'Không rõ lỗi')}")
            return False

    except requests.exceptions.RequestException as e:
        logger.error(f"Lỗi kết nối API: {e}")
        return False
    except Exception as e:
        logger.error(f"Lỗi không xác định: {e}")
        return False

# Khởi tạo dữ liệu khi start app
if not fetch_usdt_pairs():
    logger.warning("Không thể lấy dữ liệu ban đầu, app vẫn sẽ chạy")

@name_coin.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'OK',
        'message': 'API đang hoạt động',
        'timestamp': datetime.datetime.now().isoformat()
    })

@name_coin.route('/api/v1/coin', methods=['GET'])
def name_coin_list():
    """API endpoint trả về danh sách các cặp USDT"""
    try:
        # Nếu danh sách trống, thử lấy lại
        if not usdt_pairs:
            logger.info("Danh sách trống, đang thử lấy lại...")
            fetch_usdt_pairs()
        
        return jsonify({
            'success': True,
            'data': usdt_pairs,
            'count': len(usdt_pairs),
            'message': 'Danh sách các cặp USDT',
            'timestamp': datetime.datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Lỗi khi xử lý request: {e}")
        return jsonify({
            'success': False,
            'data': [],
            'count': 0,
            'message': 'Có lỗi xảy ra khi lấy dữ liệu',
            'error': str(e)
        }), 500

@name_coin.route('/api/v1/coin/refresh', methods=['POST'])
def refresh_coin_list():
    """API endpoint để refresh danh sách coin"""
    try:
        success = fetch_usdt_pairs()
        if success:
            return jsonify({
                'success': True,
                'message': 'Đã refresh thành công',
                'count': len(usdt_pairs),
                'timestamp': datetime.datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Không thể refresh dữ liệu'
            }), 500
    except Exception as e:
        logger.error(f"Lỗi khi refresh: {e}")
        return jsonify({
            'success': False,
            'message': 'Có lỗi xảy ra khi refresh',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Cấu hình cho development
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting server on {host}:{port}")
    name_coin.run(port=port, debug=debug, host=host)