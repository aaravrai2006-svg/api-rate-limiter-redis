import time
from typing import Dict, List

class SlidingWindowLimiter:
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.records: Dict[str, List[float]] = {}

    def is_allowed(self, client_id: str) -> bool:
        now = time.time()
        timestamps = self.records.get(client_id, [])
        valid_timestamps = [t for t in timestamps if now - t < self.window_seconds]
        
        if len(valid_timestamps) < self.max_requests:
            valid_timestamps.append(now)
            self.records[client_id] = valid_timestamps
            return True
        return False

if __name__ == "__main__":
    limiter = SlidingWindowLimiter(max_requests=2, window_seconds=10)
    print("Req 1 allowed:", limiter.is_allowed("192.168.1.1"))
    print("Req 2 allowed:", limiter.is_allowed("192.168.1.1"))
    print("Req 3 allowed:", limiter.is_allowed("192.168.1.1"))
