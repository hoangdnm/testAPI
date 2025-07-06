#!/bin/bash
# Script để start ứng dụng trên VPS
echo "Starting Flask API..."
# Kiểm tra Python version
python3 --version
# Cài đặt dependencies
pip3 install -r requirements.txt
# Start ứng dụng với gunicorn (production server)
gunicorn --bind 0.0.0.0:5000 --workers 2 --timeout 120 name_coin:name_coin
# Hoặc chạy trực tiếp với Python (development)
# python3 name_coin.py
