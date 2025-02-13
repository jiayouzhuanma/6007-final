from flask import Flask, request, jsonify
from datetime import datetime
import threading
import time
from data_stru import MeterReading
import random


app = Flask(__name__)
meter_reading_manager = MeterReading()

@app.route('/meter-reading', methods=['POST'])
def add_meter_reading():
    """用户提交单次电表读数"""
    data = request.json
    meter_id = data.get("meter_id")
    kwh = data.get("kwh")

    # 生成时间戳（格式: YYYY-MM-DD HH:MM）
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    if not meter_id or not kwh:
        return jsonify({"error": "Missing meter_id or kwh"}), 400

    meter_reading_manager.add_reading(meter_id, timestamp, kwh)
    return jsonify({"message": "Meter reading recorded successfully"}), 200

@app.route('/meter-reading/<meter_id>', methods=['GET'])
def get_meter_readings(meter_id):
    """查询某个电表的所有读数"""
    readings = meter_reading_manager.get_readings(meter_id)
    return jsonify({"meter_id": meter_id, "readings": readings}), 200

def auto_meter_reading():
    """模拟每半小时采集电表数据"""
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        meter_id = "123-456-789"
        kwh = round(random.uniform(5, 20), 1)  # 随机生成 5~20 kWh
        meter_reading_manager.add_reading(meter_id, timestamp, kwh)
        print(f"[{timestamp}] Auto meter reading: {meter_id} - {kwh} kWh")
        time.sleep(1800)  # 30 分钟读取一次

if __name__ == '__main__':
    threading.Thread(target=auto_meter_reading, daemon=True).start()
    app.run(debug=True)

