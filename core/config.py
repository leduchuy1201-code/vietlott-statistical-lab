# vietlott-statistical-lab/core/config.py

# Cấu hình luật chơi cho các loại hình xổ số
GAMES = {
    "MEGA645": {
        "name": "Mega 6/45",
        "pool_size": 45,           # Tổng số bóng (từ 1 đến 45)
        "numbers_per_draw": 6      # Số bóng được rút mỗi kỳ quay
    },
    "POWER655": {
        "name": "Power 6/55",
        "pool_size": 55,           # Tổng số bóng (từ 1 đến 55)
        "numbers_per_draw": 6      # Số bóng được rút mỗi kỳ quay
    },
    "MAX3D": {
        "name": "Max 3D",
        "pool_size": 9,            # Các chữ số xoay vòng từ 0 đến 9
        "positions": 3             # Có 3 vị trí: Trăm, Chục, Đơn vị
    }
}