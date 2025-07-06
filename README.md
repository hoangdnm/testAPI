# API Documentation

## Coin API Service

Dịch vụ API để lấy danh sách các cặp coin USDT từ sàn Bitget.

### Endpoints

#### 1. Health Check
```
GET /
```
Kiểm tra trạng thái API

#### 2. Lấy danh sách coin
```
GET /api/v1/coin
```
Trả về danh sách tất cả các cặp USDT

#### 3. Refresh danh sách
```
POST /api/v1/coin/refresh
```
Cập nhật lại danh sách coin từ API Bitget

### Cách chạy trên VPS

1. **Cài đặt Python 3.8+**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

2. **Upload code lên VPS**
```bash
scp -r . user@your-vps-ip:/path/to/your/app
```

3. **Cài đặt dependencies**
```bash
cd /path/to/your/app
pip3 install -r requirements.txt
```

4. **Chạy với Gunicorn (Production)**
```bash
chmod +x start.sh
./start.sh
```

Hoặc:
```bash
gunicorn -c gunicorn.conf.py name_coin:name_coin
```

5. **Chạy background với systemd**
Tạo file `/etc/systemd/system/coin-api.service`:
```ini
[Unit]
Description=Coin API Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/app
Environment="PATH=/path/to/your/app/venv/bin"
ExecStart=/usr/local/bin/gunicorn -c gunicorn.conf.py name_coin:name_coin
Restart=always

[Install]
WantedBy=multi-user.target
```

Sau đó:
```bash
sudo systemctl daemon-reload
sudo systemctl enable coin-api
sudo systemctl start coin-api
```

### Truy cập từ máy khác

**Có thể truy cập từ máy khác!** API đã được cấu hình bind `0.0.0.0:5000` nên có thể truy cập từ bất kỳ IP nào.

#### Cách truy cập:
```bash
# Thay YOUR_VPS_IP bằng IP thực của VPS
curl http://YOUR_VPS_IP:5000/
curl http://YOUR_VPS_IP:5000/api/v1/coin
```

#### Lưu ý quan trọng:
1. **Mở port 5000 trên VPS:**
```bash
# Ubuntu/Debian
sudo ufw allow 5000
sudo ufw reload

# CentOS/RHEL
sudo firewall-cmd --permanent --add-port=5000/tcp
sudo firewall-cmd --reload
```

2. **Kiểm tra security group (nếu dùng cloud VPS):**
   - AWS: Mở port 5000 trong Security Group
   - Google Cloud: Mở port trong Firewall Rules
   - Azure: Mở port trong Network Security Group

3. **Sử dụng reverse proxy (khuyên dùng):**
   - Nginx hoặc Apache để proxy từ port 80/443 → 5000
   - Có thể thêm SSL certificate

### Kiểm tra

```bash
# Kiểm tra từ localhost
curl http://localhost:5000/

# Kiểm tra từ máy khác (thay YOUR_VPS_IP)
curl http://YOUR_VPS_IP:5000/

# Lấy danh sách coin
curl http://YOUR_VPS_IP:5000/api/v1/coin

# Test từ browser
# http://YOUR_VPS_IP:5000/api/v1/coin
```

### Cấu hình Nginx (tùy chọn)
Tạo file `/etc/nginx/sites-available/coin-api`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Enable và restart:
```bash
sudo ln -s /etc/nginx/sites-available/coin-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```
