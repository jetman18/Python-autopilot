###
def swapAngle(deg,swA):
    deg += swA
    if deg > 359:
        return deg - 359
    else:
        return deg
    
def sign(x):
    temporary=0
    if x > 0:
        temporary = 1
    elif x < 0:
        temporary = -1
    return temporary

def range360(value):
    if  value < 0:
        value = 360 + value
    elif value >359:
        value = value - 360
    return value

def range180(value):
    if  value > 180:
        value = value - 360
    elif value < -180:
        value = value + 360
    return value

def range90(value):
    if  value > 90:
        value = 180 - value
    elif value < -90:
        value = (value + 180)*sign(value)
    return value

def constranin(value,min,max):
    if value > max:
        value = max
    elif value < min:
        value = min
    return value

