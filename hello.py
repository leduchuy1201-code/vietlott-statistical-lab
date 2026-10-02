import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

print("Đang khởi tạo kết nối Firebase...")

# 1. Khai báo thông tin xác thực từ file JSON
cred = credentials.Certificate('firebase_credentials.json')

# 2. Khởi tạo ứng dụng kết nối với Database URL của bạn
# CHÚ Ý: Thay đổi đường link bên dưới thành link của bạn
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://vietlott-statistical-lab-default-rtdb.firebaseio.com/' 
})

# 3. Trỏ đến nút gốc (root) của cơ sở dữ liệu
ref = db.reference('/')

# 4. Thử ghi một dữ liệu mẫu lên Firebase
print("Đang thử ghi dữ liệu...")
ref.set({
    'loi_chao': 'Xin chào Firebase từ Python Cloud Shell!',
    'trang_thai': 'Kết nối thành công'
})

# 5. Thử đọc dữ liệu vừa ghi về
print("Đang đọc dữ liệu từ Firebase...")
data = ref.get()
print("Dữ liệu nhận được:", data)

print("Hoàn tất kiểm tra!")