from time import sleep


class Robot:
    def __init__(self, dc_motor_1, dc_motor_2):
        self.dc_motor_1 = dc_motor_1
        self.dc_motor_2 = dc_motor_2

    def forward(self, speed):
        self.speed = speed
        self.dc_motor_1.forward(speed)
        self.dc_motor_2.forward(speed)
        # sleep(1)
        # self.dc_motor_1.stop()
        # self.dc_motor_2.stop()

    def backward(self, speed):
        self.speed = speed
        self.dc_motor_1.backward(speed)
        self.dc_motor_2.backward(speed)
        # sleep(1)
        # self.dc_motor_1.stop()
        # self.dc_motor_2.stop()

    def rotate_left(self, speed):
        self.speed = speed
        self.dc_motor_1.forward(speed)
        self.dc_motor_2.backward(speed)
        # sleep(0.25)
        # self.dc_motor_1.stop()
        # self.dc_motor_2.stop()

    def rotate_right(self, speed):
        self.speed = speed
        self.dc_motor_1.backward(speed)
        self.dc_motor_2.forward(speed)
        # sleep(0.25)
        # self.dc_motor_1.stop()
        # self.dc_motor_2.stop()

    def stop(self):
        self.dc_motor_1.stop()
        self.dc_motor_2.stop()
