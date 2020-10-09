# script principal para el juego
import glfw
from OpenGL.GL import *
import sys
import os

from models import *
from control import Controller

if __name__ == '__main__':
    print(sys.argv)
    n = 10

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 800
    height = 600

    window = glfw.create_window(width, height, "Snake!", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    controlador = Controller()

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, controlador.on_key)

    # Assembling the shader program (pipeline) with both shaders
    pipeline_color = es.SimpleTransformShaderProgram()
    pipeline_texture = es.SimpleTextureTransformShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.8, 1, 0.8, 1.0)

    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    fondo = Escenario(n,'img/game_over.png')
    snake = Snake(n,'img/serpiente.png')
    manzana = CreadorApple(n)

    controlador.set_model(snake)
    controlador.set_apple(manzana)
    controlador.set_dif(1/n)
    t0 = 0
    dt = 0
    rot = 0
    vel = 0.1


    while not glfw.window_should_close(window):
        
        ti = glfw.get_time()
        dt = ti - t0

        if dt > vel:
            snake.update()
            snake.cabeza.colision(snake.cuerpo,snake,manzana)
            snake.comer(manzana)
            dt = 0
            t0 = ti


        # Using GLFW to check for input events
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT)

        # Dibujamos
        if snake.cabeza.vida == True:
            fondo.draw(pipeline_color)
            snake.draw(pipeline_color,pipeline_texture)
            manzana.draw(pipeline_color)

            # Once the render is done, buffers are swapped, showing only the complete scene.
            glfw.swap_buffers(window)
        
        else:
            glClearColor(0, 0, 0, 0)
            if rot < (mt.pi/8):
                fondo.update(rot)
                rot += 0.0001
            fondo.draw_go(pipeline_texture)
             # Once the render is done, buffers are swapped, showing only the complete scene.
            glfw.swap_buffers(window)

    glfw.terminate()