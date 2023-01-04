import tkinter as tk
from tkinter import ttk
from dynamixel_sdk import *
import time
import numpy as np 

# Control table address
ADDR_PRO_TORQUE_ENABLE      = 64               # Control table address is different in Dynamixel model
ADDR_PRO_LED_RED            = 65
ADDR_PRO_GOAL_POSITION      = 116
ADDR_PRO_PRESENT_POSITION   = 132

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
DEVICENAME                  = '/dev/tty.usbserial-FT6Z5R6J'    # Check which port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1                # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque
DXL_MINIMUM_POSITION_VALUE  = 100           # Dynamixel will rotate between this value
DXL_MAXIMUM_POSITION_VALUE  = 4000            # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_MOVING_STATUS_THRESHOLD = 20 

portHandler = PortHandler(DEVICENAME)

packetHandler = PacketHandler(PROTOCOL_VERSION)

if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    quit()

if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    quit()


#Torque off 
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL1_ID, 64, 0)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL2_ID, 64, 0)


dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL1_ID, 11, 3)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL2_ID, 11, 3)


dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL1_ID, 64, 1)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL2_ID, 64, 1)




# root window
root = tk.Tk()
root.geometry('300x200')
root.resizable(False, False)
root.title('Wave Generator')


root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)

# slider current value
omega = tk.DoubleVar()


# label for the slider
slider1_label = ttk.Label(
    root,
    text='omega'
)

slider1_label.grid(
    column=0,
    row=0,
    sticky='we'
)

# slider current value
theta = tk.DoubleVar()


# label for the slider
slider2_label = ttk.Label(
    root,
    text='theta'
)

slider2_label.grid(
    column=0,
    row=1,
    sticky='we'
)

# label for the slider
slider3_label = ttk.Label(
    root,
    text='theta2'
)

slider3_label.grid(
    column=0,
    row=6,
    sticky='we'
)

# label for the slider
delay_label = ttk.Label(
    root,
    text='delay'
)

delay_label.grid(
    column=0,
    row=2,
    sticky='we'
)

number_label = ttk.Label(
    root,
    text='number'
)

number_label.grid(
    column=0,
    row=3,
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
    row = 2,
    sticky='we'
)

wave_number.grid(
    column = 1,
    row = 3,
    sticky='we'
)

slider1 = ttk.Scale(
    root,
    from_=1,
    to=4095,
    orient='horizontal',  # vertical
    variable=omega
)



slider1.set(100)

slider1.grid(
    column=1,
    row=0,
    sticky='we'
)

slider2 = ttk.Entry(
    root,
)

slider2.grid(
    column=1,
    row=1,
    sticky='we'
)

theta2 = tk.DoubleVar()
slider3 = ttk.Entry(
    root,

)

slider3.grid(
    column=1,
    row=6,
    sticky='we'
)

bwave = tk.StringVar()

big_wave = ttk.Checkbutton(
    root,
    text="big wave?",
    variable=bwave
)

bwave.set(0)

big_wave.grid(
    column=1,
    row=5,
    sticky='we'
)

wave_delay.insert("end",'0')
wave_number.insert("end", '1')


def launch_wave(): 
    num = int(wave_number.get())
    delay = int(wave_delay.get())
    omega = int(slider1.get())
    theta = float(slider2.get())

    #Profile Velocity 
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL1_ID, 112, 200)

    goal_pos = 3072 - int((2048. / np.pi) * theta)
    bottom_pos = 1048+ int((2048. / np.pi) * float(slider3.get()))


    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL1_ID, 116, goal_pos)
    pos = 0
    count = 0 
    while pos < goal_pos - 50  and (count < 1000): 
        pos, result, error = packetHandler.read4ByteTxRx(portHandler, DXL2_ID, 132)
        print(pos)
        count = count + 1

    time.sleep(1)
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL1_ID, 112, omega)

    #Position = 2048 * 2 
    #3072 = top <-> 1048 = bottom
    print(goal_pos)
    print("slider", float(slider2.get()))
    print("theta", theta)

    print(bwave.get())
    i = 1
    while i <= num:
        move_motors(goal_pos, bottom_pos,i)
        time.sleep(delay)
        print("delay", delay)
        i = i + 1

    if int(bwave.get()) == 1:
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL1_ID, 112, 600)
        move_motors(3072, 1048, i) 
        print("BIG WAVE")

    time.sleep(2)
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL1_ID, 116, 3072)

    



def move_motors(goal_pos, bottom_pos, i):
    
    if goal_pos < bottom_pos:
        quit()
    print("john")
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL1_ID, 116, goal_pos)

    pos = 0
    count = 0 
    while pos < goal_pos - 80  and (count < 100): 
        pos, result, error = packetHandler.read4ByteTxRx(portHandler, DXL2_ID, 132)
        print(goal_pos, pos, count)
        count = count + 1


    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL1_ID, 116, bottom_pos)

    pos = 5000 
    count = 0 
    while (pos > bottom_pos + 80) and (count < 100): 
        pos, result, error = packetHandler.read4ByteTxRx(portHandler, DXL2_ID, 132)
        print(bottom_pos, pos, count)
        count = count + 1






launch_button = ttk.Button(
    root,
    text="launch",
    command=launch_wave,
)

launch_button.grid(
    column=1,
    row=4,
    sticky='we'
)



root.mainloop()



