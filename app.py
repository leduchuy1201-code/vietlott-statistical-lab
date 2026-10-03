# vietlott-statistical-lab/app.py
from flask import Flask, jsonify, render_template
from core.database import db_manager
from core.statistics import stat_engine
from core.ml_engine import ml_engine
from core.collector import data_collector # <-- Đã thêm Data Collector

# Khởi tạo ứng dụng Web Flask
app = Flask(__name__)

# Tạo đường dẫn trang chủ
@app.route('/', methods=['GET'])
def home():
    # Thay vì trả JSON, máy chủ sẽ đọc file index.html và gửi cho trình duyệt
    return render_template('index.html')

# ==========================================
# API DÀNH CHO MEGA 6/45
# ==========================================
@app.route('/api/v1/stats/mega645', methods=['GET'])
def get_mega645_stats():
    print("Đang truy xuất dữ liệu từ Firestore...")
    
    # 1. Lấy dữ liệu từ database thay vì tải từ internet
    collection = db_manager.get_collection('mega645_history')
    docs = collection.stream()
    
    all_draws = []
    for doc in docs:
        data = doc.to_dict()
        all_draws.append({
            "id": doc.id,
            "numbers": data.get('numbers', [])
        })
        
    # Nếu không có dữ liệu
    if len(all_draws) == 0:
        return jsonify({"error": "Chưa có dữ liệu trong Database. Hãy chạy pipeline trước!"}), 404
        
    # 2. Sắp xếp lại kỳ quay từ Cũ đến Mới (dựa vào id)
    all_draws_sorted = sorted(all_draws, key=lambda x: x['id'])
    
    # 3. Lấy 100 kỳ gần nhất và chỉ trích xuất mảng các con số
    recent_draws = all_draws_sorted[-100:]
    draws_only = [item['numbers'] for item in recent_draws]
    
    # 4. Đưa vào bộ máy thống kê
    freq = stat_engine.calculate_frequency(draws_only, pool_size=45)
    gaps = stat_engine.calculate_gap(draws_only, pool_size=45)

    # 5. Sắp xếp kết quả (Lấy Top 5 cao nhất)
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:5]
    sorted_gaps = sorted(gaps.items(), key=lambda x: x[1], reverse=True)[:5]

    # 6. Đưa dữ liệu vào AI để dự đoán
    ai_prediction = ml_engine.predict_next_draw(draws_only, pool_size=45)

    # 7. Định dạng kết quả trả về cho trình duyệt (JSON)
    return jsonify({
        "game": "MEGA 6/45",
        "analyzed_draws": len(draws_only),
        "hot_numbers": [{"number": f"{k:02d}", "frequency": v} for k, v in sorted_freq],
        "cold_numbers": [{"number": f"{k:02d}", "gap_days": v} for k, v in sorted_gaps],
        "ai_prediction": ai_prediction 
    })

# ==========================================
# API MỚI DÀNH CHO MAX 3D
# ==========================================
@app.route('/api/v1/stats/max3d', methods=['GET'])
def get_max3d_stats():
    print("Đang truy xuất dữ liệu Max 3D từ GitHub...")
    result = data_collector.fetch_history_max3d(limit=500)
    
    if result["status"] != "SUCCESS":
        return jsonify({"error": "Không thể tải dữ liệu Max 3D"}), 500
        
    draws = result["draws"]
    
    # Đưa vào AI dự đoán
    predictions = ml_engine.predict_max3d(draws)
    
    # Ghép con số Siêu Cấp
    best_number = ""
    for i in range(3):
        best_number += str(predictions[i][0][0])
        
    # Trả về kết quả JSON
    return jsonify({
        "game": "MAX 3D",
        "analyzed_draws": len(draws),
        "ai_prediction": {
            "best_number": best_number,
            "details": {
                "tram": [{"digit": d, "prob": p} for d, p in predictions[0][:3]],
                "chuc": [{"digit": d, "prob": p} for d, p in predictions[1][:3]],
                "don_vi": [{"digit": d, "prob": p} for d, p in predictions[2][:3]]
            }
        }
    })

# Khởi động Web Server ở cổng 8080
if __name__ == '__main__':
    print("🚀 Máy chủ Web đang khởi động ở cổng 8080...")
    app.run(host='0.0.0.0', port=8080, debug=True)