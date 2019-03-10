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

    parallelepiped_1 = Parallelepiped(color=(4, 5.5, 1),
                                      angle=np.pi/4)

    parallelepiped_2 = Parallelepiped(color=(4, 5.5, 1),
                                      alpha=np.pi/5,
                                      size=(0.1, 0.5, 0.4))

    pyramid_1 = Pyramid(color=(1, 0, 0))

    pyramid_trunk_1 = PyramidTrunk(color=(0.3, 0.5, 1),
                                   angle=np.pi/2)

    hexagon_1 = Hexagon(color=(0, 0.1, 0.7))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        cube_1.origin = [1, 0, -5]
        cube_1.axis = [1, 1, 0]
        cube_1.angle_degree -= 1
        cube_1.draw()

        parallelepiped_1.origin = [1, 1, -5]
        parallelepiped_1.axis = [1, 1, 0]
        parallelepiped_1.angle_degree += 1
        parallelepiped_1.draw()

        parallelepiped_2.origin = [-1, 1, -5]
        parallelepiped_2.axis = [1, 0.3, 0]
        parallelepiped_2.angle_degree -= 1
        parallelepiped_2.draw()

        pyramid_1.draw()
        pyramid_1.origin = [0, 0, -5]
        pyramid_1.axis = [1, 1, 0]
        pyramid_1.angle_degree += 1
        pyramid_1.draw()

        pyramid_trunk_1.origin = [-1, -0, -5]
        pyramid_trunk_1.axis = [1, 1, 1]
        pyramid_trunk_1.angle -= 0.01*np.pi
        pyramid_trunk_1.draw()

        hexagon_1.origin = [-1, -1, -5]
        hexagon_1.axis = [0, 0.3, 1]
        hexagon_1.angle -= 0.01*np.pi
        hexagon_1.draw()

        pygame.display.flip()

        pygame.time.wait(33)


main()