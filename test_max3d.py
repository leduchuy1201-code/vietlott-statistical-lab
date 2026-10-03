from core.collector import data_collector

print("1. Đang truy cập kho dữ liệu GitHub để tìm Max 3D...")
print("2. Đang cào 500 kỳ quay gần nhất và tách mảng (Trăm, Chục, Đơn vị)...")

# Yêu cầu lấy 500 kỳ
result = data_collector.fetch_history_max3d(limit=500)

if result["status"] == "SUCCESS":
    draws = result["draws"]
    print(f"\n✅ THÀNH CÔNG! Đã tải và trích xuất thành công {len(draws)} kỳ quay.")
    print("\n📊 5 KỲ QUAY GẦN NHẤT ĐỂ KIỂM TRA (Từ cũ đến mới):")
    
    # In ra 5 kỳ quay cuối cùng để kiểm chứng
    for i, draw in enumerate(draws[-5:]):
        print(f"  + Kỳ quay {i+1}: Chuỗi giải Nhất được tách thành -> Hàng Trăm: {draw[0]}, Hàng Chục: {draw[1]}, Hàng Đơn vị: {draw[2]}")
        
    print("\n👉 BƯỚC TIẾP THEO: Sửa đổi AI để nhận diện 3 cột riêng biệt!")
else:
    print(f"\n❌ LỖI: {result.get('message')}")
    print("Mã nguồn mở có thể đã thay đổi tên file. Cần kiểm tra lại URL.")