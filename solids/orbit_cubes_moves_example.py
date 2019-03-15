import pygame
from pygame.locals import *

from solids.Solids import *

from OpenGL.GL import *
from OpenGL.GLU import *


class Orbit(SolidsGroup):
    def __init__(self,
                 origin=(0, 0, -5),
                 origin_offset=(0, 0, 0),
                 axis=(0, 0, 1),
                 theta=np.pi/2):

        self.solids_list = []

        cube_1 = Cube(color=(0.2, 0.8, 1),
                      origin=origin,
                      origin_offset=origin_offset,
                      axis=axis,
                      theta=theta,
                      size=0.2)
        self.solids_list.append(cube_1)

        cube_2 = Cube(color=(0.4, 0.6, 1),
                      origin=origin,
                      origin_offset=(0.5+origin_offset[0], 0+origin_offset[1], 0+origin_offset[2]),
                      axis=axis,
                      theta=theta,
                      size=0.18)
        self.solids_list.append(cube_2)

        cube_3 = Cube(color=(0.6, 0.4, 0.9),
                      origin=origin,
                      origin_offset=(1+origin_offset[0], 0+origin_offset[1], 0+origin_offset[2]),
                      axis=axis,
                      theta=theta,
                      size=0.16)
        self.solids_list.append(cube_3)

        cube_4 = Cube(color=(0.8, 0.3, 0.6),
                      origin=origin,
                      origin_offset=(1.5+origin_offset[0], 0+origin_offset[1], 0+origin_offset[2]),
                      axis=axis,
                      theta=theta,
                      size=0.14)
        self.solids_list.append(cube_4)

        cube_5 = Cube(color=(1, 0, 0.2),
                      origin=origin,
                      origin_offset=(2+origin_offset[0], 0+origin_offset[1], 0+origin_offset[2]),
                      axis=axis,
                      theta=theta,
                      size=0.12)
        self.solids_list.append(cube_5)

        super().__init__(solids_list=self.solids_list,
                         origin=origin,
                         origin_offset=origin_offset,
                         axis=axis,
                         theta=theta)


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(50, (display[0]/display[1]), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)

    orbit_list = []

    orbit_list.append(Orbit(origin=(0, 0, -5),
                            origin_offset=(1, 0, 0),
                            axis=(0, 1, 1),
                            theta=np.pi/2))

    orbit_list.append(Orbit(origin=(0, 0, -5),
                            origin_offset=(1, 0, 0),
                            axis=(1, 1, 0),
                            theta=np.pi/2))

    orbit_list.append(Orbit(origin=(0, 0, -5),
                            origin_offset=(1, 0, 0),
                            axis=(1, 0, 1),
                            theta=np.pi/2))

    orbit_list.append(Orbit(origin=(0, 0, -5),
                            origin_offset=(1, 0, 0),
                            axis=(0, -1, -1),
                            theta=np.pi/2))

    orbit_list.append(Orbit(origin=(0, 0, -5),
                            origin_offset=(1, 0, 0),
                            axis=(-1, -1, 0),
                            theta=np.pi/2))

    orbit_list.append(Orbit(origin=(0, 0, -5),
                            origin_offset=(1, 0, 0),
                            axis=(-1, 0, -1),
                            theta=np.pi/2))

    orbit_list.append(Orbit(origin=(0, 0, -5),
                            origin_offset=(1, 0, 0),
                            axis=(0, -1, 1),
                            theta=np.pi/2))

    orbit_list.append(Orbit(origin=(0, 0, -5),
                            origin_offset=(1, 0, 0),
                            axis=(-1, 1, 0),
                            theta=np.pi/2))

    orbit_list.append(Orbit(origin=(0, 0, -5),
                            origin_offset=(1, 0, 0),
                            axis=(-1, 0, 1),
                            theta=np.pi/2))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for i, orbit in enumerate(orbit_list):
            orbit.theta += np.pi/(20+i)
            orbit.draw()

        pygame.display.flip()

        pygame.time.wait(33)


main()