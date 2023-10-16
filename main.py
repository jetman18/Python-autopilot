"""
Start FlightGear with:
`fgfs --native-fdm=socket,out,30,localhost,5501,udp --native-ctrls=socket,out,30,localhost,5503,udp --native-ctrls=socket,in,30,localhost,5504,udp --aircraft=sf260`
"""

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
    ctrls_data.rudder =   rud_ctrl
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


    ctrls_conn.start()  # Start the Ctrls RX/TX loop
    fdm_conn.start()  # Start the FDM RX loop0
    ##### END INIT #######################
    # roll kd= 0.01 
    roll = pidcontroller.PID(0.1,0.1,0.001) # 0,02  0.002
    pitch = pidcontroller.PID(0.02,0,0)
    yaw = pidcontroller.PID(0.5,0,0)


    roll_deg_set = 0
    pitch_deg_set = 23
    yaw_deg_set = 250

    recvAtitude=[]
    navigator = navigation.NAV()
    yaw_loiter = navigation.anglextrame()
    yaw_aircraft = navigation.anglextrame()
    pp,ppp = mp.Pipe()
    wd = window(pp)
    timer = time.time()
    loiter_st = 0
    rudder = 0
    tt=0
    while wd.isRun():
        recvAtitude = fdm_event_pipe.parent_recv() 
        if  time.time() - timer > 0.1:  # 10hz command send
            timer = time.time()
            
            #############################################
            yaw_deg = recvAtitude[2]
            yaw_command,dis = navigator.cricleFly(recvAtitude[3],recvAtitude[4],
                                    63.94846441361346,
                                    -22.605470890274642,
                                    1000)
            if ppp.poll():
                data = ppp.recv()
                data = struct.unpack('ddd',data)
                roll_deg_set = data[0]
                pitch_deg_set = data[1]
                yaw_deg_set = data[2]
                print(roll_deg_set,' ',pitch_deg_set,' ',yaw_deg_set)
            ################PID##############################
            
            if recvAtitude[5]>100:
                loiter_st = 1
            if loiter_st == 1:
                rudder = yaw.pidCalculate(yaw_deg,yaw_command)
                if rudder > 50:
                    rudder = 50
                elif rudder <-50:
                    rudder = -50
                #print(yaw_deg,'  ',  yaw_command)
                if rudder > 70:
                    rudder = 70
                elif rudder <-70:
                    rudder = -70
            if time.time() -  tt > 1:
                #print(recvAtitude[3],' ',recvAtitude[4])
                tt = time.time()
            #print(int(yaw_deg),'  ',int(yaw_command),'  ',int(dis))
            aileron = roll.pidCalculate(recvAtitude[0],-rudder)
            elevator = pitch.pidCalculate(recvAtitude[1],pitch_deg_set)
            #rude = yaw.pidCalculate(yaw_deg,yaw_deg_set)
            wd.setAttitude(int(recvAtitude[0]),int(recvAtitude[1]),
                           int(recvAtitude[2]),int(recvAtitude[5]),
                           recvAtitude[3],recvAtitude[4],
                           recvAtitude[7])
            ctrls_event_pipe.parent_send((aileron,elevator,0,0,0)) 
    ctrls_conn.stop()
    fdm_conn.stop()



#  328.96319338294563   328.96319338294563   1018.2682297300826
#  291.65909838626055   651.6590983862606   1036.8912239792962