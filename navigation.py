import math
import time
import random
import utils
earthRadius = 6356752
class NAV():
    def __init__(self) -> None:
        self.isFlying = False
        self.init = False
        self.wpInit = False
        self.isHomePosSet = False
        self.homeLatitude = 0
        self.homeLongitude = 0
        self.lastLatitude = 0
        self.lastLongitude = 0
        self.lastDistance2wp = 0
        self.velocity = 0
        self.posIndex = 0
        self.last_t = 0
        self.wpIndex = 0

    
    def cricleFlyMode1(self,lat,lon,target_lat,tarhet_lon,radius):
        dct1 = self.distanceBetweenTwopoint(lat,lon,target_lat,tarhet_lon)
        dct =dct1 - radius
        signDct = utils.sign(dct)
        kc = 500/radius
        bearingUav2Wp = self.courseOverGround(lat,lon,target_lat,tarhet_lon)
        lf =  90 - min(abs(dct*kc),90)*signDct
        yaw_command = bearingUav2Wp + lf
        yaw_command = utils.range360(yaw_command)
        return yaw_command,dct
    def cricleFlyMode2(self,lat,lon,target_lat,tarhet_lon,radius):
        kc = 10
        dct1 = self.distanceBetweenTwopoint(lat,lon,target_lat,tarhet_lon)
        dct =dct1 - radius
        signDct = utils.sign(dct)
        bearingUav2Wp = self.courseOverGround(lat,lon,target_lat,tarhet_lon)
        theta = math.degrees(math.atan2(radius,dct1))
        if dct > 0:
            lf =  90 - min(abs(dct*kc),90)*signDct - theta
        else:
            lf =  90 - min(abs(dct*kc),90)*signDct
        yaw_command = bearingUav2Wp + lf
        yaw_command = utils.range360(yaw_command)
        return yaw_command,dct

    def navigationStart(self,lat,lon,wp_list): # retrun yaw command 0-359
        kc = 0.22
        kd = 1
        dt = time.time() - self.last_t
        self.last_t = time.time()
        if self.isHomePosSet == False:
            self.lastLatitude = lat
            self.lastLongitude = lon
            self.setHomePos(lat,lon)
            self.isHomePosSet = True
            return 0
        
        # tim toa do gan nha
        if self.wpInit == False:
            min_dis = 10000000 # 1000 km
            for i in range(wp_list.count()):
                disOf2Wp = self.distanceBetweenTwopoint(lat,lon,wp_list.getLat(i),wp_list.getLon(i))
                if disOf2Wp <= min_dis:
                    min_dis = disOf2Wp
                    self.wpIndex = i + 1
            self.wpInit = True
        # toa do cuoi cung -> bay ve toa do ban dau
        # bay ve ha canh
        #print(self.wpIndex)
        if self.wpIndex == (wp_list.count()):
            #fly to fisrt wp or ...dst
            self.wpIndex = 0  # start from first wp
            print('dfdfd')
            return 0,0,0
        else:
            path_angle = self.courseOverGround(wp_list.getLat(self.wpIndex  - 1),
                                               wp_list.getLon(self.wpIndex - 1),
                                               wp_list.getLat(self.wpIndex),
                                               wp_list.getLon(self.wpIndex))
            #print('path angle:',path_angle)
            # cross track calculate
            dis2nextWp = self.distanceBetweenTwopoint(lat,lon,wp_list.getLat(self.wpIndex),
                                                              wp_list.getLon(self.wpIndex))
            
            phi = self.courseOverGround(lat,lon,wp_list.getLat(self.wpIndex),
                                                   wp_list.getLon(self.wpIndex))
            phi = path_angle - phi 
            phi = utils.range180(phi)
            #print(phi)
            phi = math.radians(phi)
            phi = utils.range90(phi)
            cross_track = dis2nextWp*math.sin(phi)
            dis2pathWp  = dis2nextWp*math.cos(phi)
            #print(int(dis2nextWp),' m')
            signCrossTrack = utils.sign(cross_track)
            temp = math.pow(abs(cross_track*kc),kd)
            theta = path_angle - min(temp,90)*signCrossTrack
            theta = utils.range360(theta)
            #print('theta',theta)
            if dt != 0:
                self.velocity = (dis2nextWp - self.lastDistance2wp)/dt
                self.lastDistance2wp = dis2nextWp
                #######################################
            if abs(dis2nextWp) < 300:  # 100m
                self.wpIndex += 1 # next path
            ##############
            #print('path angle:',path_angle,'  ',cross_track)
            return theta,dis2nextWp,self.wpIndex,cross_track
    def waypointApproach(lat,lon):
        pass

    def courseOverGround(self,lat1,lon1,lat2,lon2):
        dy = math.radians(lat2 - lat1)*earthRadius
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
        
    def waypointBearing(self,lat1,lon1,lat2,lon2):
        dy = math.radians(lat2 - lat1)*earthRadius
        #dy = math.radians(2.2*lat2 - 2.2*lat1)*earthRadius
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
        #a_coeff = math.radians(2.3*lat2 - 2.3*lat1)*earthRadius
        a_coeff = math.radians(lat2 - lat1)*earthRadius
        b_coeff = math.radians(lon2 - lon1)*earthRadius
        dis = math.sqrt(a_coeff*a_coeff + b_coeff*b_coeff)
        return dis

    def setHomePos(self,lat,lon):
        self.homeLongitude = lon
        self.homeLatitude = lat
        self.isHomePosSet = True


class anglextrame():
    def __init__(self) -> None:
        self.init = False
        self.last_value = 0
        self.step = 0
    def fixRange(self,yaw):
        if self.init == False:
            self.last_value = yaw
            self.init = True
            return yaw
        else:
            if yaw - self.last_value > 200:
                self.step -= 360
            elif yaw - self.last_value < -200:
                self.step +=360
            self.last_value = yaw
            return (yaw + self.step)


   