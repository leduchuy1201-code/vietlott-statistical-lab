import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from core.statistics import stat_engine

class MachineLearningEngine:
    def __init__(self):
        # Sử dụng thuật toán Rừng ngẫu nhiên (Random Forest)
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    # ==========================================
    # CÁC HÀM DÀNH CHO MEGA 6/45 VÀ POWER 6/55
    # ==========================================
    def prepare_training_data(self, draws_history, pool_size=45):
        """Chuẩn bị dữ liệu để dạy AI (Feature Engineering)"""
        features = []
        labels = []

        # Chúng ta dùng lịch sử từ kỳ đầu tiên đến kỳ áp chót để dạy AI
        for i in range(10, len(draws_history) - 1):
            past_draws = draws_history[:i]
            next_draw = draws_history[i]

            freq = stat_engine.calculate_frequency(past_draws, pool_size)
            gap = stat_engine.calculate_gap(past_draws, pool_size)

            for number in range(1, pool_size + 1):
                features.append([freq[number], gap[number]])
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

        # Trích xuất đặc trưng hiện tại
        current_freq = stat_engine.calculate_frequency(draws_history, pool_size)
        current_gap = stat_engine.calculate_gap(draws_history, pool_size)
        
        X_today = []
        for number in range(1, pool_size + 1):
            X_today.append([current_freq[number], current_gap[number]])

        print("🧠 [AI] Đang dự đoán xác suất xuất hiện cho kỳ tới...")
        probabilities = self.model.predict_proba(X_today)[:, 1]

        number_probs = {num: float(prob) for num, prob in zip(range(1, pool_size + 1), probabilities)}
        sorted_probs = sorted(number_probs.items(), key=lambda x: x[1], reverse=True)

        top_6_picks = [num for num, prob in sorted_probs[:6]]
        
        return {
            "top_6_picks": top_6_picks,
            "details": sorted_probs[:10]
        }

    # ==========================================
    # CÁC HÀM DÀNH RIÊNG CHO MAX 3D
    # ==========================================
    def calculate_position_stats(self, col_history):
        """Tính tần suất và độ gan cho TỪNG CỘT (0-9) của Max 3D"""
        freq = {i: 0 for i in range(10)}
        total_draws = len(col_history)
        gap = {i: total_draws for i in range(10)}
        
        # Đếm tần suất
        for digit in col_history:
            freq[digit] += 1
            
        # Tính gap (đi lùi từ mới nhất về quá khứ)
        for draws_ago, digit in enumerate(reversed(col_history)):
            if gap[digit] == total_draws:
                gap[digit] = draws_ago
                
        return freq, gap

    def predict_max3d(self, draws_history):
        """Huấn luyện 3 mô hình độc lập cho 3 vị trí (Trăm, Chục, Đơn vị)"""
        if len(draws_history) < 20:
            return {"error": "Cần ít nhất 20 kỳ quay để huấn luyện AI"}

        print("🧠 [AI] Đang tách dữ liệu và xây dựng 3 mô hình học máy...")
        predictions = []
        
        # Lặp qua 3 cột (0: Trăm, 1: Chục, 2: Đơn vị)
        for col_idx in range(3):
            print(f"  -> Đang huấn luyện AI cho cột thứ {col_idx + 1} (Mô hình {col_idx + 1}/3)...")
            # Trích xuất riêng lịch sử của cột này
            col_history = [draw[col_idx] for draw in draws_history]
            
            features = []
            labels = []
            
            # Trích xuất đặc trưng (Feature Engineering)
            for i in range(10, len(col_history) - 1):
                past_draws = col_history[:i]
                next_digit = col_history[i]
                
                freq, gap = self.calculate_position_stats(past_draws)
                
                for digit in range(10):
                    features.append([freq[digit], gap[digit]])
                    # Nhãn = 1 nếu chữ số này xuất hiện ở kỳ tiếp theo
                    labels.append(1 if digit == next_digit else 0)
                    
            # Huấn luyện mô hình Random Forest cho riêng cột này
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(features, labels)
            
            # Trích xuất đặc trưng của ngày hôm nay để dự đoán ngày mai
            current_freq, current_gap = self.calculate_position_stats(col_history)
            X_today = [[current_freq[digit], current_gap[digit]] for digit in range(10)]
            
            # Chấm điểm xác suất (Lấy xác suất ra = 1)
            probabilities = model.predict_proba(X_today)[:, 1]
            digit_probs = {d: float(p) for d, p in zip(range(10), probabilities)}
            
            # Sắp xếp từ cao xuống thấp
            sorted_probs = sorted(digit_probs.items(), key=lambda x: x[1], reverse=True)
            
            # Lưu lại dự đoán của cột này
            predictions.append(sorted_probs)
            
        return predictions

# Biến toàn cục để dùng chung
ml_engine = MachineLearningEngine()