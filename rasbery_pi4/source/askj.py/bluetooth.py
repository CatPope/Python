import serial
import RPi.GPIO as GPIO
import time
import random

# Bluetooth 시리얼 포트 설정
BTSerial = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)

# GPIO 핀 설정
TrigPin = 17
EchoPin = 18
Motor1A = 27
Motor1B = 22
Motor2A = 23
Motor2B = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(TrigPin, GPIO.OUT)
GPIO.setup(EchoPin, GPIO.IN)
GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor2A, GPIO.OUT)
GPIO.setup(Motor2B, GPIO.OUT)

# 전역 변수 설정
speedSet = 170
bt = ' '

def setup():
    stop_motor()

def loop():
    global bt
    if bt == 'f':
        go_motor()
    elif bt == 'b':
        back_motor()
    elif bt == 'r':
        right_motor()
    elif bt == 'l':
        left_motor()
    elif bt == 's':
        stop_motor()

def go_motor():
    GPIO.output(Motor1A, GPIO.HIGH)
    GPIO.output(Motor1B, GPIO.LOW)
    GPIO.output(Motor2A, GPIO.HIGH)
    GPIO.output(Motor2B, GPIO.LOW)

def back_motor():
    GPIO.output(Motor1A, GPIO.LOW)
    GPIO.output(Motor1B, GPIO.HIGH)
    GPIO.output(Motor2A, GPIO.LOW)
    GPIO.output(Motor2B, GPIO.HIGH)

def right_motor():
    GPIO.output(Motor1A, GPIO.HIGH)
    GPIO.output(Motor1B, GPIO.LOW)
    GPIO.output(Motor2A, GPIO.LOW)
    GPIO.output(Motor2B, GPIO.HIGH)

def left_motor():
    GPIO.output(Motor1A, GPIO.LOW)
    GPIO.output(Motor1B, GPIO.HIGH)
    GPIO.output(Motor2A, GPIO.HIGH)
    GPIO.output(Motor2B, GPIO.LOW)

def stop_motor():
    GPIO.output(Motor1A, GPIO.LOW)
    GPIO.output(Motor1B, GPIO.LOW)
    GPIO.output(Motor2A, GPIO.LOW)
    GPIO.output(Motor2B, GPIO.LOW)

if __name__ == '__main__':
    setup()
    try:
        while True:
            loop()
    except KeyboardInterrupt:
        GPIO.cleanup()
