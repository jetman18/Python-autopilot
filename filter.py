import math
class LPF():
    def __init__(self,fcut,dt) -> None:
        self.f_cut = fcut
        self.value = 0
        self.rc = 1/(2*math.pi*self.f_cut)
        self.gain = dt/(self.rc + dt)
        print(self.gain)
    def lpfApply(self,input):
        self.value = self.value + self.gain*(input - self.value)
        return self.value
