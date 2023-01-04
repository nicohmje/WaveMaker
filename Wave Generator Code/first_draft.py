from dynamixel_sdk import *
import time

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

#1 = velocity and 3 = position 
dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL1_ID, 11, 3)
dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL2_ID, 11, 3)

#Torque enable
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL1_ID, 64, 1)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL2_ID, 64, 1)

#LED enable
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL1_ID, 65, 1)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL2_ID, 65, 1)

time.sleep(2)
i=1
while i<3:
#Read position
    pos1, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL1_ID, 132)
    pos2, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL2_ID, 132)
    print("pos 1:", pos1, "pos 2:", pos2 )
    i = i + 1 
    time.sleep(1)

#Give position
dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL1_ID, 116, 1560)
dxl_comm_result, dxl_error = packetHandler.4ByteTxRx(portHandler, DXL2_ID, 116, 2326)

time.sleep(3)

dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL1_ID, 116, 3032)
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL2_ID, 116, 854)

time.sleep(3)

dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL1_ID, 104, 0)
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL2_ID, 104, 0)


dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL1_ID, 64, 0)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL2_ID, 64, 0)



