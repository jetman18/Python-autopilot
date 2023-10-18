"""
Start FlightGear with:
`fgfs --native-fdm=socket,out,30,localhost,5501,udp --native-ctrls=socket,out,30,localhost,5503,udp --native-ctrls=socket,in,30,localhost,5504,udp --aircraft=sf260`
"""
from utils import *
import waypoint
import navigation
import time
import math
import pidcontroller
from flightgear_python.fg_if import FDMConnection, CtrlsConnection
from windowview import window
import multiprocessing as mp
import struct
def ctrls_callback(ctrls_data, event_pipe):
    #if event_pipe.child_poll():
    ail_ctrl,ele_ctrl,rud_ctrl,thro_ctrl,flap_ctrl = event_pipe.child_recv()  
    ctrls_data.elevator = ele_ctrl
    ctrls_data.aileron  = -ail_ctrl
    ctrls_data.aile =   rud_ctrl
    ctrls_data.throttle[0] = 1#thro_ctrl
    #ctrls_data.flaps = flap_ctrl
    return ctrls_data

def fdm_callback(fdm_data, event_pipe):
    buffer =[]
    buffer.append(math.degrees(fdm_data.phi_rad))
    buffer.append(math.degrees(fdm_data.theta_rad))
    buffer.append( math.degrees(fdm_data.psi_rad))
    buffer.append(math.degrees(fdm_data.lat_rad))
    buffer.append(math.degrees(fdm_data.lon_rad))
    buffer.append(fdm_data.alt_m)
    buffer.append(fdm_data.eng_state[0])
    buffer.append(math.degrees(fdm_data.psidot_rad_per_s))
    event_pipe.child_send((buffer))

if __name__ == '__main__':  # NOTE: This is REQUIRED on Windows!
    ctrls_conn = CtrlsConnection(ctrls_version=27)
    ctrls_event_pipe = ctrls_conn.connect_rx('localhost', 5503, ctrls_callback)
    ctrls_conn.connect_tx('localhost', 5504)
    
    fdm_conn = FDMConnection(fdm_version=24)  # May need to change version from 24
    fdm_event_pipe = fdm_conn.connect_rx('localhost', 5501, fdm_callback)
    fdm_event_pipe.is_set()

    ctrls_conn.start()  # Start the Ctrls RX/TX loop
    fdm_conn.start()  # Start the FDM RX loop0
    ##### END INIT #######################
    # roll kd= 0.01 
    roll = pidcontroller.PID(0.05,0.01,0.003) # 0,02  0.002
    pitch = pidcontroller.PID(0.02,0,0)
    yaw = pidcontroller.PID(1,0,0)


    roll_deg_set = 0
    pitch_deg_set = 12
   

    recvAtitude=[]
    nav = navigation.NAV()
    yaw_loiter = navigation.anglextrame()
    yaw_aircraft = navigation.anglextrame()
    p1,p2 = mp.Pipe()
    wd = window(p1)
    timer = time.time()
    loiter_st = 0
    aile = 0
    rud = 0
    dis = 0
    wpindex = 0
    cross_track = 0
    
    end_runway_lat =  37.6254018
    end_runway_lon =  -122.385271
    head_runway_lat = 37.628715674334124
    head_runway_lon =-122.39334575867426
    yaw_deg_set = 117

    wp = waypoint.wayPoint()
    wp.addWaypoint('to',head_runway_lat,head_runway_lon,0)
    wp.addWaypoint('wp',head_runway_lat,head_runway_lon + 0.04,0)
    wp.addWaypoint('wp',head_runway_lat + 0.04,head_runway_lon + 0.04,0)
    wp.addWaypoint('wp',head_runway_lat + 0.04,head_runway_lon,0)

    ttt = time.time()
    while wd.isRun():
        recvAtitude = fdm_event_pipe.parent_recv() 
        if  time.time() - timer > 0.1:  # 10hz control
            timer = time.time()
            #############################################
            yaw_deg   = recvAtitude[2]
            latitude  = recvAtitude[3]
            longitude = recvAtitude[4]
            altitude  = recvAtitude[5]
            #yaw_command,dis = nav.cricleFlyMode1(recvAtitude[3],recvAtitude[4],head_runway_lat,head_runway_lon,1000)
            command = nav.navigationStart(latitude,longitude,wp)
            try:
                rud = command[0]
                dis = command[1]
                wpindex  = command[2]
                cross_track = command[3]
            except:
                pass
            
            if p2.poll():
                data = p2.recv()
                data = struct.unpack('ddd',data)
                roll_deg_set = data[0]
                pitch_deg_set = data[1]
                yaw_deg_set = data[2]
                #print(roll_deg_set,' ',pitch_deg_set,' ',yaw_deg_set)
            
            if altitude > 50: # 50 m
                loiter_st = 1
            else:
                rude = yaw.pidCalculate(yaw_deg,yaw_deg_set)
            if loiter_st == 1:
                aile = yaw.yawPid(yaw_deg,rud)
                aile = constranin(aile,-40,40)
                rude = 0
            #print(int(yaw_deg),'  ',int(yaw_command),'  ',int(dis))
            if time.time() - ttt > 1:
                ttt = time.time()
                print(int(yaw_deg),'  ',int(rud),'  ',int(dis),
                      '   ',int(cross_track),'  ',int(wpindex))
            
            wd.setAttitude(int(recvAtitude[0]),int(recvAtitude[1]),
                           int(recvAtitude[2]),int(recvAtitude[5]),
                                     recvAtitude[3],recvAtitude[4],
                                                   recvAtitude[7])
            aileron = roll.pidCalculate(recvAtitude[0],-aile)
            elevator = pitch.pidCalculate(recvAtitude[1],pitch_deg_set)
            ctrls_event_pipe.parent_send((aileron,elevator,rude,0,0)) 
            ctrls_event_pipe.clear() #important
    # stop all child process
    ctrls_conn.stop()
    fdm_conn.stop()
