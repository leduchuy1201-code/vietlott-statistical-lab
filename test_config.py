# Nhúng file cấu hình vừa tạo vào đây
from core.config import GAMES

print("Đang tải cấu hình hệ thống...")

# Lấy luật chơi của Mega
mega_rules = GAMES["MEGA645"]
print(f"Luật chơi {mega_rules['name']}: Chọn {mega_rules['numbers_per_draw']} số trong tập hợp {mega_rules['pool_size']} số.")

# Lấy luật chơi của Power
power_rules = GAMES["POWER655"]
print(f"Luật chơi {power_rules['name']}: Chọn {power_rules['numbers_per_draw']} số trong tập hợp {power_rules['pool_size']} số.")

print("Hoàn tất Bước 11!")
