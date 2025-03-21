

class QVector3:
    roll:float
    pitch:float
    yaw:float

    def __init__(self, x=0, y=0, z=0):
        self.roll, self.pitch, self.yaw = x, y, z