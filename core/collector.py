# vietlott-statistical-lab/core/collector.py
import requests
import json
from core.config import GAMES

class VietlottCollector:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0'
        }

    def fetch_latest_mega645(self):
        """Thu thập kết quả kỳ quay mới nhất (1 kỳ)"""
        url = "https://raw.githubusercontent.com/vietvudanh/vietlott-data/main/data/power645.jsonl"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                lines = [line for line in response.text.splitlines() if line.strip()]
                latest_raw = lines[-1]
                latest_draw = json.loads(latest_raw)
                
                return {
                    "status": "SUCCESS",
                    "draw_number_raw": f"#{str(latest_draw.get('id', '')).zfill(5)}",
                    "draw_date_raw": latest_draw.get('date', ''),
                    "numbers": latest_draw.get('result', [])
                }
            return {"status": "ERROR"}
        except Exception as e:
             return {"status": "ERROR", "message": str(e)}

    def fetch_history_mega645(self, limit=100):
        """Thu thập lịch sử nhiều kỳ quay để phân tích thống kê"""
        url = "https://raw.githubusercontent.com/vietvudanh/vietlott-data/main/data/power645.jsonl"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                lines = [line for line in response.text.splitlines() if line.strip()]
                
                # Cắt lấy số lượng kỳ quay (limit) từ dưới lên (gần nhất)
                if limit > 0:
                    lines = lines[-limit:]
                
                draws_history = []
                for line in lines:
                    draw_data = json.loads(line)
                    numbers = draw_data.get('result', [])
                    # Đảm bảo mảng có 6 con số mới lấy
                    if isinstance(numbers, list) and len(numbers) == 6:
                        draws_history.append(numbers)
                        
                return {
                    "status": "SUCCESS",
                    "draws": draws_history
                }
            else:
                return {"status": "ERROR", "message": "Không thể tải dữ liệu"}
        except Exception as e:
             return {"status": "ERROR", "message": str(e)}

# Tạo biến toàn cục
data_collector = VietlottCollector()