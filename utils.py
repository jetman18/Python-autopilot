###
def swapAngle(deg,swA):
    deg += swA
    if deg > 359:
        return deg - 359
    else:
        return deg
def sign(x):
    temporary=1
    try:
        temporary = int(x/abs(x))
    except:
        pass
    return temporary