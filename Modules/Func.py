from Modules import classes
import math

def get_current_ratio() -> classes.QVector3:
    return classes.QVector3()

def rotate_point(center, point, angle):
    cx, cy = center
    px, py = point

    # Поворачиваем точку
    s = math.sin(math.radians(angle))
    c = math.cos(math.radians(angle))

    # Новые координаты
    x_new = c * (px - cx) - s * (py - cy) + cx
    y_new = s * (px - cx) + c * (py - cy) + cy

    return x_new, y_new