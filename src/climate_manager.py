# src/climate_manager.py
import random
import time
from config.stats import CLIMATE_WEIGHTS, CLIMATE_CHANGE_INTERVAL

class ClimateManager:
    def __init__(self):
        # pick initial climate
        types, weights = zip(*CLIMATE_WEIGHTS.items())
        self.current = "Sunny"
        # schedule next roll
        self.next_change = time.perf_counter() + CLIMATE_CHANGE_INTERVAL

    def update(self):
        """Call once per frame.  When the timer elapses,
           randomly pick a new climate and reset timer."""
        now = time.perf_counter()
        if now >= self.next_change:
            types, weights = zip(*CLIMATE_WEIGHTS.items())
            self.current = random.choices(types, weights)[0]
            self.next_change = now + CLIMATE_CHANGE_INTERVAL

    def get(self):
        return self.current
