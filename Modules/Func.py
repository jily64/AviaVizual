from Modules import classes
import math

def get_current_ratio() -> classes.QVector3:
    return classes.QVector3()

def rotate_point(center, point, angle):
    cx, cy = center
    px, py = point

    s = math.sin(math.radians(angle))
    c = math.cos(math.radians(angle))

    x_new = c * (px - cx) - s * (py - cy) + cx
    y_new = s * (px - cx) + c * (py - cy) + cy

    return x_new, y_new

def count_speed_module(vx, vy):
    return round(abs(math.sqrt(vx**2 + vy**2)), 2)



def calculate_height_from_pressure(app, P_ground, P_height, T=288.15, L=0.0065, R=8.31447, g=9.80665, M=0.0289644):
    # Преобразуем давление из гПа в Па
    P_ground = P_ground * 100
    P_height = P_height * 100
    
    # Вычисляем высоту по барометрической формуле
    exponent = (R * L) / (g * M)
    height = (T / L) * (1 - (P_height / P_ground) ** exponent)
    
    return round(height, 2)