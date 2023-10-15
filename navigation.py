import math
import time
import random
earthRadius = 6356752
class NAV():
    def __init__(self) -> None:
        self.homeLatitude = 0
        self.homeLongitude = 0
        self.lastLatitude = 0
        self.lastLongitude = 0
        self.velocity = 0
        self.lat_array = []
        self.lon_array = []
        self.isFlying = False
        self.isHomePosSet = False
        self.posIndex = 0
        self.posCount = 0
        self.cvg_last_lat = 0
        self.cvg_last_lon = 0
        self.last_t = 0
    
    def loiter(self,lat,lon,target_lat,tarhet_lon,radius,kc):
        dct1 = self.distanceBetweenTwopoint(lat,lon,target_lat,tarhet_lon)
        dct =dct1 - radius
        signDct = self.sign(dct)
        bearingUav2Wp = self.waypoint_bearing(lat,lon,target_lat,tarhet_lon)
        #bearingUav2Wp = self.swapAngle(bearingUav2Wp,90)
        lf=  90 - min(abs(dct*kc),90)*signDct
        yaw_command = bearingUav2Wp + lf
       #print(dct1)
        return yaw_command,dct


    def navStart(self,lat,lon):
        dt = time.time() - self.last_t
        if self.isHomePosSet == False:
            self.cvg_last_lat = lat
            self.cvg_last_lon = lon
            self.lastLatitude = lat
            self.lastLongitude = lon
            self.setHomePos(lat,lon)
            self.last_t = time.time()
            self.isHomePosSet = True
            return
        #van toc thang cua may bay
        self.velocity = self.distanceBetweenTwopoint(lat,lon,self.lastLatitude,self.lastLongitude)
        self.velocity /= dt
        # huong di chuyen so voi mat dat
        CourseOg =  self.courseOverGround(self.lastLatitude,self.lastLongitude,lat,lon)
        self.lastLatitude = lat
        self.lastLongitude = lon


        lenLat = len(self.lat_array)
        lenLon = len(self.lon_array)
        if lenLat == lenLon:
            self.posCount = lenLat
        if self.posCount > 0:
            disToNextP = self.distanceBetweenTwopoint(lat,lon,self.lat_array[self.posIndex],self.lon_array[self.posIndex])

    def courseOverGround(self,lat,lon):
        dx = math.radians(-lat - self.cvg_last_lat)*earthRadius
        dy = math.radians(lon - self.cvg_last_lon)*earthRadius
        self.cvg_last_lat = -lat
        self.cvg_last_lon = lon
        anlpha = abs(math.degrees(math.atan2(dx,dy)))
        belta = abs(math.degrees(math.atan2(dy,dx)))
        if(dx >= 0 and dy >= 0):
            angle = anlpha
            return angle
        if(dx >= 0 and dy <= 0):
            angle = 90 + belta
            return angle
        if(dx <= 0 and dy <= 0):
            angle = 90 + belta
            return angle
        if(dx <= 0 and dy >= 0):
            angle = 360 - anlpha
            return angle
    def waypoint_bearing(self,lat1,lon1,lat2,lon2):
        dy = math.radians(2.2*lat2 - 2.2*lat1)*earthRadius
        dx = math.radians(lon2 - lon1)*earthRadius
        anlpha = abs(math.degrees(math.atan2(dx,dy)))
        belta = abs(math.degrees(math.atan2(dy,dx)))
        if(dx >= 0 and dy >= 0):
            angle = anlpha
            return angle
        if(dx >= 0 and dy <= 0):
            angle = 90 + belta
            return angle
        if(dx <= 0 and dy <= 0):
            angle = 90 + belta
            return angle
        if(dx <= 0 and dy >= 0):
            angle = 360 - anlpha
            return angle
    def distanceToHome(self,lat,lon):# degre
        y = math.radians(lat - self.homeLatitude)*earthRadius
        x = math.radians(lon - self.homeLongitude)*earthRadius
        dis = math.sqrt(y*y + x*x)
        return dis
    def distanceBetweenTwopoint(self,lat1,lon1,lat2,lon2):
        a_coeff = math.radians(2.2*lat2 - 2.2*lat1)*earthRadius
        b_coeff = math.radians(lon2 - lon1)*earthRadius
        dis = math.sqrt(a_coeff*a_coeff + b_coeff*b_coeff)
        return dis

    def setHomePos(self,lat,lon):
        self.homeLongitude = lon
        self.homeLatitude = lat
        self.isHomePosSet = True
    def swapAngle(self,deg,swA):
        deg += swA
        if deg > 359:
            return deg - 359
        else:
            return deg
    def sign(self,x):
        k=0
        try:
            k = int(x/abs(x))
        except:
            k=0
        return k


class yawExtrame():
    def __init__(self) -> None:
        self.init = False
        self.last_yaw = 0
        self.step = 0
    def fixRange(self,yaw):
        if self.init == False:
            self.last_yaw = yaw
            self.init = True
            return 0
        else:
            if yaw - self.last_yaw > 200:
                self.step -= 360
            elif yaw - self.last_yaw < -200:
                self.step +=360
            self.last_yaw = yaw
            return (yaw + self.step)


   