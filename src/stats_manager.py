import time
from config.stats import STATS_INITIAL, STATS_RATES

class StatsManager:
    def __init__(self):
        # copy initial values
        self.values = dict(STATS_INITIAL)
        self.last_update = time.perf_counter()

    def update(self):
        now = time.perf_counter()
        dt = now - self.last_update
        self.last_update = now

        # increment each stat
        for key, rate in STATS_RATES.items():
            self.values[key] = min(1.0, self.values[key] + rate * dt)

    def get(self, key):
        return self.values.get(key, 0)
        
    def set(self, key, value):
        """Set a specific stat to a given value"""
        self.values[key] = max(0.0, min(1.0, value))  # Clamp between 0 and 1
        
    def adjust(self, key, amount):
        """Adjust a stat by a given amount"""
        current = self.get(key)
        self.set(key, current + amount)
        
    def reset(self):
        """Reset all stats to initial values"""
        self.values = dict(STATS_INITIAL)
        self.last_update = time.perf_counter()