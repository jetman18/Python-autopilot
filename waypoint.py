
default_altitude = 400 #m
class wp():
    def __init__(self,name,altitude,latitude,longitude) -> None:
        self.name = name
        self.altitude = 0
        self.velocity = 0
        self.latitude = 0
        self.longitude = 0
class wayPoint():
    def __init__(self) -> None:
        self.wP=[]
        self.wp_count = 0
    def addWaypoint(self,name,altitude,latitude,longitude):
        self.wp_count +=1
        self.wP.append(wp(name,altitude,latitude,longitude))
    def deleteWaypoint(self,index):
        self.wp_count -=1
        self.wP.pop(index)
    def count(wayPoint):
        return wayPoint.wp_count
    def type(self,wp_index):
        return self.wP[wp_index].name
    def getAlt(self,wp_index):
        return self.wP[wp_index].altitude
    def getLat(self,wp_index):
        return self.wP[wp_index].latitude
    def getLon(self,wp_index):
        return self.wP[wp_index].longitude


