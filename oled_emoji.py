from machine import Pin, I2C, Timer
import sh1106
import random


class OledEmoji:
    def __init__(
        self,
        oled,
        eye_width=40,
        eye_height=40,
        eye1_x_start=59,
        eye2_x_start=69,
        eye_y_end=52,
        border_radius=3,
    ):
        self.oled = oled
        self.eye_width = eye_width
        self.eye_height = eye_height
        self.eye1_x_start = eye1_x_start
        self.eye2_x_start = eye2_x_start
        self.eye_y_end = eye_y_end
        self.border_radius = border_radius

    def add_border_radius(self, side, eye_width, eye_height):
        if side == "left":
            # top left
            self.oled.hline(
                self.eye1_x_start - eye_width,
                self.eye_y_end - eye_height,
                self.border_radius,
                0,
            )
            self.oled.vline(
                self.eye1_x_start - eye_width,
                self.eye_y_end - eye_height,
                self.border_radius,
                0,
            )
            # top right
            self.oled.hline(
                self.eye1_x_start - self.border_radius,
                self.eye_y_end - eye_height,
                self.border_radius,
                0,
            )
            self.oled.vline(
                self.eye1_x_start - 1,
                self.eye_y_end - eye_height,
                self.border_radius,
                0,
            )
            # bottom left
            self.oled.hline(
                self.eye1_x_start - eye_width, self.eye_y_end - 1, self.border_radius, 0
            )
            self.oled.vline(
                self.eye1_x_start - eye_width,
                self.eye_y_end - self.border_radius,
                self.border_radius,
                0,
            )
            # bottom right
            self.oled.hline(
                self.eye1_x_start - self.border_radius,
                self.eye_y_end - 1,
                self.border_radius,
                0,
            )
            self.oled.vline(
                self.eye1_x_start - 1,
                self.eye_y_end - self.border_radius,
                self.border_radius,
                0,
            )
        elif side == "right":
            # top left
            self.oled.hline(
                self.eye2_x_start, self.eye_y_end - eye_height, self.border_radius, 0
            )
            self.oled.vline(
                self.eye2_x_start, self.eye_y_end - eye_height, self.border_radius, 0
            )
            # top right
            self.oled.hline(
                self.eye2_x_start + eye_width - self.border_radius,
                self.eye_y_end - eye_height,
                self.border_radius,
                0,
            )
            self.oled.vline(
                self.eye2_x_start + eye_width - 1,
                self.eye_y_end - eye_height,
                self.border_radius,
                0,
            )
            # bottom left
            self.oled.hline(
                self.eye2_x_start, self.eye_y_end - 1, self.border_radius, 0
            )
            self.oled.vline(
                self.eye2_x_start,
                self.eye_y_end - self.border_radius,
                self.border_radius,
                0,
            )
            # bottom right
            self.oled.hline(
                self.eye2_x_start + eye_width - self.border_radius,
                self.eye_y_end - 1,
                self.border_radius,
                0,
            )
            self.oled.vline(
                self.eye2_x_start + eye_width - 1,
                self.eye_y_end - self.border_radius,
                self.border_radius,
                0,
            )

    def normal_eye(self, side):
        if side == "left":
            self.oled.fill_rect(
                self.eye1_x_start - self.eye_width,
                self.eye_y_end - self.eye_height,
                self.eye_width,
                self.eye_height,
                1,
            )
            self.add_border_radius(side, self.eye_width, self.eye_height)
        elif side == "right":
            self.oled.fill_rect(
                self.eye2_x_start,
                self.eye_y_end - self.eye_height,
                self.eye_width,
                self.eye_height,
                1,
            )
            self.add_border_radius(side, self.eye_width, self.eye_height)

    def small_eye(self, side, scale):
        new_width = int(round(self.eye_width * scale, 0))
        new_height = int(round(self.eye_height * scale, 0))
        if side == "left":
            self.oled.fill_rect(
                self.eye1_x_start - new_width,
                self.eye_y_end - new_height,
                new_width,
                new_height,
                1,
            )
            self.add_border_radius(side, new_width, new_height)
        elif side == "right":
            self.oled.fill_rect(
                self.eye2_x_start, self.eye_y_end - new_height, new_width, new_height, 1
            )
            self.add_border_radius(side, new_width, new_height)

    def long_eye(self, side, scale):
        new_height = int(round(self.eye_height * scale, 0))
        if side == "left":
            self.oled.fill_rect(
                self.eye1_x_start - self.eye_width,
                self.eye_y_end - new_height,
                self.eye_width,
                new_height,
                1,
            )
            self.add_border_radius(side, self.eye_width, new_height)
        elif side == "right":
            self.oled.fill_rect(
                self.eye2_x_start,
                self.eye_y_end - new_height,
                self.eye_width,
                new_height,
                1,
            )
            self.add_border_radius(side, self.eye_width, new_height)

    def half_eye(self, side, up_down):
        new_height = int(round(self.eye_height / 2, 0))
        self.normal_eye(side)
        if side == "left":
            if up_down == "up":
                self.oled.fill_rect(
                    self.eye1_x_start - self.eye_width,
                    self.eye_y_end - new_height,
                    self.eye_width,
                    new_height,
                    0,
                )
            elif up_down == "down":
                self.oled.fill_rect(
                    self.eye1_x_start - self.eye_width,
                    self.eye_y_end - self.eye_height,
                    self.eye_width,
                    new_height,
                    0,
                )
        elif side == "right":
            if up_down == "up":
                self.oled.fill_rect(
                    self.eye2_x_start,
                    self.eye_y_end - new_height,
                    self.eye_width,
                    new_height,
                    0,
                )
            elif up_down == "down":
                self.oled.fill_rect(
                    self.eye2_x_start,
                    self.eye_y_end - self.eye_height,
                    self.eye_width,
                    new_height,
                    0,
                )

    def smile_eye(self, side):
        eye1_center = 39, 32
        eye2_center = 89, 32
        eye_out_radius = 20, 20
        if side == "left":
            self.oled.ellipse(
                eye1_center[0],
                eye1_center[1],
                eye_out_radius[0],
                eye_out_radius[1],
                1,
                True,
            )
            self.oled.fill_rect(
                eye1_center[0] - eye_out_radius[0],
                eye1_center[1],
                eye_out_radius[0] * 3,
                eye_out_radius[1] * 2,
                0,
            )
            self.oled.ellipse(
                eye1_center[0],
                eye1_center[1],
                eye_out_radius[0],
                int(round(eye_out_radius[1] / 2, 0)),
                0,
                True,
            )
        elif side == "right":
            self.oled.ellipse(
                eye2_center[0],
                eye2_center[1],
                eye_out_radius[0],
                eye_out_radius[1],
                1,
                True,
            )
            self.oled.fill_rect(
                eye2_center[0] - eye_out_radius[0],
                eye2_center[1],
                eye_out_radius[0] * 3,
                eye_out_radius[1] * 2,
                0,
            )
            self.oled.ellipse(
                eye2_center[0],
                eye2_center[1],
                eye_out_radius[0],
                int(round(eye_out_radius[1] / 2, 0)),
                0,
                True,
            )

    def blink_eye(self, side, action):
        print(f"{side}=>{action}")
        # if (action % 2) == 0:
        if action == 0 or action == 1:
            self.small_eye(side, 0.8)
        else:
            self.normal_eye(side)

    def smile(self):
        self.oled.fill(0)
        self.smile_eye("left")
        self.smile_eye("right")
        self.oled.show()

    def sleep(self):
        self.oled.fill(0)
        self.long_eye("left", 0.3)
        self.long_eye("right", 0.3)
        self.oled.show()

    def sad(self):
        self.oled.fill(0)
        self.half_eye("left", "down")
        self.half_eye("right", "down")
        self.oled.show()

    def happy(self):
        self.oled.fill(0)
        self.half_eye("left", "up")
        self.half_eye("right", "up")
        self.oled.show()

    def left_small_eye(self):
        self.oled.fill(0)
        self.small_eye("left", 0.8)
        self.normal_eye("right")
        self.oled.show()

    def right_small_eye(self):
        self.oled.fill(0)
        self.normal_eye("left")
        self.small_eye("right", 0.8)
        self.oled.show()

    def small_eyes(self):
        self.oled.fill(0)
        self.small_eye("left", 0.8)
        self.small_eye("right", 0.8)
        self.oled.show()

    def blink_eyes(self, event):
        actions = 4
        action_left = random.randint(0, actions)
        action_right = random.randint(0, actions)
        self.oled.fill(0)

        if action_left != action_right:
            self.blink_eye("left", action_left)
            self.blink_eye("right", action_right)
        elif action_left == action_right and action_left == 2:
            self.sleep()
        elif action_left == action_right and action_left == 3:
            self.happy()
        elif action_left == action_right and action_left == 4:
            self.sad()
        else:
            self.smile()

        # half_eye("right","up")
        # normal_eye("left")
        # normal_eye("right")
        # small_eye("left",0.8)
        # small_eye("right",0.8)
        # long_eye("left",0.3)
        # long_eye("right",0.3)
        self.oled.show()
