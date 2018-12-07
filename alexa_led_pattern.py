#!/usr/bin/env python

# Copyright (C) 2017 Seeed Technology Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import numpy
import time


class AlexaLedPattern(object):
    def __init__(self, show=None, number=12):
        self.pixels_number = number
        self.pixels = [0] * 4 * number
	self.first = 3
	self.last= 47
	self.check = 1
	self.mutestatus = 0
	self.powerstatus = 0
        if not show or not callable(show):
            def dummy(data):
                pass
            show = dummy

        self.show = show
        self.stop = False

    def wakeup(self, direction=0):
        position = int((direction + 15) / (360 / self.pixels_number)) % self.pixels_number

        pixels = [0, 0, 0, 24] * self.pixels_number
        pixels[position * 4 + 2] = 48

        self.show(pixels)

    def listen(self):
        pixels = [0, 0, 0, 24] * self.pixels_number

        self.show(pixels)

    def think(self):
        pixels  = [0, 0, 12, 12, 0, 0, 0, 24] * self.pixels_number

        while not self.stop:
            self.show(pixels)
            time.sleep(0.2)
            pixels = pixels[-4:] + pixels[:-4]

    def speak(self):
        step = 1
        position = 12
        while not self.stop:
            pixels  = [0, 0, position, 24 - position] * self.pixels_number
            self.show(pixels)
            time.sleep(0.01)
            if position <= 0:
                step = 1
                time.sleep(0.4)
            elif position >= 12:
                step = -1
                time.sleep(0.4)

            position += step


    def brightness(self):
        step = 7
	total = 47
	pixels = [0, 0, 0, 0] * self.pixels_number
	pixels[3]= 10
 #       self.show(pixels)
 #       time.sleep(0.2)
        for i in range(0,5):

            self.show(pixels)
            pixels[step]=10
            pixels[total]=10
            step +=4
            total-=4
            time.sleep(0.2)

	for i in range(0,6):

            self.show(pixels)
            pixels[step]=0
            pixels[total]=0
            step -=4
            total+=4
            time.sleep(0.2)

    def volumeup(self):
	if self.first == 3:
		self.pixels[self.first]=10
		self.show(self.pixels)
		self.first+=4
	elif self.first <= 27 and self.last >= 27:
		self.pixels[self.first] = 10
		self.pixels[self.last] = 10
		self.first += 4
		self.last -= 4
		self.show(self.pixels)
	else:
		self.pixels = [0, 20, 0, 0] * 12
		self.show(self.pixels)
		time.sleep(0.1)
		self.pixels = [0, 0, 0, 10] * 12
		self.show(self.pixels)
		time.sleep(0.1)

    def volumedown(self):
	if self.first == 27 and self.last == 27 and self.check ==1:
		self.pixels[self.first] = 0
		#self.first -= 4
		#self.last += 4
		self.show(self.pixels)
		self.check = 0
	elif self.first >=11 and self.last <= 43:
		self.first -= 4
		self.last += 4
		self.pixels[self.first] = 0
		self.pixels[self.last] = 0
		self.show(self.pixels)
	else:
		self.pixels[1] = 20
		self.pixels[3] = 0
		self.show(self.pixels)
		time.sleep(0.1)
		self.pixels[1] = 0
		self.pixels[3] = 10
		self.show(self.pixels)
		time.sleep(0.1)

    def poweron(self):
	if self.powerstatus == 0:
		self.pixels = [0, 0, 0, 0] * 12
		redcount = 1
		bluecount = 3
		for i in range(0,12):
			self.pixels[redcount] = 15
			self.pixels[bluecount] = 15
			self.show(self.pixels)
			redcount+=4
			bluecount+=4
			time.sleep(0.05)
		redcount=1
		for i in range(0,12):
			self.pixels[redcount]=0
			self.show(self.pixels)
			redcount+=4
			time.sleep(0.05)
		redcount = 1
                bluecount = 3
                for i in range(0,12):
                        self.pixels[redcount]=0
                        self.pixels[bluecount]=0
                        self.show(self.pixels)
                        redcount+=4
			bluecount+=4
                        time.sleep(0.05)
		self.powerstatus = 1


	else:
		redcount = 1
                bluecount = 3
                for i in range(0,12):
                        self.pixels[redcount] = 0
                        self.pixels[bluecount] = 15
                        self.show(self.pixels)
                        redcount+=4
                        bluecount+=4
                        time.sleep(0.05)
                redcount=1
		bluecount = 3
                for i in range(0,12):
                        self.pixels[redcount]=15
			self.pixels[bluecount]=15
                        self.show(self.pixels)
                        redcount+=4
                        time.sleep(0.05)
		redcount = 1
		bluecount = 3
		for i in range(0,12):
                        self.pixels[redcount]=0
                        self.pixels[bluecount]=0
                        self.show(self.pixels)
                        redcount+=4
			bluecount +=4
                        time.sleep(0.05)

                self.powerstatus = 0

    def off(self):
        self.show([0] * 4 * 12)
