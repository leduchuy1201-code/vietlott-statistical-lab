import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

print("1. Đang khởi tạo kết nối với Firestore...")
# Khai báo thông tin xác thực từ file JSON (chìa khóa của bạn)
cred = credentials.Certificate('firebase_credentials.json')

# Kiểm tra xem app đã khởi tạo chưa để tránh lỗi chạy trùng
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Kết nối trực tiếp vào Firestore
db = firestore.client()

print("2. Đang thử ghi dữ liệu vào Firestore...")
# Tạo một 'collection' (thư mục) tên là 'kiem_tra' 
# và một 'document' (tài liệu) tên là 'phien_ban'
doc_ref = db.collection('kiem_tra').document('phien_ban')

doc_ref.set({
    'ung_dung': 'Vietlott Statistical Lab',
    'trang_thai': 'Kết nối Firestore THÀNH CÔNG!',
    'muc_tieu': 'Sẵn sàng thu thập dữ liệu'
})

print("3. Ghi dữ liệu thành công! Đang đọc dữ liệu về...")
# Đọc dữ liệu vừa ghi
doc = doc_ref.get()
if doc.exists:
    print("-> Dữ liệu từ Firestore:", doc.to_dict())
else:
    print("-> Không tìm thấy dữ liệu!")
    
print("Hoàn tất bài kiểm tra Milestone 3!")