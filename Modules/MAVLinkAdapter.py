from pymavlink import mavutil
from Modules import classes
import math

class Adapter:
    def __init__(self):
        self.connection = mavutil.mavlink_connection('udp:127.0.0.1:14550')
        

    def heartbeat(self):
        self.connection.wait_heartbeat()
        return True
    
    def get_current_heading(self):
        message = self.connection.recv_match(type='VFR_HUD', blocking=True)
        return message.heading
    
    def get_ratio(self):
        message = self.connection.recv_match(type='ATTITUDE', blocking=True)
        return classes.QVector3(roll=math.degrees(message.roll), pitch=math.degrees(message.pitch), yaw=math.degrees(message.yaw))
    
    def get_global(self):
        message = self.connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        return classes.Global_Position(alt=message.alt, relative_alt=message.relative_alt, vz=message.vz, vx=message.vx, vy=message.vy)
    
    def destroy(self):
        self.connection.close()