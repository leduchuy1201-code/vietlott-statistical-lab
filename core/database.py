# vietlott-statistical-lab/core/database.py
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class FirestoreManager:
    def __init__(self):
        """Khởi tạo kết nối đến Firestore một lần duy nhất"""
        # Kiểm tra xem hệ thống đã kết nối chưa để tránh lỗi chạy trùng
        if not firebase_admin._apps:
            # Đọc chìa khóa bảo mật
            cred = credentials.Certificate('firebase_credentials.json')
            firebase_admin.initialize_app(cred)
        
        # Tạo đối tượng quản lý database
        self.db = firestore.client()

    def get_collection(self, collection_name):
        """Lấy một thư mục (collection) trong database"""
        return self.db.collection(collection_name)

# Tạo một biến db_manager để các file khác trong dự án có thể dùng chung
db_manager = FirestoreManager()
