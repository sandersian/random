#!/usr/bin/env python

from lightify import Lightify

lightify = Lightify("10.1.210.195")
lightify.update_all_light_status()
lights = lightify.lights()
if (lights[8984750156480241920].on() == 0):
    lights[8984750156480241920].set_onoff(True)
elif (lights[8984750156480241920].on() == 1):
    lights[8984750156480241920].set_onoff(False)