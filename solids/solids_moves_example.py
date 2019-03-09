import pygame
from pygame.locals import *

from solids.Solids import *

from OpenGL.GL import *
from OpenGL.GLU import *


class Orbit:
    def __init__(self,
                 origin=(0, 0, -5),
                 offset=(0, 0, 0),
                 axis=(0, 0, 1),
                 theta=np.pi/2):

        self.solids_list = []

        cube_1 = Cube(color=(0.2, 0.8, 1),
                      origin=origin,
                      offset=offset,
                      axis=axis,
                      theta=theta,
                      size=0.2)
        self.solids_list.append(cube_1)

        cube_2 = Cube(color=(0.4, 0.6, 1),
                      origin=origin,
                      offset=(0.5+offset[0], 0+offset[1], 0+offset[2]),
                      axis=axis,
                      theta=theta,
                      size=0.18)
        self.solids_list.append(cube_2)

        cube_3 = Cube(color=(0.6, 0.4, 0.9),
                      origin=origin,
                      offset=(1+offset[0], 0+offset[1], 0+offset[2]),
                      axis=axis,
                      theta=theta,
                      size=0.16)
        self.solids_list.append(cube_3)

        cube_4 = Cube(color=(0.8, 0.3, 0.6),
                      origin=origin,
                      offset=(1.5+offset[0], 0+offset[1], 0+offset[2]),
                      axis=axis,
                      theta=theta,
                      size=0.14)
        self.solids_list.append(cube_4)

        cube_5 = Cube(color=(1, 0, 0.2),
                      origin=origin,
                      offset=(2+offset[0], 0+offset[1], 0+offset[2]),
                      axis=axis,
                      theta=theta,
                      size=0.12)
        self.solids_list.append(cube_5)

        self._origin = np.asarray(origin)
        self._offset = np.asarray(offset)
        self._axis = np.asarray(axis)
        self._theta_degree = 0
        self._theta = 0

    def draw(self):
        for solid in self.solids_list:
            solid.draw()

    @property
    def origin(self):
        return self.origin

    @origin.setter
    def origin(self, value):
        for solid in self.solids_list:
            solid.origin = np.asarray(value)

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        for solid in self.solids_list:
            solid.offset = np.asarray(value)

    @property
    def axis(self):
        return self._axis

    @axis.setter
    def axis(self, value):
        for solid in self.solids_list:
            solid.axis = np.asarray(value)

    @property
    def theta(self):
        return self._theta

    @theta.setter
    def theta(self, value):
        self._theta = value
        if self._theta > 2*np.pi:
            self._theta += 2*np.pi
        elif self._theta > 2*np.pi:
            self._theta -= 2*np.pi

        self._theta_degree = 180 * (value / np.pi)

        for solid in self.solids_list:
            solid.theta = self._theta

    @property
    def theta_degree(self):
        return self._theta_degree

    @theta_degree.setter
    def theta_degree(self, value):
        self._theta_degree = value
        if self._theta_degree < 0:
            self._theta_degree += 360
        elif self._theta_degree > 360:
            self._theta_degree -= 360

        self._theta = np.pi * (value / 180)

        for solid in self.solids_list:
            solid.theta_degree = self._theta_degree


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(50, (display[0]/display[1]), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)

    orbit_list = []

    orbit_list.append(Orbit(origin=(0, 0, -5),
                            offset=(1, 0, 0),
                            axis=(0, 1, 1),
                            theta=np.pi/2))

    orbit_list.append(Orbit(origin=(0, 0, -5),
                            offset=(1, 0, 0),
                            axis=(1, 1, 0),
                            theta=np.pi/2))

    orbit_list.append(Orbit(origin=(0, 0, -5),
                            offset=(1, 0, 0),
                            axis=(1, 0, 1),
                            theta=np.pi/2))

    orbit_list.append(Orbit(origin=(0, 0, -5),
                            offset=(1, 0, 0),
                            axis=(0, -1, -1),
                            theta=np.pi/2))

    orbit_list.append(Orbit(origin=(0, 0, -5),
                            offset=(1, 0, 0),
                            axis=(-1, -1, 0),
                            theta=np.pi/2))

    orbit_list.append(Orbit(origin=(0, 0, -5),
                            offset=(1, 0, 0),
                            axis=(-1, 0, -1),
                            theta=np.pi/2))

    orbit_list.append(Orbit(origin=(0, 0, -5),
                            offset=(1, 0, 0),
                            axis=(0, -1, 1),
                            theta=np.pi/2))

    orbit_list.append(Orbit(origin=(0, 0, -5),
                            offset=(1, 0, 0),
                            axis=(-1, 1, 0),
                            theta=np.pi/2))

    orbit_list.append(Orbit(origin=(0, 0, -5),
                            offset=(1, 0, 0),
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