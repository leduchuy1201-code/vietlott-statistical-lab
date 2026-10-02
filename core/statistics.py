# vietlott-statistical-lab/core/statistics.py

class StatisticalEngine:
    def __init__(self):
        pass

    def calculate_frequency(self, draws_history, pool_size=45):
        """
        Tính số lần xuất hiện của từng con số trong lịch sử.
        draws_history: Danh sách các mảng con số (từ cũ nhất đến mới nhất)
        """
        # Tạo một từ điển (dictionary) đếm từ 1 đến pool_size, mặc định = 0
        frequency = {i: 0 for i in range(1, pool_size + 1)}
        
        # Duyệt qua từng kỳ quay, và từng con số trong kỳ quay đó
        for draw in draws_history:
            for number in draw:
                if number in frequency:
                    frequency[number] += 1
                    
        return frequency

    def calculate_gap(self, draws_history, pool_size=45):
        """
        Tính số kỳ quay liên tiếp mà một con số chưa xuất hiện (Gap).
        Khoảng cách 0 nghĩa là vừa xuất hiện ở kỳ gần nhất.
        """
        # Mặc định, nếu chưa từng xuất hiện, gap sẽ bằng tổng số kỳ quay
        total_draws = len(draws_history)
        gap = {i: total_draws for i in range(1, pool_size + 1)}
        
        # Lật ngược lịch sử (Duyệt từ kỳ quay MỚI NHẤT lùi về QUÁ KHỨ)
        # enumerate giúp chúng ta đếm lùi: 0 (mới nhất), 1 (kỳ trước), 2...
        for draws_ago, draw in enumerate(reversed(draws_history)):
            for number in draw:
                # Nếu số này chưa được tính gap (nghĩa là lần đầu tiên ta gặp nó khi đi lùi)
                if gap[number] == total_draws:
                    gap[number] = draws_ago
                    
        return gap

# Tạo biến toàn cục để sử dụng
stat_engine = StatisticalEngine()