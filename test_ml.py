# test_ml.py
from core.collector import data_collector
from core.ml_engine import ml_engine

print("1. Đang tải 100 kỳ quay Mega 6/45 gần nhất...")
result = data_collector.fetch_history_mega645(limit=100)

if result["status"] == "SUCCESS":
    draws = result["draws"]
    print("\n2. BẮT ĐẦU QUY TRÌNH HỌC MÁY (MACHINE LEARNING)")
    
    # Đưa vào AI
    prediction = ml_engine.predict_next_draw(draws, pool_size=45)
    
    print("\n=============================================")
    print(" 🤖 AI GỢI Ý CHO KỲ QUAY TIẾP THEO (MEGA 6/45)")
    print("=============================================")
    print(f"👉 Dãy số tiềm năng nhất: {sorted(prediction['top_6_picks'])}")
    
    print("\n📊 BẢNG XÁC SUẤT CHI TIẾT (TOP 10):")
    for num, prob in prediction['details']:
        # Format xác suất thành %
        print(f"  + Số {num:02d} : {prob * 100:.2f}% cơ hội xuất hiện")
        
    print("\n⚠️️ Lưu ý: Kết quả do AI học từ dữ liệu lịch sử và chỉ mang tính chất tham khảo thực hành thuật toán.")
else:
    print("Lỗi tải dữ liệu!")