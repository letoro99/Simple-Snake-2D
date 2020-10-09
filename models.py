# Modelos del Snake
# Contiene :

import transformations as tr
import basic_shapes as bs
import scene_graph as sg
import easy_shaders as es
import random as rd
import math as mt

from OpenGL.GL import glClearColor
from typing import List


class Apple:
    def __init__(self,n):
        self.n = n
        # basic figures
        gpu_body_quad = es.toGPUShape(bs.createColorQuad(0,0,1))
        gpu_rama_quad = es.toGPUShape(bs.createColorQuad(0.8,0.5,0.5))

        # Creamos el cuerpo
        body = sg.SceneGraphNode('body')
        body.transform = tr.uniformScale(0.8)
        body.childs += [gpu_body_quad]

        # Rama
        rama = sg.SceneGraphNode('rama')
        rama.transform = tr.matmul([tr.scale(0.2,0.5,0),tr.translate(0,0.8,0)])
        rama.childs += [gpu_rama_quad]

        # Ensamblamos
        apple = sg.SceneGraphNode('apple')
        apple.transform = tr.uniformScale(1/self.n)
        apple.childs += [body,rama]

        transform_apple = sg.SceneGraphNode('appleTR')
        transform_apple.childs += [apple]

        self.model = transform_apple
        self.pos_x = mt.trunc(rd.random()*rd.randint(-1,0)*10)/10
        self.pos_y = mt.trunc(rd.random()*rd.randint(-1,1)*10)/10
    
    def draw(self,pipeline):
        self.model.transform = tr.translate(self.pos_x,self.pos_y,0)
        sg.drawSceneGraphNode(self.model,pipeline,'transform')

class CreadorApple():
    def __init__(self,n):
        self.comidas = 1
        self.fruta = Apple(n)

    def draw(self,pipeline):
        self.fruta.draw(pipeline)

    def update(self,lista):
        self.comidas += 1
        print(self.comidas)
        test = False
        error = 0.00001
        self.fruta.pos_x = mt.trunc(rd.random()*rd.randint(-1,1)*10)/10
        self.fruta.pos_y = mt.trunc(rd.random()*rd.randint(-1,1)*10)/10
        while test == False:
            self.fruta.pos_x = mt.trunc(rd.random()*rd.randint(-1,1)*10)/10
            self.fruta.pos_y = mt.trunc(rd.random()*rd.randint(-1,1)*10)/10
            test = True
            for i in range(len(lista)):
                if self.fruta.pos_x - error <= lista[i][0] <= self.fruta.pos_x + error and self.fruta.pos_y - error <= lista[i][1] <=  self.fruta.pos_y + error:
                    test = False
                    break
            print(self.fruta.pos_x,self.fruta.pos_y)

class Cabeza:
    def __init__(self,n):
        self.n = n
        # basic figures
        gpu_cabeza_quad = es.toGPUShape(bs.createColorCube(0,1,1))

        # cabeza
        cabeza = sg.SceneGraphNode('cabeza')
        cabeza.transform = tr.matmul([tr.translate(0,0,0),tr.uniformScale(1)])
        cabeza.childs += [gpu_cabeza_quad]

        # Ensamblamos 
        snake = sg.SceneGraphNode('snake')
        snake.transform = tr.matmul([tr.uniformScale(1/self.n),tr.rotationX(90)])
        snake.childs += [cabeza]

        transform_snake = sg.SceneGraphNode('snakeTR')
        transform_snake.childs += [snake]

        self.model = transform_snake
        self.pos_x = 0
        self.pos_y = 0
        self.vida = True
    
    def draw(self,pipeline):
        sg.drawSceneGraphNode(self.model,pipeline,'transform')

    def gameOver(self):
        self.vida == False
        glClearColor(1,0,0,1.0)

    def colision(self,lista,snake,manzana):
        error = 0.00001
        if 1 - error < self.pos_x < 1  + error or -1 - error < self.pos_x < -1 +error:
            self.gameOver()
        if 1 - error < self.pos_y < 1 + error or -1 -error < self.pos_y < -1 +error:
            self.gameOver()
        for i in range(1,len(lista)):
            if self.pos_x - error <= lista[i][0] <= self.pos_x + error and self.pos_y - error <= lista[i][1] <= self.pos_y + error:
                self.gameOver()
        

class Cuerpo:
    def __init__(self,x,y,n):
        self.x = x
        self.y = y
        self.n = n
        # cuerpo
        gpu_cuerpo_quad = es.toGPUShape(bs.createColorQuad(0.8,0.8,0.2))

        cuerpo = sg.SceneGraphNode('cuerpo')
        cuerpo.transform = tr.matmul([tr.translate(self.x,self.y,0),tr.uniformScale(1/self.n)])
        cuerpo.childs += [gpu_cuerpo_quad]

        transform_cuerpo = sg.SceneGraphNode('cuerpoTR')
        transform_cuerpo.childs += [cuerpo]

        self.model = transform_cuerpo

    def draw(self,pipeline):
        sg.drawSceneGraphNode(self.model,pipeline,'transform')

    def posicionar(self,posx,posy):
        self.x,self.y = posx,posy
        self.model.transform = tr.translate(posx,posy,0)

class Snake:
    def __init__(self,n):
        self.n = n
        self.cabeza = Cabeza(n)
        self.cola = [Cuerpo(0,0,n),Cuerpo(0,0,n),Cuerpo(0,0,n)]
        self.cuerpo = [[0,0],[1/self.n,0],[2/self.n,0],[3/self.n,0]]
        self.dx = -1*(1/n)
        self.dy = 0
        self.jugando = False

    def draw(self,pipeline):
        self.cabeza.draw(pipeline)
        for i in range(len(self.cola)):
            self.cola[i].draw(pipeline)
            
    def update(self):
        for i in range(len(self.cola)-1,-1,-1):
            self.cola[i].posicionar(self.cuerpo[i][0],self.cuerpo[i][1])
            self.cuerpo[i+1] = [self.cuerpo[i][0],self.cuerpo[i][1]]
        self.cabeza.pos_x += self.dx
        self.cabeza.pos_y += self.dy
        self.cuerpo[0] = [self.cabeza.pos_x,self.cabeza.pos_y]
        self.cabeza.model.transform = tr.translate(self.cabeza.pos_x,self.cabeza.pos_y,0)
        self.jugando = False
    
    def comer(self,manzana):
        error = 0.00001 
        if self.cabeza.pos_x - error <= manzana.fruta.pos_x <= self.cabeza.pos_x + error and self.cabeza.pos_y - error <= manzana.fruta.pos_y <= self.cabeza.pos_y + error:
            nuevo = Cuerpo(0,0,self.n)
            nuevo.posicionar(self.cuerpo[len(self.cuerpo)-1][0],self.cuerpo[len(self.cuerpo)-1][1])
            self.cuerpo.append([self.cuerpo[len(self.cuerpo)-1][0],self.cuerpo[len(self.cuerpo)-1][1]])
            self.cola.append(nuevo)
            manzana.update(self.cuerpo)

class Escenario:
    def __init__(self,n):
        # Basic Figures
        gpu_bordes_quad = es.toGPUShape(bs.createColorQuad(0,1,0)) #Verde fuerte
        gpu_campo_quad = es.toGPUShape(bs.createColorQuad(0.3,1,0.3)) # Verde no tan fuerte

        # creamos los bordes horizontales
        border_h = sg.SceneGraphNode('border_h')
        border_h.transform = tr.scale(1/n,2,0)
        border_h.childs += [gpu_bordes_quad]

        # creamos bordes verticales
        border_v = sg.SceneGraphNode('border_v')
        border_v.transform = tr.scale(2,1/n,0)
        border_v.childs += [gpu_bordes_quad]

        # bordes left-rigth
        border_hl = sg.SceneGraphNode('border_hl')
        border_hl.transform = tr.translate(-1,0,0)
        border_hl.childs += [border_h]

        border_hr = sg.SceneGraphNode('border_hr')
        border_hr.transform = tr.translate(1,0,0)
        border_hr.childs += [border_h]

        # bordes up-down
        border_vu = sg.SceneGraphNode('border_vu')
        border_vu.transform = tr.translate(0,1,0)
        border_vu.childs += [border_v]

        border_vd = sg.SceneGraphNode('border_vd')
        border_vd.transform = tr.translate(0,-1,0)
        border_vd.childs += [border_v]

        # Fondo cuadriculado
        # cuadro 1
        cuadro1 = sg.SceneGraphNode('cuadro1')
        cuadro1.transform = tr.uniformScale(1)
        cuadro1.childs += [gpu_campo_quad]

        #patron 1
        # Ensamblaje
        fondo = sg.SceneGraphNode('fondo')
        fondo.childs += [border_vu,border_hr,border_hl,border_vd]
        
        self.model = fondo

    def draw(self,pipeline):
        sg.drawSceneGraphNode(self.model,pipeline,'transform')