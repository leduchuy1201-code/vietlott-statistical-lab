# Nhúng người quản lý database vừa tạo vào đây
from core.database import db_manager

print("1. Đang gọi Database Manager...")

# Thử yêu cầu người quản lý lấy ra thư mục 'games' (chứa thông tin luật chơi)
collection = db_manager.get_collection('games')

print(f"2. Kết nối thành công! Đã truy cập vào collection: {collection.id}")
print("Hoàn tất Bước 12!")
