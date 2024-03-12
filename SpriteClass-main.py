from microbit import *
import neopixel
from random import randint
import machine
np = neopixel.NeoPixel(pin0,64)

np = neopixel.NeoPixel(pin0, 64) #changed from 32 to 64 to get full 8x8 array
#V2 microbit has configurable pin drives, which are setup differently to the V1 by default.
#The NRF processor GPIO pin2 is microbit pin0  where the ZIP LEDs are connected.
#To set it to high drive mode we write directly to the configuration register with this obscure looking incantation:
machine.mem32[0x50000708]= 0x703

def np_plot(x, y, r, g, b):
    np[x+(y*8)] = (r, g, b)

# This should be a class called Sprite that mimics the 
# behaviour of the Sprite class in MakeCode 

# Create sprite at x, y returns the class as well as calls "display"


class MySprite:
    def __init__(self, x, y, r, g, b):
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.b = b
        self.plot()

    # set should erase current location as well
    def set(self, coord, value):
        self.clear()
        if coord.lower() == "x" and value < 8 and value >= 0:
            # print("set x",value)
            self.x = value
        elif coord.lower() == "y" and value < 8 and value >= 0:
            # print("set y", value)
            self.y = value
        self.plot()
        
    def change(self, coord, value):
        self.clear()
        if coord.lower() == "x" and self.x + value < 8 and self.x + value >= 0:
            # print("change x",value)
            self.x = self.x + value
        elif coord.lower() == "y" and self.y + value < 8 and self.y + value >= 0:
            # print("change y", value)
            self.y = self.y + value
        self.plot()

    def clear(self):
        np_plot(self.x, self.y, 0,0,0)
        np.show()
        
    def plot(self):
        np_plot(self.x, self.y, self.r, self.g, self.b)
        np.show()

    def __del__(self):
        self.clear()

ticks = 1
emptyObstacleY = 0
obstacles = []
bird = MySprite(0, 2,25,0,0)

emptyObstacleY = randint(0, 7)
for index in range(8):
    if index != emptyObstacleY:
        obstacles.append(MySprite(7, index,0,0,25))

while True:
    if pin8.read_digital() == 0:
        bird.change("y",-1)
    if pin14.read_digital() == 0:
        bird.change("y",1)
   
    while len(obstacles) > 0 and obstacles[0].x == 0:
        # print("obs-len", len(obstacles), "x=",obstacles[0].x)
        obstacles[0].clear()
        obstacles.pop(0)
    if ticks % 10 == 0:   
        for obstacle in obstacles:
            obstacle.change("x", -1)
    if ticks % 30 == 0:    
        emptyObstacleY = randint(0, 7)
        for index in range(8):
            if index != emptyObstacleY:
                obstacles.append(MySprite(7, index,0,0,25))
    ticks += 1
    print(ticks)
    sleep(100)

        