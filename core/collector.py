# vietlott-statistical-lab/core/collector.py
import requests
import json
from core.config import GAMES

class VietlottCollector:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0'
        }

    # ==========================================
    # CÁC HÀM CỦA MEGA 6/45
    # ==========================================
    def fetch_latest_mega645(self):
        url = "https://raw.githubusercontent.com/vietvudanh/vietlott-data/main/data/power645.jsonl"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                lines = [line for line in response.text.splitlines() if line.strip()]
                if not lines: return {"status": "PARSE_ERROR", "message": "File trống"}
                
                latest_raw = lines[-1]
                latest_draw = json.loads(latest_raw)
                return {
                    "status": "SUCCESS",
                    "game": "MEGA645",
                    "draw_number_raw": f"#{str(latest_draw.get('id', '')).zfill(5)}",
                    "draw_date_raw": latest_draw.get('date', ''),
                    "numbers": latest_draw.get('result', [])
                }
            return {"status": "ERROR", "message": f"Mã lỗi: {response.status_code}"}
        except Exception as e: return {"status": "ERROR", "message": str(e)}

    def fetch_history_mega645(self, limit=100):
        url = "https://raw.githubusercontent.com/vietvudanh/vietlott-data/main/data/power645.jsonl"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                lines = [line for line in response.text.splitlines() if line.strip()]
                if limit > 0: lines = lines[-limit:]
                draws_history = []
                for line in lines:
                    draw_data = json.loads(line)
                    numbers = draw_data.get('result', [])
                    if isinstance(numbers, list) and len(numbers) == 6:
                        draws_history.append(numbers)
                return {"status": "SUCCESS", "draws": draws_history}
            return {"status": "ERROR", "message": f"Mã lỗi: {response.status_code}"}
        except Exception as e: return {"status": "ERROR", "message": str(e)}

    # ==========================================
    # CÁC HÀM CỦA MAX 3D
    # ==========================================
    def fetch_history_max3d(self, limit=500):
        url = "https://raw.githubusercontent.com/vietvudanh/vietlott-data/main/data/3d.jsonl"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                lines = [line for line in response.text.splitlines() if line.strip()]
                if limit > 0: lines = lines[-limit:]
                draws_history = []
                for line in lines:
                    draw_data = json.loads(line)
                    results = draw_data.get('result', [])
                    
                    first_prize_str = ""
                    if isinstance(results, dict) and len(results) > 0:
                        first_prize_group = list(results.values())[0]
                        if isinstance(first_prize_group, list) and len(first_prize_group) > 0:
                            first_prize_str = str(first_prize_group[0])
                    elif isinstance(results, list) and len(results) > 0:
                        first_prize_str = str(results[0])
                        
                    first_prize_str = ''.join(filter(str.isdigit, first_prize_str))
                    if len(first_prize_str) >= 3:
                        digits = [int(char) for char in first_prize_str[:3]]
                        draws_history.append(digits)
                return {"status": "SUCCESS", "draws": draws_history}
            else:
                return {"status": "ERROR", "message": f"Lỗi HTTP {response.status_code}"}
        except Exception as e: return {"status": "ERROR", "message": str(e)}

    # ==========================================
    # CÁC HÀM CỦA MAX 3D+ (PRO)
    # ==========================================
    def fetch_history_max3d_plus(self, limit=500):
        url = "https://raw.githubusercontent.com/vietvudanh/vietlott-data/main/data/3d_pro.jsonl"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                lines = [line for line in response.text.splitlines() if line.strip()]
                if limit > 0: lines = lines[-limit:]
                draws_history = []
                for line in lines:
                    draw_data = json.loads(line)
                    results = draw_data.get('result', [])
                    
                    # Giải nhất Max 3D+ có 2 số (VD: ["123", "456"])
                    first_prize_group = []
                    if isinstance(results, dict) and len(results) > 0:
                        first_prize_group = list(results.values())[0]
                    elif isinstance(results, list) and len(results) > 0:
                        first_prize_group = results[0]

                    # Gộp tất cả thành 1 chuỗi rồi lọc lấy 6 số đầu tiên (VD: "['123', '456']" -> "123456")
                    all_digits = ''.join(filter(str.isdigit, str(first_prize_group)))
                    if len(all_digits) >= 6:
                        digits = [int(char) for char in all_digits[:6]]
                        draws_history.append(digits)
                return {"status": "SUCCESS", "draws": draws_history}
            else:
                return {"status": "ERROR", "message": f"Lỗi HTTP {response.status_code}"}
        except Exception as e: return {"status": "ERROR", "message": str(e)}

# Tạo biến toàn cục
data_collector = VietlottCollector()