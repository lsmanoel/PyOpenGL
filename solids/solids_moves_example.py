import pygame
from pygame.locals import *

from solids.Solids import *

from OpenGL.GL import *
from OpenGL.GLU import *


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(50, (display[0]/display[1]), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)

    cube_1 = Cube(color=(0, 1, 0))

    pyramid_1 = Pyramid(color=(1, 0, 0))

    chassis_2 = Trapezoid(color=(0, 0.5, 0),
                          origin=(0, 0, -5),
                          axis=(0, 0, 1),
                          theta=np.pi / 4,
                          size=(1.7, -1.6, 1.6, -1.5, 0.1, 0.1))


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # cube_1.origin = [1, 0, -5]
        # cube_1.axis = [1, 0, 0]
        # cube_1.theta_degree -= 1
        # cube_1.draw(mode='translate>rotate')
        #
        # pyramid_1.draw(mode='translate>rotate')
        # pyramid_1.origin = [0, 0, -5]
        # pyramid_1.axis = [1, 0, 0]
        # pyramid_1.theta_degree += 1
        # pyramid_1.draw()

        chassis_2.theta_degree += 1
        chassis_2.draw()

        pygame.display.flip()

        pygame.time.wait(33)


main()