import windowview
import multiprocessing as mp
import navigation

import waypoint

wp = waypoint.wayPoint()
k=navigation.NAV()
home_lat = 37.628715674334124
home_lon =-122.39334575867426

wp.addWaypoint('to',0,0,0)
wp.addWaypoint('wp',1,0,0)
wp.addWaypoint('wp',2,2,0)

for i in range(4):
    h=k.navigationStart(2,-1,wp)



