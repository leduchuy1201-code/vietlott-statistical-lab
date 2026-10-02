from core.statistics import stat_engine

print("--- KIỂM TRA BỘ MÁY THỐNG KÊ ---")
# Giả lập lịch sử 4 kỳ quay (Kỳ 1 cũ nhất, Kỳ 4 mới nhất)
fake_history = [
    [1, 2, 3, 4, 5, 6],       # Kỳ 1
    [1, 7, 8, 9, 11, 12],     # Kỳ 2
    [2, 5, 13, 14, 15, 16],   # Kỳ 3
    [10, 20, 30, 40, 41, 42]  # Kỳ 4 (Mới nhất)
]

print("Dữ liệu lịch sử giả lập (4 kỳ):")
for i, draw in enumerate(fake_history):
    print(f"Kỳ {i+1}: {draw}")

# Tính toán Tần suất và Gap (Giả sử chơi Mega 6/45)
freq = stat_engine.calculate_frequency(fake_history, pool_size=45)
gaps = stat_engine.calculate_gap(fake_history, pool_size=45)

print("\n--- KẾT QUẢ THỐNG KÊ TẦN SUẤT ---")
print(f"Số 1 xuất hiện: {freq[1]} lần")
print(f"Số 5 xuất hiện: {freq[5]} lần")
print(f"Số 99 xuất hiện: {freq.get(99, 'Không tồn tại (Đúng luật)')}")

print("\n--- KẾT QUẢ THỐNG KÊ GAP (KHOẢNG CÁCH) ---")
print(f"Gap của số 10: {gaps[10]} kỳ (Vì vừa ra ở kỳ 4 mới nhất)")
print(f"Gap của số 5: {gaps[5]} kỳ (Ra ở kỳ 3, cách hiện tại 1 kỳ)")
print(f"Gap của số 1: {gaps[1]} kỳ (Ra ở kỳ 2, cách hiện tại 2 kỳ)")
print(f"Gap của số 45: {gaps[45]} kỳ (Chưa từng ra trong cả 4 kỳ)")
