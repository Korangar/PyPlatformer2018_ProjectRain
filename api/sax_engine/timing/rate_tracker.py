class RateTracker:
    def __init__(self, smoothing_factor: float = 0):
        self._ticks = 0
        self.smoothing = smoothing_factor
        self.rate = 0

    def increment(self, ticks: int = 1):
        self._ticks += ticks

    def measure(self):
        self.rate = self._ticks * (1 - self.smoothing) + self.rate * self.smoothing
        self._ticks = 0
