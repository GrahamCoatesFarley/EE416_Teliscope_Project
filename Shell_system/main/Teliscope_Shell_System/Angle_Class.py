class Angles(object):
    def __init__(self, h_angle, v_angle):
        self.__h_angle = h_angle
        self.__v_angle = v_angle
        self.__h_motor_data = 0
        self.__v_motor_data = 0

    # Creates empty class 
    def __init__(self):
        self.__h_angle = 0
        self.__v_angle = 0
        self.__h_motor_data = 0
        self.__v_motor_data = 0


    # Get and set angle functions
    def getVAngle(self):
        return self.__v_angle

    def getHAngle(self):
        return self.__h_angle
        
    def setHAngle(self, H_Angle):
        self.__h_angle = H_Angle

    def setVAngle(self, V_Angle):
        self.__v_angle = V_Angle

    # Get and set motor data functions
    def getVMotorData(self):
        return self.__v_motor_data

    def getHMotorData(self):
        return self.__h_motor_data
        
    def setHMotorData(self, H_Data):
        self.__h_motor_data = H_Data

    def setVMotorData(self, V_data):
        self.__v_motor_data = V_data

