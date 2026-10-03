# vietlott-statistical-lab/core/config.py

# Cấu hình luật chơi cho các loại hình xổ số
GAMES = {
    "MEGA645": {
        "name": "Mega 6/45",
        "pool_size": 45,
        "numbers_per_draw": 6
    },
    "POWER655": {
        "name": "Power 6/55",
        "pool_size": 55,
        "numbers_per_draw": 6
    },
    "MAX3D": {
        "name": "Max 3D",
        "pool_size": 9,
        "positions": 3
    },
    "MAX3D_PLUS": {
        "name": "Max 3D+",
        "pool_size": 9,
        "positions": 6 # 2 bộ số x 3 chữ số = 6 vị trí cột
    }
}