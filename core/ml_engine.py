# vietlott-statistical-lab/core/ml_engine.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from core.statistics import stat_engine

class MachineLearningEngine:
    def __init__(self):
        # Sử dụng thuật toán Rừng ngẫu nhiên (Random Forest)
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    def prepare_training_data(self, draws_history, pool_size=45):
        """Chuẩn bị dữ liệu để dạy AI (Feature Engineering)"""
        features = []
        labels = []

        # Chúng ta dùng lịch sử từ kỳ đầu tiên đến kỳ áp chót để dạy AI
        # AI sẽ dự đoán kết quả của kỳ ngay sau đó
        for i in range(10, len(draws_history) - 1):
            # Lấy lịch sử tính đến kỳ i
            past_draws = draws_history[:i]
            # Kết quả thực tế của kỳ i+1 (để làm đáp án/nhãn chấm điểm AI)
            next_draw = draws_history[i]

            # Tính toán đặc trưng (Features) tại thời điểm i
            freq = stat_engine.calculate_frequency(past_draws, pool_size)
            gap = stat_engine.calculate_gap(past_draws, pool_size)

            # Ghi chép lại đặc trưng của từng con số (từ 1 đến 45)
            for number in range(1, pool_size + 1):
                features.append([freq[number], gap[number]])
                # Nếu số này trúng ở kỳ tiếp theo, nhãn = 1, ngược lại = 0
                labels.append(1 if number in next_draw else 0)

        return features, labels

    def predict_next_draw(self, draws_history, pool_size=45):
        """Huấn luyện và dự đoán kỳ quay tương lai"""
        if len(draws_history) < 20:
            return {"error": "Cần ít nhất 20 kỳ quay để huấn luyện AI"}

        print("🧠 [AI] Đang trích xuất đặc trưng và chuẩn bị dữ liệu...")
        X_train, y_train = self.prepare_training_data(draws_history, pool_size)

        print(f"🧠 [AI] Đang huấn luyện mô hình Random Forest trên {len(X_train)} mẫu dữ liệu...")
        self.model.fit(X_train, y_train)

        # Trích xuất đặc trưng hiện tại (của ngày hôm nay) để đoán tương lai
        current_freq = stat_engine.calculate_frequency(draws_history, pool_size)
        current_gap = stat_engine.calculate_gap(draws_history, pool_size)
        
        X_today = []
        for number in range(1, pool_size + 1):
            X_today.append([current_freq[number], current_gap[number]])

        print("🧠 [AI] Đang dự đoán xác suất xuất hiện cho kỳ tới...")
        # Lấy xác suất dự đoán (probability) cho nhãn '1' (xuất hiện)
        probabilities = self.model.predict_proba(X_today)[:, 1]

        # Ghép số với xác suất của nó và sắp xếp từ cao xuống thấp
        number_probs = {num: float(prob) for num, prob in zip(range(1, pool_size + 1), probabilities)}
        sorted_probs = sorted(number_probs.items(), key=lambda x: x[1], reverse=True)

        # Lấy 6 số có xác suất cao nhất do AI gợi ý
        top_6_picks = [num for num, prob in sorted_probs[:6]]
        
        return {
            "top_6_picks": top_6_picks,
            "details": sorted_probs[:10] # Top 10 chi tiết
        }

# Biến toàn cục
ml_engine = MachineLearningEngine()
