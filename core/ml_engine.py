# vietlott-statistical-lab/core/ml_engine.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from core.statistics import stat_engine

class MachineLearningEngine:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    # ==========================================
    # HÀM AI DÀNH CHO MEGA 6/45
    # ==========================================
    def prepare_training_data(self, draws_history, pool_size=45):
        features, labels = [], []
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
        if len(draws_history) < 20: return {"error": "Cần ít nhất 20 kỳ"}
        X_train, y_train = self.prepare_training_data(draws_history, pool_size)
        self.model.fit(X_train, y_train)
        current_freq = stat_engine.calculate_frequency(draws_history, pool_size)
        current_gap = stat_engine.calculate_gap(draws_history, pool_size)
        X_today = [[current_freq[number], current_gap[number]] for number in range(1, pool_size + 1)]
        probabilities = self.model.predict_proba(X_today)[:, 1]
        sorted_probs = sorted({num: float(prob) for num, prob in zip(range(1, pool_size + 1), probabilities)}.items(), key=lambda x: x[1], reverse=True)
        return {"top_6_picks": [num for num, prob in sorted_probs[:6]], "details": sorted_probs[:10]}

    # ==========================================
    # HÀM AI DÀNH CHO MAX 3D & MAX 3D+ (Đa năng)
    # ==========================================
    def calculate_position_stats(self, col_history):
        freq = {i: 0 for i in range(10)}
        total_draws = len(col_history)
        gap = {i: total_draws for i in range(10)}
        for digit in col_history: freq[digit] += 1
        for draws_ago, digit in enumerate(reversed(col_history)):
            if gap[digit] == total_draws: gap[digit] = draws_ago
        return freq, gap

    def predict_positional(self, draws_history, positions=3):
        """Hàm đa năng: Nếu truyền positions=3 sẽ dự đoán Max 3D. positions=6 sẽ dự đoán Max 3D+"""
        if len(draws_history) < 20: return {"error": "Cần ít nhất 20 kỳ để huấn luyện"}
        
        predictions = []
        for col_idx in range(positions):
            col_history = [draw[col_idx] for draw in draws_history]
            features, labels = [], []
            for i in range(10, len(col_history) - 1):
                past_draws = col_history[:i]
                next_digit = col_history[i]
                freq, gap = self.calculate_position_stats(past_draws)
                for digit in range(10):
                    features.append([freq[digit], gap[digit]])
                    labels.append(1 if digit == next_digit else 0)
                    
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(features, labels)
            current_freq, current_gap = self.calculate_position_stats(col_history)
            X_today = [[current_freq[digit], current_gap[digit]] for digit in range(10)]
            probabilities = model.predict_proba(X_today)[:, 1]
            sorted_probs = sorted({d: float(p) for d, p in zip(range(10), probabilities)}.items(), key=lambda x: x[1], reverse=True)
            predictions.append(sorted_probs)
            
        return predictions

ml_engine = MachineLearningEngine()