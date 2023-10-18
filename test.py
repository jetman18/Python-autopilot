import windowview
import multiprocessing as mp
import navigation

import waypoint

wp = waypoint.wayPoint()
k=navigation.NAV()
home_lat = 37.628715674334124
home_lon =-122.39334575867426

wp.addWaypoint('to',home_lat,home_lon,0)
wp.addWaypoint('wp',home_lat,home_lon + 0.04,0)
wp.addWaypoint('wp',home_lat + 0.04,home_lon + 0.04,0)
wp.addWaypoint('wp',home_lat + 0.04,home_lon,0)
for i in range(400):
    h=k.navigationStart(home_lat,home_lon + i/100000,wp)
    print(h)


