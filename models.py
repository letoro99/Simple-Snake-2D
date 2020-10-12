# Modelos del Snake version final
# Contiene : Creador manzana, snake y escenrario como nodos principales.
from OpenGL.GL import *
import transformations as tr
import basic_shapes as bs
import scene_graph as sg
import easy_shaders as es
import random as rd
import math as mt
import numpy as np

from OpenGL.GL import glClearColor
from typing import List


class Apple: # crea la figura de la manzana
    def __init__(self,n):
        self.n = n
        # basic figures
        gpu_body_quad = es.toGPUShape(bs.createColorQuad(1,0.1,0.1))
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
        self.pos_x = 0
        self.pos_y = 0
    
    def draw(self,pipeline):
        glUseProgram(pipeline.shaderProgram)
        self.model.transform = tr.translate(self.pos_x,self.pos_y,0)
        sg.drawSceneGraphNode(self.model,pipeline,'transform')

class CreadorApple(): # Encargado de la posicion y la actualizacion de la posicion de la manzana
    def __init__(self,n):
        self.fruta = Apple(n)
        self.rango = np.arange(-1+(1/n),1-(1/n),1/n)
    
    def randomPos(self):
        self.fruta.pos_x = self.rango[rd.randint(0,len(self.rango)-1)]
        self.fruta.pos_y = self.rango[rd.randint(0,len(self.rango)-1)]

    def draw(self,pipeline):
        self.fruta.draw(pipeline)

    def update(self,lista): # actualiza la posicion de la manzana sin que esta choque con Snake
        test = False
        error = 0.00001
        while test == False:
            self.randomPos()
            test = True
            for i in range(len(lista)):
                if self.fruta.pos_x - error <= lista[i][0] <= self.fruta.pos_x + error and self.fruta.pos_y - error <= lista[i][1] <=  self.fruta.pos_y + error:
                    test = False
                    break
        print(self.fruta.pos_x,self.fruta.pos_y)

class Cabeza: # Objeto que movera el jugador, se vera si choca o come la manzana
    def __init__(self,n,texture_head):
        self.n = n
        # basic figures
        gpu_cabeza_quad = es.toGPUShape(bs.createTextureQuad(texture_head),GL_REPEAT, GL_NEAREST)

        # cabeza
        cabeza = sg.SceneGraphNode('cabeza')
        cabeza.transform = tr.matmul([tr.translate(0,0,0),tr.uniformScale(1)])
        cabeza.childs += [gpu_cabeza_quad]

        # Ensamblamos 
        snake = sg.SceneGraphNode('snake')
        snake.transform = tr.matmul([tr.rotationX(1),tr.scale(1/n,2/n,1),tr.rotationZ(mt.pi/2)])
        snake.childs += [cabeza]

        transform_snake = sg.SceneGraphNode('snakeTR')
        transform_snake.childs += [snake]

        self.model = transform_snake
        self.pos_x = 0
        self.pos_y = 0
        self.vida = True

    def draw(self,pipeline):
        glUseProgram(pipeline.shaderProgram)
        sg.drawSceneGraphNode(self.model,pipeline,'transform')

    def gameOver(self):
        self.vida = False

    def colision(self,lista,snake,manzana,textura_body): # Revisa si la cabeza de la snake esta encima de el borde, su cuerpo o la manzana
        error = 0.00001
        if 1 - error < self.pos_x < 1  + error or -1 - error < self.pos_x < -1 +error:
            self.gameOver()

        if 1 - error < self.pos_y < 1 + error or -1 -error < self.pos_y < -1 +error:
            self.gameOver()
            
        for i in range(1,snake.largo+1):
            if self.pos_x - error <= lista[i][0] <= self.pos_x + error and self.pos_y - error <= lista[i][1] <= self.pos_y + error:
                self.gameOver()

            if self.pos_x - error <= manzana.fruta.pos_x <= self.pos_x + error and self.pos_y - error <= manzana.fruta.pos_y <= self.pos_y + error:
                snake.largo +=1
                nuevo = Cuerpo(0,0,self.n,textura_body)
                nuevo.posicionar(snake.cuerpo[snake.largo-1][0],snake.cuerpo[snake.largo-1][1])
                snake.cuerpo[snake.largo] = [snake.cuerpo[snake.largo-1][0],snake.cuerpo[snake.largo-1][1]]
                snake.cola.append(nuevo)
                manzana.update(snake.cuerpo)
                
        

class Cuerpo: # Cuerpo del jugador en la que estara en un lista para saber la posicion del cuerpo de la serpiente
    def __init__(self,x,y,n,textura):
        self.x = x
        self.y = y
        self.n = n
        # cuerpo
        gpu_cuerpo_quad = es.toGPUShape(bs.createTextureQuad(textura),GL_REPEAT,GL_NEAREST)

        cuerpo = sg.SceneGraphNode('cuerpo')
        cuerpo.transform = tr.matmul([tr.translate(self.x,self.y,0),tr.uniformScale(1/self.n)])
        cuerpo.childs += [gpu_cuerpo_quad]

        transform_cuerpo = sg.SceneGraphNode('cuerpoTR')
        transform_cuerpo.childs += [cuerpo]

        self.model = transform_cuerpo

    def draw(self,pipeline):
        glUseProgram(pipeline.shaderProgram)
        sg.drawSceneGraphNode(self.model,pipeline,'transform')

    def posicionar(self,posx,posy): # reubica al cuerpo
        self.x,self.y = posx,posy
        self.model.transform = tr.translate(posx,posy,0)

class Snake: # conjunto de la cabeza y el cuepro de la snake
    def __init__(self,n,texture_head,textura_body):
        self.n = n
        self.largo = 3
        self.cabeza = Cabeza(n,texture_head)
        self.cola = [Cuerpo(0,0,n,textura_body),Cuerpo(0,0,n,textura_body),Cuerpo(0,0,n,textura_body)]
        self.cuerpo = np.zeros((int(2*n-1)*int(2*n-1),2))
        for i in range(4):
            self.cuerpo[i] = [i/self.n,0]
        self.dx = -1*(1/n)
        self.dy = 0
        self.theta = -1*mt.pi/2
        self.jugando = False
        self.vida = True

    def draw(self,pipeline1,pipeline2):
        glUseProgram(pipeline2.shaderProgram)
        self.cabeza.draw(pipeline2)
        for i in range(len(self.cola)):
            self.cola[i].draw(pipeline2)
            
    def update(self): # actualiza la posicion de la cabeza y el cuerpo de la serpiente
        for i in range(len(self.cola)-1,-1,-1):
            self.cola[i].posicionar(self.cuerpo[i][0],self.cuerpo[i][1])
            self.cuerpo[i+1] = [self.cuerpo[i][0],self.cuerpo[i][1]]
        self.cabeza.pos_x += self.dx
        self.cabeza.pos_y += self.dy
        self.cuerpo[0] = [self.cabeza.pos_x,self.cabeza.pos_y]
        self.cabeza.model.transform = tr.matmul([tr.translate(self.cabeza.pos_x,self.cabeza.pos_y,0),tr.rotationZ(self.theta)])
        self.jugando = False
        print(self.cabeza.pos_x,self.cabeza.pos_y)

    
class Escenario: # Eso, el campo donde se jugara
    def __init__(self,n,texture_go,texture_win):
        # Basic Figures
        gpu_bordes_quad = es.toGPUShape(bs.createColorQuad(0,1,0)) #Verde fuerte
        gpu_campo_quad = es.toGPUShape(bs.createColorQuad(0.65,1,0.65)) # Verde no tan fuerte
        gpu_texture_go = es.toGPUShape(bs.createTextureQuad(texture_go),GL_REPEAT, GL_NEAREST)
        gpu_texture_win = es.toGPUShape(bs.createTextureQuad(texture_win),GL_REPEAT, GL_NEAREST)

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
        cuadro = sg.SceneGraphNode('cuadro')
        cuadro.transform = tr.uniformScale(1)
        cuadro.childs += [gpu_campo_quad]

        fondo_gameover = sg.SceneGraphNode('fondo_gameover')
        fondo_gameover.transform = tr.uniformScale(1)
        fondo_gameover.childs += [gpu_texture_go]

        fondo_win = sg.SceneGraphNode('fondo_win')
        fondo_win.transform = tr.uniformScale(1)
        fondo_win.childs += [gpu_texture_win]

        # Ensamblaje
        fondo = sg.SceneGraphNode('fondo')

        # Patron
        patron = sg.SceneGraphNode('patron_i')
        i = -1 + (1/n)
        while i < 1: # crea el patron de fondo
            temp = sg.SceneGraphNode('quad'+str(i))
            temp.transform = tr.matmul([tr.translate(i,0,0),tr.uniformScale(1/n)])
            temp.childs += [cuadro]
            patron.childs += [temp]
            i += 2/n

        i = 1 - (1/n)
        cont = 1
        while i > -1: # Ubica el patron de fondo, creando los necesarios para cubrir el campo
            temp = sg.SceneGraphNode('patron'+str(i))
            if cont%2 == 0:
                temp.transform = tr.translate(0,i,0)
            else:
                temp.transform = tr.translate(1/n,i,0)
            cont += 1
            temp.childs += [patron]
            fondo.childs += [temp]
            i -= 1/n

        fondo.childs += [border_vu,border_hr,border_hl,border_vd]

        self.model = fondo
        self.model1 = fondo_gameover
        self.model2 = fondo_win

    def draw(self,pipeline): # dibuja el campo
        glUseProgram(pipeline.shaderProgram)
        sg.drawSceneGraphNode(self.model,pipeline,'transform')
    
    def draw_go(self,pipeline,x): # Dibuja la pantalla de textura
        if x == 1:
            glUseProgram(pipeline.shaderProgram)
            sg.drawSceneGraphNode(self.model1,pipeline,'transform')
        if x == 2:
            glUseProgram(pipeline.shaderProgram)
            sg.drawSceneGraphNode(self.model2,pipeline,'transform')
    
    def update(self,rotacion): # Animacion de la pantalla de perdida
        self.model1.transform = tr.matmul([tr.uniformScale(2),tr.rotationZ(rotacion),tr.translate(rotacion/100,0,0)])

    