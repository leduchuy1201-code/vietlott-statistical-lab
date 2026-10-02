# Nhúng bộ thu thập dữ liệu
from core.collector import data_collector

print("1. Đang gọi Vietlott Collector...")
print("2. Đang kết nối tới vietlott.vn để lấy kết quả Mega 6/45 mới nhất...")

# Yêu cầu lấy dữ liệu
result = data_collector.fetch_latest_mega645()

if result["status"] == "SUCCESS":
    print("\n--- KẾT QUẢ THU THẬP THÀNH CÔNG ---")
    print(f"Loại vé: {result['game']}")
    print(f"Kỳ quay: {result['draw_number_raw']}")
    print(f"Ngày quay: {result['draw_date_raw']}")
    print(f"Các số trúng thưởng: {result['numbers']}")
else:
    print(f"\n--- LỖI THU THẬP ---")
    print(f"Trạng thái: {result['status']}")
    print(f"Lý do: {result.get('message')}")

print("\nHoàn tất Bước 13!")