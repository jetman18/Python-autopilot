import time
from utils import *
class PID:
    def __init__(self,kp,ki,kd) -> None:
        self.init = False
        self.lastValue = 0
        self.lastExcTime = time.time()
        self.I = 0
        self.Dt = 0
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.maxI = 0.7
    def pidCalculate(self,value,setpoint):
        self.Dt = time.time() - self.lastExcTime
        self.lastExcTime = time.time()
        if self.Dt == 0:
            return 0
        eror = value - setpoint
        P = eror*self.kp
        self.I += eror*self.Dt*self.ki
        if self.I > self.maxI:
            self.I = self.maxI
        if self.I < -self.maxI:
            self.I = -self.maxI
        D = (value - self.lastValue)*self.kd/self.Dt
        self.lastValue = value
        return (P + self.I + D)
    def setmaxI(self,val):
         self.maxI = val
    
    
    def yawPid(self,value,setpoint):
        self.Dt = time.time() - self.lastExcTime
        self.lastExcTime = time.time()
        if self.Dt == 0:
            return 0
        eror = value - setpoint
        eror = range180(eror)
        '''
        if eror > 180:
            eror = eror - 360
        elif eror < -180:
            eror = eror + 360
        '''
        P = eror*self.kp
        self.I += eror*self.Dt*self.ki
        if self.I > self.maxI:
            self.I = self.maxI
        if self.I < -self.maxI:
            self.I = -self.maxI
        D = (value - self.lastValue)*self.kd/self.Dt
        self.lastValue = value
        return (P + self.I + D)
    
    def pidReset(self):
        self.lastValue = 0
        self.I = 0
    def get(self):
        return self.Dt