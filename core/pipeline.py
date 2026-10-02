# vietlott-statistical-lab/core/pipeline.py
import requests
import json
from core.database import db_manager

class DataPipeline:
    def __init__(self):
        # Kết nối vào một thư mục mới tên là 'mega645_history' trong Firestore
        self.collection = db_manager.get_collection('mega645_history')

    def run_etl_mega645(self, limit=100):
        """Chạy quy trình ETL: Extract - Transform - Load"""
        print(f"-> [EXTRACT] Đang cào {limit} dòng dữ liệu từ GitHub...")
        url = "https://raw.githubusercontent.com/vietvudanh/vietlott-data/main/data/power645.jsonl"
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                return {"status": "ERROR", "message": "Không thể tải dữ liệu"}
            
            # Cắt lấy số lượng dòng theo limit từ dưới lên
            lines = [line for line in response.text.splitlines() if line.strip()][-limit:]
            
            print(f"-> [TRANSFORM] Đang làm sạch và định dạng {len(lines)} kỳ quay...")
            batch_data = []
            for line in lines:
                raw_data = json.loads(line)
                
                # Biến đổi id thành chuỗi 5 số (VD: '01568')
                draw_id = str(raw_data.get('id', '')).zfill(5) 
                numbers = raw_data.get('result', [])
                draw_date = raw_data.get('date', '')
                
                # Chỉ lấy những mảng có đủ 6 số
                if len(numbers) == 6:
                    batch_data.append({
                        "id": draw_id,
                        "date": draw_date,
                        "numbers": numbers
                    })
            
            print(f"-> [LOAD] Đang tải {len(batch_data)} bản ghi vào Firestore. Vui lòng đợi...")
            
            # Lưu từng bản ghi vào database
            for item in batch_data:
                # Dùng id (số kỳ quay) làm tên tài liệu (Document ID) để tránh trùng lặp
                doc_ref = self.collection.document(item['id'])
                doc_ref.set({
                    "date": item['date'],
                    "numbers": item['numbers']
                })
                
            return {"status": "SUCCESS", "count": len(batch_data)}
            
        except Exception as e:
            return {"status": "ERROR", "message": str(e)}

# Khởi tạo biến toàn cục để sử dụng
etl_pipeline = DataPipeline()