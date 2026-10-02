from core.pipeline import etl_pipeline

print("=== KHỞI ĐỘNG HỆ THỐNG DATA PIPELINE ===")

# Gọi đường ống chạy thử với 100 kỳ quay
result = etl_pipeline.run_etl_mega645(limit=100)

if result["status"] == "SUCCESS":
    print(f"\n✅ HOÀN TẤT! Đã đồng bộ thành công {result['count']} kỳ quay vào Database của bạn.")
    print("Hãy mở trang Firebase Console (Firestore) trên trình duyệt để kiểm tra thành quả!")
else:
    print(f"\n❌ LỖI: {result.get('message')}")