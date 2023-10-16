
from waypoint import wayPoint
from navigation import NAV
import time
k = NAV()

wp = wayPoint()

wp.addWaypoint('wpp',0,0,0)
wp.addWaypoint('wp',0.002,-0.002,0)
wp.addWaypoint('wp',0.003,-0.003,0)

k.navigationStart(0.0,0.001,wp)
time.sleep(0.6)
k.navigationStart(0.0,0.001,wp)



