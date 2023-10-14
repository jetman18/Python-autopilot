import serial
import time
import threading

running = True

class IBUS:
    IBUS_BUFFSIZE = 32
    def __init__(self,com) -> None:
        self.rcValue = [0 for i in range(0, 8)]
        self.ibus = [0 for i in range(0, self.IBUS_BUFFSIZE)]
        self.thre = threading.Thread(target=self.serial_listener)
        self.ibusIndex = 0
        self.stream = serial.Serial(
            port=com,\
            baudrate=115200,\
            parity=serial.PARITY_NONE,\
            stopbits=serial.STOPBITS_ONE,\
            bytesize=serial.EIGHTBITS,\
            timeout=0)
            
    def process(self,v):
        if self.ibusIndex == 0 and v != 0x20:
            return
        if self.ibusIndex == 1 and v != 0x40:
            self.ibusIndex = 0
            return
        if self.ibusIndex < self.IBUS_BUFFSIZE:
            self.ibus[self.ibusIndex] = v
        self.ibusIndex = self.ibusIndex + 1
        if self.ibusIndex == self.IBUS_BUFFSIZE:
            self.ibusIndex = 0
            chksum = 0xFFFF
            for i in range(0,30):
                chksum -= self.ibus[i]
            rxsum = self.ibus[30] + (self.ibus[31]<<8)
            if chksum == rxsum:
                self.rcValue[0] = (self.ibus[ 3]<<8) | self.ibus[ 2] 
                self.rcValue[1] = (self.ibus[ 5]<<8) | self.ibus[ 4]
                self.rcValue[2] = (self.ibus[ 7]<<8) | self.ibus[ 6]
                self.rcValue[3] = (self.ibus[ 9]<<8) | self.ibus[ 8]
                self.rcValue[4] = (self.ibus[11]<<8) | self.ibus[10]
                self.rcValue[5] = (self.ibus[13]<<8) | self.ibus[12]
                self.rcValue[6] = (self.ibus[15]<<8) | self.ibus[14]
                self.rcValue[7] = (self.ibus[17]<<8) | self.ibus[16]
    def serial_listener(self):
        while 1:
            for c in self.stream.read():
                self.process(c)
    def start(self):
        self.thre.start()
    def get(self):
        return self.rcValue
    def close(self):
        self.stream.close()
        self.thre.join()





