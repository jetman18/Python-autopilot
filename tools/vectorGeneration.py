# Import the required libraries
from tkinter import *
import math
# Create an instance of tkinter frame or window
win=Tk()

# Set the size of the tkinter window
win.geometry("1200x1200")


def sign(x):
    k=0
    try:
        k =int(x/abs(x))
    except:
        k=0
    return k
# Create a canvas widget
canvas=Canvas(win, width=1000, height=600)
def vect(x,y,angle,color):
    angle +=90
    if angle > 359:
        angle -= 359
    
    angle_in_radians = angle * math.pi / 180
    line_length = 10
    center_x = x
    center_y = y
    end_x = center_x + line_length * math.cos(angle_in_radians)
    end_y = center_y + line_length * math.sin(angle_in_radians)
    canvas.create_oval(center_x -1,center_y -1 ,center_x +1,center_y +1,outline = color,fill = "white",width = 2)
    canvas.create_line(center_x,center_y,end_x,end_y, fill=color, width=2)

def test_case1():
    Kd = 0.5
    Kc =1
    pi2 = 90
    step = 20
    line_p1 = [300,300]
    line_p2 = [500,300]
    canvas.create_oval(line_p1[0]-3,line_p1[1]-3,line_p1[0]+3,line_p1[1]+3,outline = "black",fill = "white",width = 5)
    canvas.create_oval(line_p2[0]-3,line_p2[1]-3,line_p2[0]+3,line_p2[1]+3,outline = "black",fill = "white",width = 5)
    canvas.create_line(line_p1,line_p2, fill="black", width=2)
    for i in range(100,1000,step-5):
        for j in range(0,600,step-5):
            x = line_p1[0] - i
            y = line_p1[1] - j
            pi1 = math.atan2(y,x)
            pi1 = math.degrees(pi1) + 90
            Dct = j - line_p2[1]
            sigDct = sign(Dct)
            s = math.pow(abs(Dct*Kc*(pi1 - pi2)),Kd)*sigDct
            phi = 90 - s
            vect(i,j,phi,'blue')
    canvas.create_text(35,20, text='Kd: '+str(Kd), fill="black", font=('8'))
    canvas.create_text(35,45, text='Kc: '+str(Kc), fill="black", font=('8'))

def test_case2_loiter(radius):
    step = 20
    canvas.create_oval(500,300,502,302,outline = "black",fill = "white",width = 5)
    canvas.create_oval(500 - radius,300 - radius,500 + radius + 2,300 +radius + 2,outline = "black",width = 2)
    Kc =1
    for i in range(100,1000,step):
        for j in range(0,600,step-5):
            x = 501 - i
            y = 301 - j
            Dct = math.sqrt(x*x + y*y) - radius
            pi1 = math.atan2(y,x)
            pi1 = math.degrees(pi1) + 90 #- math.degrees(math.atan2(radius,Dct))
            
            sigDct = sign(Dct)
            phi = pi1 - 90 + min(abs(Dct*Kc),90)*sigDct
            vect(i,j,phi,'blue')
def test_folow_waypoint(radius):
    step = 20
    #canvas.create_oval(500,300,502,302,outline = "black",fill = "white",width = 5)
    
    wp1 = [500,300]
    canvas.create_line(500,300,700,300, fill="black", width=2)
    canvas.create_oval(500 - radius,300 - 2*radius,500 + radius,300,outline = "black",width = 2)
    canvas.create_oval(500 - radius,300,500 + radius,300 +2*radius,outline = "black",width = 2)
    Kc = 6
    Kd = 1
    pi2 = 90 # waypoint heading
    fisrtWp = False
    for j in range(0,600,step-4):
        for i in range(0,1000,step-1):
            col = 'blue'
            if fisrtWp == False:
                if j <= wp1[1]:
                    x = wp1[0] - i
                    y = wp1[1] - j - radius
                    pi1 = math.atan2(y,x)
                    Dct = math.sqrt(x*x + y*y) - radius
                    pi1 = math.degrees(pi1) + 90 + math.degrees(math.atan2(radius,Dct*Kc))
                elif j > wp1[1]:
                    x = wp1[0] - i
                    y = wp1[1] - j + radius
                    pi1 = math.atan2(y,x)
                    Dct = math.sqrt(x*x + y*y) - radius
                    pi1 = math.degrees(pi1) + 90 - math.degrees(math.atan2(radius,Dct*Kc))
                
                if (abs(j - wp1[1]) < 20) and (wp1[0] - i < 100) and (abs(pi1 - pi2) < 20):
                    col = 'red'
                    print(j,'  ',i,'  ',pi1)
                vect(i,j,pi1,col)
                    #cross 1st point
                    #fisrtWp = True
                    #wp1[0] = 700
                    #wp1[1] = 300
                    #print('1st wp')
            elif fisrtWp == True:
                pass


           
#test_case1()
#test_folow_waypoint(100)
test_case2_loiter(400)
canvas.pack()
win.mainloop()