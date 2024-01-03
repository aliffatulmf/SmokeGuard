class Counter:
    def __init__(self):
        self.stats = 0

    def add(self, n=0):
        self.stats += n if n else 1

    def reset(self):
        self.stats.clear()
