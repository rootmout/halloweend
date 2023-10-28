
class EntityManager:
    def __init__(self):
        self.timeBetweenBlinkMin = 0
        self.timeBetweenBlinkMax = 0
        self.timeActiveMin = 0
        self.timeActiveMax = 0
        self.timeHiddenMin = 0
        self.timeHiddenMax = 0
    def setTimeBetweenBlink(self, min, max):
        self.timeBetweenBlinkMin = min
        self.timeBetweenBlinkMax = max


entity
