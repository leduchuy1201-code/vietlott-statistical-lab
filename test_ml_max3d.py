from core.collector import data_collector
from core.ml_engine import ml_engine

print("1. Đang tải 500 kỳ quay Max 3D gần nhất...")
result = data_collector.fetch_history_max3d(limit=500)

if result["status"] == "SUCCESS":
    draws = result["draws"]
    print(f"\n2. BẮT ĐẦU HUẤN LUYỆN 3 MÔ HÌNH AI (Dữ liệu: {len(draws)} kỳ)")
    
    # Đưa vào "Trái tim AI"
    predictions = ml_engine.predict_max3d(draws)
    
    print("\n=============================================")
    print(" 🤖 AI GỢI Ý CHO KỲ QUAY TIẾP THEO (MAX 3D)")
    print("=============================================")
    
    position_names = ["HÀNG TRĂM", "HÀNG CHỤC", "HÀNG ĐƠN VỊ"]
    best_number = ""
    
    for i in range(3):
        print(f"\n📍 {position_names[i]}:")
        # Lấy top 3 chữ số có xác suất cao nhất cho vị trí này
        top_3 = predictions[i][:3]
        
        # Ghép chữ số top 1 vào con số chung cuộc
        best_number += str(top_3[0][0])
        
        for digit, prob in top_3:
            print(f"  + Số {digit} : {prob * 100:.2f}%")
            
    print("\n🏆 CHUỖI 3 CHỮ SỐ ĐƯỢC AI ĐÁNH GIÁ CAO NHẤT (SIÊU CẤP):")
    print(f"👉 [ {best_number} ] 👈")
    
else:
    print("Lỗi tải dữ liệu!")