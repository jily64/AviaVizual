from pymavlink import mavutil
from Modules import classes
import math

class Adapter:
    def __init__(self):
        self.connection = mavutil.mavlink_connection('udp:192.168.4.1:14555', baud=921600)
        self.heartbeat()
        self.arm_diarm()

    def heartbeat(self):
        self.connection.wait_heartbeat()
        return True
    
    def arm_diarm(self):
        self.connection.mav.command_long_send(
        self.connection.target_system,  # ID системы
        self.connection.target_component,  # ID компонента
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,  # Команда ARM
        0,  # Подтверждение
        1,  # Параметр 1: 1 для ARM
        0,  # Параметр 2: 0 для силы
        0, 0, 0, 0, 0  # Остальные параметры
        )
    
    def get_current_heading(self):
        message = self.connection.recv_match(type='VFR_HUD', blocking=True)
        return message.heading
    
    def get_ratio(self):
        message = self.connection.recv_match(type='ATTITUDE', blocking=True)
        return classes.QVector3(roll=math.degrees(message.roll), pitch=math.degrees(message.pitch), yaw=math.degrees(message.yaw))
    
    def get_global(self):
        message = self.connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        return classes.Global_Position(alt=message.alt, relative_alt=message.relative_alt, vz=message.vz, vx=message.vx, vy=message.vy)
    
    def get_pressure(self):
        message = self.connection.recv_match(type='SCALED_PRESSURE', blocking=True)
        return message.press_abs

    def destroy(self):
        self.connection.close()