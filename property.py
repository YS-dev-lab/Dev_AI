class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius      # setter 통해 검증

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("절대영도보다 낮을 수 없어요")
        self._celsius = value

    @property
    def fahrenheit(self):          # 읽기 전용, 자동 계산
        return round(self._celsius * 9/5 + 32, 1)

    @property
    def kelvin(self):
        return round(self._celsius + 273.15, 1)

    @property
    def state(self):
        if self._celsius <= 0:   return "얼음"
        if self._celsius < 100:  return "물"
        return "수증기"

t = Temperature(100)
print(t.fahrenheit)   # 212.0  — () 없이!
print(t.kelvin)       # 373.2
print(t.state)        # 수증기
t.celsius = -300      # ❌ ValueError