
import struct
import multiprocessing as mp
import time
from windowview import window
import time
import signal
import os
if __name__ == '__main__':
    p1,p2 = mp.Pipe()
    b = window(p1)
    while b.isRun():
        if p2.poll():
            m=p2.recv()
            f= struct.unpack('ddd',m)
            print(f[0],'  ',f[1],' ',f[2])
        print(b.isRun())
        time.sleep(1)
        
