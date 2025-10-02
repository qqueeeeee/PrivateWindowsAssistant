import time
import json
from collections import deque
from pathlib import Path
from datetime import datetime

class GroqRequestTracker:
    def __init__(self, store_dir="tracker/tracker_data"):
        self.store_dir = Path(store_dir)
        self.store_dir.mkdir(exist_ok=True)
        
        self.today_str = datetime.now().strftime("%Y-%m-%d")
        self.store_file = self.store_dir / f"tracker_{self.today_str}.json"
        
        self.request_times = deque()
        self._load_today_file()

    def _load_today_file(self):
        if self.store_file.exists():
            try:
                data = json.load(self.store_file.open("r"))
                self.request_times = deque(data)
            except Exception:
                self.request_times = deque()

    def _cleanup(self):
        now = time.time()
        while self.request_times and now - self.request_times[0] > 86400:
            self.request_times.popleft()

    async def send_request(self, api_func, *args, **kwargs):
        today_str = datetime.now().strftime("%Y-%m-%d")
        if today_str != self.today_str:
            self.today_str = today_str
            self.store_file = self.store_dir / f"tracker_{self.today_str}.json"
            self.request_times = deque()
        
        result = await api_func(*args, **kwargs)
        self.request_times.append(time.time())
        self._save_today_file()
        return result
    
    def _save_today_file(self):
        json.dump(list(self.request_times), self.store_file.open("w"))

    def get_stats(self):
        self._cleanup()
        rpm = sum(1 for t in self.request_times if time.time() - t <= 60)
        rpd = len(self.request_times)
        return {
            "RPM": rpm,
            "RPD": rpd,
            "File": str(self.store_file)
        }
