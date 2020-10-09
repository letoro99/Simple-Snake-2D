# script principal para el juego
import glfw
from OpenGL.GL import *
import sys
import os

from models import *
from control import Controller

if __name__ == '__main__':
    print(sys.argv)
    n = int(sys.argv[1])

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
    pipeline = es.SimpleTransformShaderProgram()

    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.8, 1, 0.8, 1.0)

    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    fondo = Escenario(n)
    snake = Snake(n)
    manzana = CreadorApple(n)

    controlador.set_model(snake)
    controlador.set_apple(manzana)
    controlador.set_dif(1/n)
    t0 = 0
    dt = 0
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
        snake.draw(pipeline)
        manzana.draw(pipeline)
        fondo.draw(pipeline)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()