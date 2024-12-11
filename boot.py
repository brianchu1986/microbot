from machine import Pin, I2C, Timer, PWM
import sh1106
import random
from oled_emoji import OledEmoji
import time
from dcmotor import DCMotor
from robot import Robot

##### configure network #####
try:
    import usocket as socket
except:
    import socket

import network, usys
import esp
import ujson as json

esp.osdebug(None)

import gc

gc.collect()

with open("/config.json") as credentials_json:  # This open and read config file.
    config = json.loads(credentials_json.read())
ssid = config["WIFI_SSID"]
password = config["WIFI_PASSWORD"]


def do_connect(mode="STA_IF"):
    if mode == "STA_IF":
        ap = network.WLAN(network.STA_IF)
        ap.active(True)  # Activate the interface so you can use it.
        if ap.isconnected():
            ap.disconnect()
            print("started in the connected state, but now disconnected")
        else:  # Unless already connected, try to connect.
            print("connecting to network...")
        time.sleep(2)
        ap.connect(
            ssid, password
        )  # Connect to the station using credentials from the json file.
        if not ap.isconnected():
            print("Can't connect to network with given credentials.")
            usys.exit(
                0
            )  # This will programmatically break the execution of this script and return to shell.
    elif mode == "AP_IF":
        ap = network.WLAN(network.AP_IF)  # access point
        ap.config(essid=ssid, password=password)
        ap.active(True)  # Activate the interface so you can use it.

    print("Connection successful")
    print("network config:", ap.ifconfig())
    return ap


ap = do_connect(
    mode="AP_IF"
)  # mode can be "STA_IF" for station or "AP_IF" for access point


##### configure motor #####
frequency = 15000

pin1 = Pin(27, Pin.OUT)
pin2 = Pin(26, Pin.OUT)
enable_motor_1 = PWM(Pin(14), frequency)

pin3 = Pin(32, Pin.OUT)
pin4 = Pin(33, Pin.OUT)
enable_motor_2 = PWM(Pin(25), frequency)

dc_motor_1 = DCMotor(pin1, pin2, enable_motor_1)
dc_motor_2 = DCMotor(pin3, pin4, enable_motor_2)

robot = Robot(dc_motor_1, dc_motor_2)
speed = 50

##### configure oled #####
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
x = 0
y = 0
u = 1
m = 1
oled_width = 128
oled_height = 64
oled = sh1106.SH1106_I2C(oled_width, oled_height, i2c)
oled.flip()

eye_width = 40
eye_height = 40
eye1_x_start = 59
eye2_x_start = 69
eye_y_end = 52
border_radius = 3

emoji = OledEmoji(
    oled, eye_width, eye_height, eye1_x_start, eye2_x_start, eye_y_end, border_radius
)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 80))
s.listen(5)

period = 2000
blink_timer_1 = Timer(1)
blink_eyes = False


def stop_blink_eyes():
    global blink_eyes
    blink_timer_1.deinit()
    blink_eyes = False


def start_blink_eyes():
    global blink_eyes
    blink_timer_1.init(period=period, mode=Timer.PERIODIC, callback=emoji.blink_eyes)
    blink_eyes = True


##### start display ######
oled.text("Micro:Bot", 30, 0, 1)
oled.text(ssid, 1, 24, 1)
oled.text("waiting for", 1, 34, 1)
oled.text("connection:", 1, 44, 1)
oled.text(ap.ifconfig()[0], 1, 54, 1)
oled.show()

try:
    while True:
        conn, addr = s.accept()
        print("Got a connection from %s" % str(addr))
        raw_request = conn.recv(1024)
        request = str(raw_request)
        print("Content = %s" % request)
        req = raw_request.decode("utf8")
        request_method, route = req.split(" ")[:2]
        print(request_method, route)  # ["GET", "/"]

        if route == "/?speed=slow":
            print("speed_slow")
            speed = 25
            emoji.sleep()
        elif route == "/?speed=normal":
            print("speed_normal")
            speed = 50
            emoji.happy()
        elif route == "/?speed=fast":
            print("speed_fast")
            speed = 100
            emoji.sad()
        elif route == "/?move=forward":
            print("move_forward")
            robot.forward(speed)
            if blink_eyes:
                stop_blink_eyes()
            emoji.smile()
        elif route == "/?move=backward":
            print("move_backward")
            robot.backward(speed)
            if blink_eyes:
                stop_blink_eyes()
            emoji.small_eyes()
        elif route == "/?move=left":
            print("move_left")
            robot.rotate_left(speed)
            if blink_eyes:
                stop_blink_eyes()
            emoji.left_small_eye()
        elif route == "/?move=right":
            print("move_right")
            robot.rotate_right(speed)
            if blink_eyes:
                stop_blink_eyes()
            emoji.right_small_eye()
        elif route == "/?move=stop":
            print("stop")
            robot.stop()
            if not blink_eyes:
                start_blink_eyes()
        conn.send("HTTP/1.1 200 OK\n")

        if route == "/":
            conn.send("Content-Type: text/html\n")
            conn.send("Connection: close\n\n")
            f = open("./static/index.html", "rb").read()
        elif ".js" in route:
            conn.send(b"Content-Type: text/javascript\n\n")
            filename = "." + route
            print(filename)
            f = open(filename, "rb").read()
        elif ".css" in route:
            conn.send(b"Content-Type: text/css\n\n")
            filename = "." + route
            print(filename)
            f = open(filename, "rb").read()
        conn.sendall(f)
        conn.close()
except KeyboardInterrupt:
    blink_timer_1.deinit()
    oled.fill(0)
