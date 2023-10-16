
default_altitude = 400 #m
class wp():
    def __init__(self,name,latitude,longitude,altitude) -> None:
        self.name = name
        self.altitude = altitude
        self.velocity = 0
        self.latitude = latitude
        self.longitude = longitude
class wayPoint():
    def __init__(self) -> None:
        self.wP=[]
        self.wp_count = 0
    def addWaypoint(self,name,latitude,longitude,altitude):
        self.wp_count +=1
        self.wP.append(wp(name,latitude,longitude,altitude))

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


