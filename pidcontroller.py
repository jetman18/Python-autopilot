import time
class PID:
    max_I = 0.3
    def __init__(self,kp,ki,kd) -> None:
        self.init = False
        self.lastValue = 0
        self.lastExcTime = time.time()
        self.I = 0
        self.Dt = 0
        self.kp = kp
        self.ki = ki
        self.kd = kd
    def pidCalculate(self,value,setpoint):
        self.Dt = time.time() - self.lastExcTime
        self.lastExcTime = time.time()
        if self.Dt == 0:
            return 0
        eror = value - setpoint
        P = eror*self.kp
        self.I += eror*self.Dt*self.ki
        if self.I > PID.max_I:
            self.I = PID.max_I
        if self.I < -PID.max_I:
            self.I = -PID.max_I
        D = (value - self.lastValue)*self.kd/self.Dt
        self.lastValue = value
        return (P + self.I + D)
    
    def pidReset(self):
        self.lastValue = 0
        self.I = 0
    def get(self):
        return self.Dt