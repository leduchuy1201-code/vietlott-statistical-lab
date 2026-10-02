from core.collector import data_collector
from core.statistics import stat_engine

print("1. Đang tải lịch sử 100 kỳ quay MEGA 6/45 gần nhất từ Internet...")
history_result = data_collector.fetch_history_mega645(limit=100)

if history_result["status"] == "SUCCESS":
    draws = history_result["draws"]
    print(f"-> Tải thành công {len(draws)} kỳ quay!")
    
    print("\n2. Đang đưa dữ liệu vào Bộ máy Thống kê...")
    # Tính toán
    freq = stat_engine.calculate_frequency(draws, pool_size=45)
    gaps = stat_engine.calculate_gap(draws, pool_size=45)

    # Dùng hàm của Python để sắp xếp dữ liệu (từ cao xuống thấp)
    # Sắp xếp tần suất: Tìm các số xuất hiện nhiều nhất
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    
    # Sắp xếp Gap: Tìm các số 'gan' nhất (đã lâu chưa về)
    sorted_gaps = sorted(gaps.items(), key=lambda x: x[1], reverse=True)

    print("\n=============================================")
    print(" BẢNG XẾP HẠNG MEGA 6/45 (TRONG 100 KỲ QUA)")
    print("=============================================")
    
    print("\n🔥 TOP 5 SỐ 'NÓNG' (XUẤT HIỆN NHIỀU NHẤT):")
    for number, count in sorted_freq[:5]:
        print(f"  + Số {number:02d} : {count} lần")
        
    print("\n❄️ TOP 5 SỐ 'LẠNH' (GAN LÂU NHẤT CHƯA VỀ):")
    for number, gap in sorted_gaps[:5]:
        print(f"  + Số {number:02d} : Đã {gap} kỳ liên tiếp vắng bóng")

else:
    print("Lỗi khi tải dữ liệu:", history_result.get("message"))