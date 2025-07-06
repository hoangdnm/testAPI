# 🚀 Coin API Service

> **Dịch vụ API lấy danh sách coin USDT từ sàn Bitget - Deploy trên AWS EC2**

## 📋 Mục lục
- [📡 API Endpoints](#-api-endpoints)
- [⚙️ Cài đặt và Deploy](#️-cài-đặt-và-deploy)
- [🔧 Cấu hình Production](#-cấu-hình-production)
- [🌐 Truy cập từ Internet](#-truy-cập-từ-internet)
- [🛠️ Troubleshooting](#️-troubleshooting)
- [📊 Monitoring & Optimization](#-monitoring--optimization)

---

## 📡 API Endpoints

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| `GET` | `/` | ✅ Health Check - Kiểm tra API hoạt động |
| `GET` | `/api/v1/coin` | 📈 Lấy danh sách tất cả cặp USDT |
| `POST` | `/api/v1/coin/refresh` | 🔄 Refresh danh sách từ Bitget |

### 🧪 Test API:
```bash
# Health check
curl http://52.221.179.117:5000/

# Lấy danh sách coin
curl http://52.221.179.117:5000/api/v1/coin

# Refresh data
curl -X POST http://52.221.179.117:5000/api/v1/coin/refresh
```

---

## ⚙️ Cài đặt và Deploy

### 📦 1. Chuẩn bị VPS
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Cài đặt Python 3.8+
sudo apt install python3 python3-pip python3-venv -y

# Cài đặt git (nếu cần)
sudo apt install git -y
```

### 📁 2. Upload code lên VPS
```bash
# Cách 1: SCP từ máy local
scp -r . ubuntu@52.221.179.117:/home/ubuntu/testAPI

# Cách 2: Git clone
git clone <your-repo-url> /home/ubuntu/testAPI
```

### 🔧 3. Cài đặt dependencies
```bash
cd /home/ubuntu/testAPI
pip3 install -r requirements.txt
```

### 🚀 4. Chạy API (chọn 1 cách)

#### Cách 1: Script tự động (Khuyên dùng)
```bash
chmod +x start.sh
./start.sh
```

#### Cách 2: Gunicorn manual
```bash
gunicorn -c gunicorn.conf.py name_coin:name_coin
```

#### Cách 3: Python development
```bash
python3 name_coin.py
```

---

## 🔧 Cấu hình Production

### 🔄 1. Systemd Service (Chạy 24/7)

#### Tạo service file:
```bash
sudo nano /etc/systemd/system/coin-api.service
```

#### Nội dung file:
```ini
[Unit]
Description=🪙 Coin API Service
After=network.target

[Service]
Type=simple
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/testAPI
Environment="PATH=/usr/local/bin:/usr/bin:/bin"
ExecStart=/usr/local/bin/gunicorn -c gunicorn.conf.py name_coin:name_coin
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

#### Kích hoạt service:
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable auto-start
sudo systemctl enable coin-api

# Start service
sudo systemctl start coin-api

# Check status
sudo systemctl status coin-api
```

### 📋 2. Quản lý Service

| Lệnh | Mô tả |
|------|-------|
| `sudo systemctl start coin-api` | ▶️ Khởi động API |
| `sudo systemctl stop coin-api` | ⏹️ Dừng API |
| `sudo systemctl restart coin-api` | 🔄 Khởi động lại API |
| `sudo systemctl status coin-api` | 📊 Xem trạng thái |
| `journalctl -u coin-api -f` | 📝 Xem logs realtime |
| `journalctl -u coin-api -n 50` | 📄 Xem 50 logs gần nhất |

### ✅ 3. Lợi ích Systemd
- 🔄 **Auto-restart** khi VPS reboot
- 🛡️ **Auto-recovery** khi API crash
- 📝 **Centralized logging** với journalctl
- ⚡ **Background process** không bị ngắt

---

## 🌐 Truy cập từ Internet

> ✅ **API có thể truy cập từ bất kỳ đâu!** Đã cấu hình bind `0.0.0.0:5000`

### 🔑 1. Cấu hình AWS Security Group

#### 📍 **QUAN TRỌNG**: Mở port 5000 trong AWS Console

1. 🌐 **Đăng nhập AWS Console**: https://console.aws.amazon.com
2. 🖥️ **Vào Services** → **EC2** → **Instances**
3. 🔍 **Tìm instance** có IP `52.221.179.117`
4. 🖱️ **Click instance** → tab **Security** (phần dưới)
5. 🔒 **Click tên Security Group** (sg-xxxxxxxxx)
6. ➕ **"Edit inbound rules"** → **"Add rule"**
7. 📝 **Điền thông tin:**
   ```
   Type: Custom TCP
   Port range: 5000
   Source: 0.0.0.0/0
   Description: Coin API Service
   ```
8. 💾 **Click "Save rules"**

### ⚠️ 2. Port Range Guidelines

| Port Setting | Mô tả | Status |
|--------------|-------|--------|
| `5000` | Chỉ mở port 5000 | ✅ **KHUYÊN DÙNG** |
| `0-5000` | Mở port 1-5000 | ⚠️ **CÓ THỂ DÙNG** (không an toàn) |
| `5000-5010` | Mở dải port 5000-5010 | ✅ **OK** (nếu cần nhiều port) |
| `0-65535` | Mở tất cả port | ❌ **CỰC KỲ NGUY HIỂM** |
| `0` | Port không hợp lệ | ❌ **KHÔNG HOẠT ĐỘNG** |

### 🔧 3. VPS Firewall (UFW)

```bash
# Kiểm tra UFW status
sudo ufw status

# Mở port 5000 (nếu UFW active)
sudo ufw allow 5000
sudo ufw reload

# Disable UFW (nếu chỉ dùng Security Group)
sudo ufw disable
```

---

## 🛠️ Troubleshooting

### 🔍 1. Kiểm tra API Status

```bash
# ✅ Kiểm tra service status
sudo systemctl status coin-api

# 📊 Kiểm tra process
ps aux | grep gunicorn

# 🔌 Kiểm tra port đang lắng nghe
ss -tlnp | grep :5000
# Kết quả mong đợi: LISTEN 0 2048 0.0.0.0:5000

# 🧪 Test từ VPS
curl http://localhost:5000/
curl http://127.0.0.1:5000/api/v1/coin
```

### 🌐 2. Test từ máy khác

```bash
# 🏠 Health check
curl http://52.221.179.117:5000/

# 📈 API endpoint
curl http://52.221.179.117:5000/api/v1/coin

# 🔄 Refresh data
curl -X POST http://52.221.179.117:5000/api/v1/coin/refresh

# 🌍 Test từ browser
# http://52.221.179.117:5000/api/v1/coin
```

### 🔧 3. Fix Common Issues

#### 🚫 Nếu API không start:
```bash
# Xem logs chi tiết
journalctl -u coin-api -n 50

# Restart service
sudo systemctl restart coin-api

# Manual restart
pkill -f gunicorn
cd /home/ubuntu/testAPI
gunicorn -c gunicorn.conf.py name_coin:name_coin
```

#### 🌐 Nếu không truy cập được từ internet:
1. ✅ **Kiểm tra localhost OK**: `curl http://localhost:5000/`
2. 🔒 **Kiểm tra Security Group** đã mở port 5000
3. 🛡️ **Kiểm tra UFW**: `sudo ufw status`
4. 🔌 **Kiểm tra port**: `ss -tlnp | grep :5000`

#### 📄 Update code và deploy:
```bash
cd /home/ubuntu/testAPI
# Upload code mới hoặc git pull
sudo systemctl restart coin-api
sudo systemctl status coin-api
```

---

## 📊 Monitoring & Optimization

### 💾 1. Resource Usage (Chạy 24/7)

#### 📈 Tài nguyên tiêu thụ:
- **RAM**: ~30-70MB (chiếm ~5-7% VPS 1GB)
- **CPU**: ~1-3% khi idle, ~5-15% khi có request
- **Network**: ~7-10MB/ngày (nếu refresh mỗi phút)

#### 🔍 Monitoring commands:
```bash
# 📊 Kiểm tra RAM/CPU usage
ps aux | grep gunicorn | grep -v grep
top -p $(pgrep -f gunicorn)

# 📋 Memory chi tiết
sudo systemctl status coin-api
journalctl -u coin-api --since "1 hour ago" | grep -i memory

# 🖥️ Monitor tổng thể VPS
htop
free -h
df -h
```

### ⚙️ 2. Gunicorn Optimization

#### 📝 File: `gunicorn.conf.py`
```python
# Cấu hình tối ưu tài nguyên
bind = "0.0.0.0:5000"
workers = 1                    # 1 worker cho API đơn giản
worker_class = "sync"
worker_connections = 100       # Giảm connection pool
max_requests = 1000           # Restart sau 1000 request
max_requests_jitter = 50
preload_app = True            # Tiết kiệm RAM
timeout = 30
keepalive = 2

# Logging tối ưu
accesslog = "-"
errorlog = "-"
loglevel = "warning"          # Chỉ log warning/error
```

### 🔄 3. Auto-Restart & Maintenance

#### ⏰ Cron job restart định kỳ:
```bash
# Edit crontab
sudo crontab -e

# Restart mỗi tuần (CN 3h sáng)
0 3 * * 0 /bin/systemctl restart coin-api

# Hoặc restart hàng ngày (3h sáng)
0 3 * * * /bin/systemctl restart coin-api
```

#### 🎛️ Resource limits với systemd:
```bash
# Edit service file
sudo nano /etc/systemd/system/coin-api.service

# Thêm vào [Service]:
[Service]
# ...existing config...
MemoryLimit=100M        # Giới hạn RAM 100MB
CPUQuota=50%           # Giới hạn CPU 50%
TasksMax=10            # Giới hạn processes

# Apply changes
sudo systemctl daemon-reload
sudo systemctl restart coin-api
```

### 📝 4. Log Management

#### 🔄 Log rotation setup:
```bash
# Tạo logrotate config
sudo nano /etc/logrotate.d/coin-api

# Nội dung:
/var/log/coin-api.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 644 ubuntu ubuntu
    postrotate
        systemctl reload coin-api
    endscript
}
```

### 🚀 5. Performance Optimization

#### 💾 Cache implementation:
```python
# Thêm vào code Python để cache API calls
import time
from functools import lru_cache

# Cache trong 5 phút
@lru_cache(maxsize=1)
def get_cached_symbols():
    return get_symbols_from_bitget()

# Hoặc simple cache
cache_data = None
cache_time = 0
CACHE_DURATION = 300  # 5 phút

def get_symbols_cached():
    global cache_data, cache_time
    now = time.time()
    
    if cache_data is None or (now - cache_time) > CACHE_DURATION:
        cache_data = get_symbols_from_bitget()
        cache_time = now
    
    return cache_data
```

### 📋 6. Daily Monitoring Script

```bash
#!/bin/bash
# File: /home/ubuntu/monitor_api.sh

echo "=== 📊 API Resource Report $(date) ==="
echo "🔧 Service Status:"
sudo systemctl is-active coin-api

echo "💾 Memory Usage:"
ps aux | grep gunicorn | grep -v grep | awk '{print $4"% RAM, "$6"KB"}'

echo "⚡ CPU Usage:"
top -bn1 | grep gunicorn | awk '{print $9"% CPU"}'

echo "💽 Disk Usage:"
df -h | grep -E "(/$|/var)" | awk '{print $5" used on "$6}'

echo "🌐 Network:"
ss -tuln | grep :5000 | wc -l | awk '{print $1" connections"}'

echo "✅ API Test:"
curl -s http://localhost:5000/ > /dev/null && echo "API OK" || echo "API ERROR"
```

### 🔧 7. Nginx Reverse Proxy (Tùy chọn)

```nginx
# File: /etc/nginx/sites-available/coin-api
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable Nginx config
sudo ln -s /etc/nginx/sites-available/coin-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🎯 Quick Commands Summary

| Task | Command |
|------|---------|
| 🚀 **Start API** | `sudo systemctl start coin-api` |
| ⏹️ **Stop API** | `sudo systemctl stop coin-api` |
| 🔄 **Restart API** | `sudo systemctl restart coin-api` |
| 📊 **Check Status** | `sudo systemctl status coin-api` |
| 📝 **View Logs** | `journalctl -u coin-api -f` |
| 🧪 **Test Local** | `curl http://localhost:5000/` |
| 🌐 **Test Remote** | `curl http://52.221.179.117:5000/` |
| 📈 **Check Resources** | `ps aux \| grep gunicorn` |

---

> 🎉 **Setup Complete!** API đã sẵn sàng phục vụ 24/7 với monitoring và auto-recovery!
