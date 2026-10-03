# vietlott-statistical-lab/app.py
from flask import Flask, jsonify, render_template
from core.database import db_manager
from core.statistics import stat_engine
from core.ml_engine import ml_engine
from core.collector import data_collector

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# API MEGA 6/45
@app.route('/api/v1/stats/mega645', methods=['GET'])
def get_mega645_stats():
    collection = db_manager.get_collection('mega645_history')
    docs = collection.stream()
    all_draws = [{"id": doc.id, "numbers": doc.to_dict().get('numbers', [])} for doc in docs]
    if not all_draws: return jsonify({"error": "Chưa có dữ liệu"}), 404
    all_draws_sorted = sorted(all_draws, key=lambda x: x['id'])
    draws_only = [item['numbers'] for item in all_draws_sorted[-100:]]
    freq = stat_engine.calculate_frequency(draws_only, 45)
    gaps = stat_engine.calculate_gap(draws_only, 45)
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:5]
    sorted_gaps = sorted(gaps.items(), key=lambda x: x[1], reverse=True)[:5]
    ai_prediction = ml_engine.predict_next_draw(draws_only, 45)
    return jsonify({
        "game": "MEGA 6/45", "analyzed_draws": len(draws_only),
        "hot_numbers": [{"number": f"{k:02d}", "frequency": v} for k, v in sorted_freq],
        "cold_numbers": [{"number": f"{k:02d}", "gap_days": v} for k, v in sorted_gaps],
        "ai_prediction": ai_prediction 
    })

# API MAX 3D
@app.route('/api/v1/stats/max3d', methods=['GET'])
def get_max3d_stats():
    result = data_collector.fetch_history_max3d(limit=500)
    if result["status"] != "SUCCESS": return jsonify({"error": result.get("message")}), 500
    draws = result["draws"]
    predictions = ml_engine.predict_positional(draws, positions=3) # Trích xuất 3 cột
    if isinstance(predictions, dict) and "error" in predictions: return jsonify({"error": predictions["error"]}), 500
    
    best_number = "".join([str(predictions[i][0][0]) for i in range(3)])
    return jsonify({
        "game": "MAX 3D", "analyzed_draws": len(draws),
        "ai_prediction": {
            "best_number": best_number,
            "details": {
                "tram": [{"digit": d, "prob": p} for d, p in predictions[0][:3]],
                "chuc": [{"digit": d, "prob": p} for d, p in predictions[1][:3]],
                "don_vi": [{"digit": d, "prob": p} for d, p in predictions[2][:3]]
            }
        }
    })

# API MAX 3D+ (PRO)
@app.route('/api/v1/stats/max3dplus', methods=['GET'])
def get_max3dplus_stats():
    result = data_collector.fetch_history_max3d_plus(limit=500)
    if result["status"] != "SUCCESS": return jsonify({"error": result.get("message")}), 500
    draws = result["draws"]
    predictions = ml_engine.predict_positional(draws, positions=6) # Trích xuất 6 cột
    if isinstance(predictions, dict) and "error" in predictions: return jsonify({"error": predictions["error"]}), 500
    
    # Tách thành 2 dãy số (3 số đầu và 3 số cuối)
    best_number_1 = "".join([str(predictions[i][0][0]) for i in range(0, 3)])
    best_number_2 = "".join([str(predictions[i][0][0]) for i in range(3, 6)])
    
    return jsonify({
        "game": "MAX 3D+", "analyzed_draws": len(draws),
        "ai_prediction": {
            "best_number_1": best_number_1,
            "best_number_2": best_number_2,
            "details_1": {
                "tram": [{"digit": d, "prob": p} for d, p in predictions[0][:3]],
                "chuc": [{"digit": d, "prob": p} for d, p in predictions[1][:3]],
                "don_vi": [{"digit": d, "prob": p} for d, p in predictions[2][:3]]
            },
            "details_2": {
                "tram": [{"digit": d, "prob": p} for d, p in predictions[3][:3]],
                "chuc": [{"digit": d, "prob": p} for d, p in predictions[4][:3]],
                "don_vi": [{"digit": d, "prob": p} for d, p in predictions[5][:3]]
            }
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)