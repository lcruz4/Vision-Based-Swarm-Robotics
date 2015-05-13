#!/usr/bin/python

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import time

# Right side motors. Pin definitions for H-bridge control
rf_e = "P8_13"  # controls speed of right front motor via PWM
rb_e = "P8_19"  # controls speed of right rear motor via PWM

# Left side motors. Pin definitions for H-bridge control
lf_e = "P9_16"  # controls speed of left front motor via PWM
lb_e = "P9_14"  # controls speed of left rear motor via PWM

led = "P8_8"
# set pin directions as output

GPIO.setup(led,GPIO.OUT)
GPIO.output(led,GPIO.LOW)
PWM.start(rf_e, 0)
PWM.start(rb_e, 0)
PWM.start(lf_e, 0)
PWM.start(lb_e, 0)

def ledOn():
  GPIO.output(led,GPIO.HIGH)

def ledOff():
  GPIO.output(led,GPIO.LOW)

def forward(vel):
	PWM.set_duty_cycle(rf_e, vel-1)
	PWM.set_duty_cycle(rb_e, 0)
	PWM.set_duty_cycle(lf_e, vel)
	PWM.set_duty_cycle(lb_e, 0)
def backward(vel):
	PWM.set_duty_cycle(rf_e, 0)
	PWM.set_duty_cycle(rb_e, vel)
	PWM.set_duty_cycle(lf_e, 0)
	PWM.set_duty_cycle(lb_e, vel)
def spin_left(vel):
	PWM.set_duty_cycle(rf_e, 0)
	PWM.set_duty_cycle(rb_e, vel)
	PWM.set_duty_cycle(lf_e, vel)
	PWM.set_duty_cycle(lb_e, 0)
def spin_right(vel):
	PWM.set_duty_cycle(rf_e, vel)
	PWM.set_duty_cycle(rb_e, 0)
	PWM.set_duty_cycle(lf_e, 0)
	PWM.set_duty_cycle(lb_e, vel)
def stop():
	PWM.set_duty_cycle(rf_e, 0)
	PWM.set_duty_cycle(rb_e, 0)
	PWM.set_duty_cycle(lf_e, 0)
	PWM.set_duty_cycle(lb_e, 0)
def clean():
	PWM.stop(rf_e)
	PWM.stop(rb_e)
	PWM.stop(lf_e)
	PWM.stop(lb_e)
	PWM.cleanup()
        GPIO.cleanup()

