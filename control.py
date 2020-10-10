"Codigo para el control de snake!"

from models import *
import glfw
import sys
from typing import Union

class Controller:
    model : Union['Snake',None]
    apple : Union['Apple',None]

    def __init__(self):
        self.model = None
        self.apple = None
        self.dif = None
        self.last_button = "a"

    def set_model(self,m):
        self.model = m

    def set_apple(self,a):
        self.apple = a

    def set_dif(self,n):
        self.dif = n

    def on_key(self,window,key,scancode,action,mods):

        if action != glfw.PRESS:
            return
            
        elif (key == glfw.KEY_LEFT or key == glfw.KEY_A) and action == glfw.PRESS:
            if self.model.jugando == False and self.model.dx != self.dif:
                if self.model.dy < 0 and self.last_button != "a":
                    self.model.theta += -1*(mt.pi/2)
                if self.model.dy > 0 and self.last_button != "a":
                    self.model.theta += 1*(mt.pi/2)
                self.last_button = "a"
                self.model.jugando = True
                self.model.dx = -1*self.dif
                self.model.dy = 0

        elif (key == glfw.KEY_RIGHT or key == glfw.KEY_D) and action == glfw.PRESS:
            if self.model.jugando == False and self.model.dx != -1*self.dif:
                if self.model.dy < 0 and self.last_button != "d":
                    self.model.theta += 1*(mt.pi/2)
                if self.model.dy > 0 and self.last_button != "d":
                    self.model.theta += -1*(mt.pi/2)
                self.last_button = "d"
                self.model.jugando = True
                self.model.dx = self.dif
                self.model.dy = 0

        elif (key == glfw.KEY_UP or key == glfw.KEY_W) and action == glfw.PRESS:
            if self.model.jugando == False and self.model.dy != -1*self.dif:
                if self.model.dx < 0 and self.last_button != "w":
                    self.model.theta += -1*(mt.pi/2)
                if self.model.dx > 0 and self.last_button != "w":
                    self.model.theta += 1*(mt.pi/2)
                self.last_button = "w"
                self.model.dx = 0
                self.model.dy = self.dif
                self.model.jugando = True

        elif(key == glfw.KEY_DOWN or key == glfw.KEY_S) and action == glfw.PRESS:
            if self.model.jugando == False and self.model.dy != self.dif:
                if self.model.dx < 0 and self.last_button != "s":
                    self.model.theta += 1*(mt.pi/2)
                if self.model.dx > 0 and self.last_button != "s":
                    self.model.theta += -1*(mt.pi/2)
                self.last_button = "s"
                self.model.dx = 0
                self.model.dy = -1*self.dif
                self.model.jugando = True

        if key == glfw.KEY_ESCAPE:
            sys.exit()
