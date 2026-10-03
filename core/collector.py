# vietlott-statistical-lab/core/collector.py
import requests
import json
from core.config import GAMES

class VietlottCollector:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def fetch_latest_mega645(self):
        """Thu thập kết quả kỳ quay mới nhất của Mega 6/45 qua GitHub JSONL"""
        url = "https://raw.githubusercontent.com/vietvudanh/vietlott-data/main/data/power645.jsonl"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                lines = [line for line in response.text.splitlines() if line.strip()]
                if not lines:
                     return {"status": "PARSE_ERROR", "message": "File dữ liệu trống"}
                latest_raw = lines[-1]
                latest_draw = json.loads(latest_raw)
                draw_number = f"#{str(latest_draw.get('id', '')).zfill(5)}"
                draw_date = latest_draw.get('date', '')
                numbers = latest_draw.get('result', [])
                return {
                    "status": "SUCCESS",
                    "game": "MEGA645",
                    "draw_number_raw": draw_number,
                    "draw_date_raw": draw_date,
                    "numbers": numbers,
                    "source_url": url
                }
            else:
                return {"status": "SOURCE_UNAVAILABLE", "message": f"Mã lỗi: {response.status_code}"}
        except Exception as e:
             return {"status": "ERROR", "message": str(e)}

    def fetch_history_mega645(self, limit=100):
        """Thu thập lịch sử nhiều kỳ quay để phân tích thống kê (Mega/Power)"""
        url = "https://raw.githubusercontent.com/vietvudanh/vietlott-data/main/data/power645.jsonl"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                lines = [line for line in response.text.splitlines() if line.strip()]
                if limit > 0:
                    lines = lines[-limit:]
                draws_history = []
                for line in lines:
                    draw_data = json.loads(line)
                    numbers = draw_data.get('result', [])
                    if isinstance(numbers, list) and len(numbers) == 6:
                        draws_history.append(numbers)
                return {"status": "SUCCESS", "draws": draws_history}
            else:
                return {"status": "ERROR", "message": "Không thể tải dữ liệu"}
        except Exception as e:
             return {"status": "ERROR", "message": str(e)}

    def fetch_history_max3d(self, limit=500):
        """Thu thập lịch sử Max 3D (Giải Nhất gồm 3 chữ số)"""
        # Đã cập nhật tên file chính xác từ GitHub: 3d.jsonl
        url = "https://raw.githubusercontent.com/vietvudanh/vietlott-data/main/data/3d.jsonl"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                lines = [line for line in response.text.splitlines() if line.strip()]
                if limit > 0:
                    lines = lines[-limit:]
                
                draws_history = []
                for line in lines:
                    draw_data = json.loads(line)
                    results = draw_data.get('result', [])
                    
                    # Cấu trúc của Max 3D là Từ điển (Dictionary) phân theo giải, không phải List.
                    first_prize_str = ""
                    if isinstance(results, dict) and len(results) > 0:
                        first_prize_group = list(results.values())[0] # Lấy danh sách số của giải đầu tiên
                        if isinstance(first_prize_group, list) and len(first_prize_group) > 0:
                            first_prize_str = str(first_prize_group[0])
                    elif isinstance(results, list) and len(results) > 0:
                        first_prize_str = str(results[0])
                        
                    # Lọc bỏ các ký tự thừa (nếu có), chỉ lấy số
                    first_prize_str = ''.join(filter(str.isdigit, first_prize_str))
                    
                    if len(first_prize_str) >= 3:
                        # Cắt đúng 3 chữ số đầu và tách thành mảng [Trăm, Chục, Đơn vị] (VD: "195" -> [1, 9, 5])
                        numbers = [int(char) for char in first_prize_str[:3]]
                        draws_history.append(numbers)
                            
                return {
                    "status": "SUCCESS",
                    "draws": draws_history
                }
            else:
                return {"status": "ERROR", "message": f"Lỗi HTTP {response.status_code}. Sai URL!"}
        except Exception as e:
             return {"status": "ERROR", "message": str(e)}

# Tạo biến toàn cục
data_collector = VietlottCollector()