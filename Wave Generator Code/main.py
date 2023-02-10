import tkinter as tk
from tkinter import ttk
from dynamixel_sdk import *
import time
import os
import numpy as np 

# Control table address
ADDR_PRO_TORQUE_ENABLE      = 64               # Control table address is different in Dynamixel model
ADDR_PRO_LED_RED            = 65
ADDR_PRO_GOAL_POSITION      = 116
ADDR_PRO_PRESENT_POSITION   = 132
ADDR_PRO_PROFILE_VELOCITY   = 112

# Data Byte Length
LEN_PRO_LED_RED             = 1
LEN_PRO_GOAL_POSITION       = 4
LEN_PRO_PRESENT_POSITION    = 4

# Protocol version
PROTOCOL_VERSION            = 2.0               # See which protocol version is used in the Dynamixel

# Default setting
DXL1_ID                     = 1                 # Dynamixel#1 ID : 1
DXL2_ID                     = 2                # Dynamixel#1 ID : 2
BAUDRATE                    = 57600             # Dynamixel default baudrate : 57600
DEVICENAME                  = '/dev/tty.usbserial-FT763MZ5'    # Check which port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1                # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque
DXL_MINIMUM_POSITION_VALUE  = 100           # Dynamixel will rotate between this value
DXL_MAXIMUM_POSITION_VALUE  = 4000            # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_MOVING_STATUS_THRESHOLD = 20 


os.system("clear")

print("-------------WAVE GENERATOR INTEFACE-------------")
print("|                                               |")
print("|                                               |")
print("|           Created by Nicolas Hammje           |")
print("|                                               |")
print("|                                               |")
print("|             www.nicolashammje.com             |")
print("|                                               |")
print("|              me@nicolashammje.com             |")
print("|                                               |")
print("|                                               |")
print("-------------------------------------------------")
print(" ")
print(" ")
print("Use the GUI to interface with the wave generator")
print("Output will be printed below this line:")


portHandler = PortHandler(DEVICENAME)

packetHandler = PacketHandler(PROTOCOL_VERSION)

if portHandler.openPort():
    print("[INFO] Succeeded to open the port")
else:
    print("[ERROR] Failed to open the port")
    quit()

if portHandler.setBaudRate(BAUDRATE):
    print("[INFO] Succeeded to change the baudrate")
else:
    print("[ERROR] Failed to change the baudrate")
    quit()


#Torque off 
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL1_ID, ADDR_PRO_TORQUE_ENABLE, 0)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL2_ID, ADDR_PRO_TORQUE_ENABLE, 0)

#Operating mode : position
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL1_ID, 11, 3)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL2_ID, 11, 3)

#Torque on
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL1_ID, ADDR_PRO_TORQUE_ENABLE, 1)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL2_ID, ADDR_PRO_TORQUE_ENABLE, 1)




# root window
root = tk.Tk()
root.geometry('400x200')
root.resizable(False, False)
root.title('Wave Generator')


root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)

# slider current value
omega = tk.DoubleVar()


# label for the slider
speed_slider = ttk.Label(
    root,
    text='Speed'
)

speed_slider.grid(
    column=0,
    row=0,
    sticky='we'
)

# slider current value
theta = tk.DoubleVar()


# label for the slider
theta_slider_label = ttk.Label(
    root,
    text='Start angle (rad)'
)

theta_slider_label.grid(
    column=0,
    row=1,
    sticky='we'
)

# label for the slider
theta2_slider_label = ttk.Label(
    root,
    text='End angle (rad)'
)

theta2_slider_label.grid(
    column=0,
    row=2,
    sticky='we'
)

# label for the slider
delay_label = ttk.Label(
    root,
    text='Delay between waves (s)'
)

delay_label.grid(
    column=0,
    row=3,
    sticky='we'
)

number_label = ttk.Label(
    root,
    text='Number of waves'
)

number_label.grid(
    column=0,
    row=4,
    sticky='we'
)

wave_number = ttk.Entry(
    root,
    
)

wave_delay = ttk.Entry(
    root
)

wave_delay.grid(
    column = 1,
    row = 3,
    sticky='we'
)

wave_number.grid(
    column = 1,
    row = 4,
    sticky='we'
)

speed = ttk.Scale(
    root,
    from_=1,
    to=4095,
    orient='horizontal',  # vertical
    variable=omega
)



speed.set(100)

speed.grid(
    column=1,
    row=0,
    sticky='we'
)

theta_slider = ttk.Entry(
    root,
)

theta_slider.grid(
    column=1,
    row=1,
    sticky='we'
)

theta2 = tk.DoubleVar()
theta2_slider = ttk.Entry(
    root,

)

theta2_slider.grid(
    column=1,
    row=2,
    sticky='we'
)

bwave = tk.StringVar()

big_wave = ttk.Checkbutton(
    root,
    text="Add a big wave at the end?",
    variable=bwave
)

bwave.set(0)

big_wave.grid(
    column=1,
    row=6,
    sticky='we'
)

theta_slider.insert("end", "0")
theta2_slider.insert("end", "0")
wave_delay.insert("end",'0')
wave_number.insert("end", '1')

def check_angles():
    theta = float(theta_slider.get())
    theta2 = float(theta2_slider.get())

    goal_pos = 3072 - int((2048. / np.pi) * theta2) #Goal pos is straight down plus theta1
    top_pos = 1024+ int((2048. / np.pi) * theta) #Top pos is straight up minus theta2
    if goal_pos<top_pos:
        print("[ERROR] : User inputted angles are not valid. Please check that your units are radians, and that the start position is above the end position.")
        return
    if theta>2*np.pi:
        print("[ERROR] : Start angle is too big. Check that your units are radians")
        return  
    if theta2>2*np.pi:
        print("[ERROR] : End angle is too big. Check that your units are radians")
        return  
    launch_wave()


def launch_wave(): 
    num = int(wave_number.get())
    delay = int(wave_delay.get())
    omega = int(speed.get())
    theta = float(theta_slider.get())
    theta2 = float(theta2_slider.get())

    #Profile Velocity 
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL1_ID, ADDR_PRO_PROFILE_VELOCITY, 200)

    goal_pos = 3072 - int((2048. / np.pi) * theta2) #Goal pos is straight up minus theta1
    top_pos = 1024+ int((2048. / np.pi) * theta) #Bottom pos is straight down plus theta2

    print("[INFO] Moving to starting position ..")
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL1_ID, ADDR_PRO_GOAL_POSITION, top_pos)
    pos = 0
    count = 0 
    while pos < top_pos - 50  and (count < 1000): 
        pos, result, error = packetHandler.read4ByteTxRx(portHandler, DXL2_ID, ADDR_PRO_PRESENT_POSITION)
        #print(pos)
        count = count + 1

    time.sleep(1)
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL1_ID, ADDR_PRO_PROFILE_VELOCITY, omega)

    #Position = 2048 * 2 
    #3072 = top <-> 1024 = bottom
    print("[INFO] Moving from", (top_pos-1024)*(np.pi/2048), "to", (goal_pos-1024)*(np.pi/2048))
    print("[INFO] Start angle:", theta)
    print("[INFO] End angle:", theta2)

    if bwave.get():
        print("[INFO] Big wave is enabled")
    else:
        print("[INFO] Big wave is disabled")


    i = 1
    while i <= num: #Launch 'num' waves
        print("[INFO] Launching wave", i)
        completed = False
        failure, completed = move_motors(goal_pos, top_pos)
        while (completed == False):
            print("waiting")
            time.sleep(0.05)
        if (delay>0):
            print("[INFO] Delaying :", delay)
            time.sleep(delay)
        if (failure):
            print("[ERROR] : Failed to execute trajectory. Check theta1 and theta2 for possible errors.")
            return
        i = i + 1

    if int(bwave.get()) == 1: #Launch big wave if enabled
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL1_ID, ADDR_PRO_PROFILE_VELOCITY, 600)
        move_motors(3072, 1024) 
        print("[INFO] Launching Big wave")

    time.sleep(2) #After 2 seconds, go back to resting position which is at the top
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL1_ID, ADDR_PRO_PROFILE_VELOCITY, 200)
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL1_ID, ADDR_PRO_GOAL_POSITION, 1024)
    print("[INFO] Successfully launched", num, "wave.s")





    



def move_motors(goal_pos, top_pos):

    if (goal_pos < top_pos):
        print("[ERROR] : The bottom position is above the top position, can't move")
        return True, True

    #Move to top starting position
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL1_ID, ADDR_PRO_GOAL_POSITION, top_pos)

    pos = 5000
    count = 0 
    while (pos > (top_pos + 80))  and (count < 100): #Tolerance and loop limit
        pos, result, error = packetHandler.read4ByteTxRx(portHandler, DXL2_ID, ADDR_PRO_PRESENT_POSITION)
        
        #print(top_pos, pos, count)
        count = count + 1
        time.sleep(0.05)

    #Move to bottom
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL1_ID, ADDR_PRO_GOAL_POSITION, goal_pos)

    pos = 0 
    count = 0 
    while (pos < (goal_pos - 80)) and (count < 100): #Tolerance and loop limit
        pos, result, error = packetHandler.read4ByteTxRx(portHandler, DXL2_ID, ADDR_PRO_PRESENT_POSITION)
        #print(goal_pos, pos, count)
        count = count + 1
        time.sleep(0.05)
    return False, True






launch_button = ttk.Button(
    root,
    text="LAUNCH",
    command=check_angles,
)

launch_button.grid(
    column=1,
    row=5,
    sticky='we'
)



root.mainloop()


