from datetime import datetime, timedelta
import random
import threading
import os
import time

class MeterReading:
    def __init__(self):
        self.readings = {}  # Stores all meter readings
        self.logs = []  # Logs all API requests
        os.makedirs("logs", exist_ok=True)  # Ensure 'logs' directory exists

    def add_reading(self, meter_id, timestamp, kwh):
        """Adds a new meter reading"""
        if meter_id not in self.readings:
            self.readings[meter_id] = []
        self.readings[meter_id].append({"timestamp": timestamp, "kwh": kwh})
        self.log_request("meter-reading", {"meter_id": meter_id, "timestamp": timestamp, "kwh": kwh})

    def get_readings(self, meter_id):
        """Retrieves all readings for a specific meter"""
        return self.readings.get(meter_id, [])

    def log_request(self, endpoint, data):
        """Logs API requests to a file"""
        log_entry = f"{datetime.now()} - {endpoint}: {data}\n"
        self.logs.append(log_entry)
        with open("logs/meter_readings.log", "a") as log_file:
            log_file.write(log_entry)

# ✅ Initialize `meter_reading_manager` before using it
meter_reading_manager = MeterReading()

class BatchJobManager:
    def __init__(self, meter_reading_manager):
        self.meter_reading_manager = meter_reading_manager

    def clean_old_data(self):
        """Removes meter readings older than 30 days"""
        cutoff_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        for meter_id in list(self.meter_reading_manager.readings.keys()):
            self.meter_reading_manager.readings[meter_id] = [
                r for r in self.meter_reading_manager.readings[meter_id]
                if r["timestamp"].split()[0] >= cutoff_date
            ]

    def prepare_new_day(self):
        """Simulates initializing new day's meter readings"""
        for meter_id in self.meter_reading_manager.readings.keys():
            self.meter_reading_manager.add_reading(meter_id, datetime.now().strftime("%Y-%m-%d 01:00"), 0)

    def run_daily_jobs(self):
        """Executes daily batch processing"""
        print("Running daily batch jobs...")
        self.clean_old_data()
        self.prepare_new_day()
        print("Daily batch jobs completed.")

# ✅ Ensure `BatchJobManager` is initialized **after** `meter_reading_manager`
job_manager = BatchJobManager(meter_reading_manager)

def schedule_daily_jobs():
    """Runs daily batch jobs at midnight (00:00)"""
    while True:
        now = datetime.now()
        if now.hour == 0 and now.minute == 0:
            job_manager.run_daily_jobs()
        time.sleep(60)  # Check every minute

# ✅ Start the daily job scheduler in a background thread
threading.Thread(target=schedule_daily_jobs, daemon=True).start()
