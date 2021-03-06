import pygame
from pygame.locals import *

from solids.Solids import *

from OpenGL.GL import *
from OpenGL.GLU import *


class Tank(SolidsGroup):
    def __init__(self,
                 origin=(0, 0, 0),
                 origin_offset=(0, 0, 0),
                 axis=(1, 1, 0),
                 theta=np.pi/2):

        self.solids_list = []

        track_1 = Trapezoid(color=(0.1, 0.1, 0.1),
                            origin=origin,
                            origin_offset=(origin_offset[0],
                                           0.1 + origin_offset[1],
                                           origin_offset[2] + 0.45),
                            axis=axis,
                            theta=theta,
                            size=(1.6, 1.6, 1.7, 1.7, 0.2, 0.25))
        self.solids_list.append(track_1)

        track_2 = Trapezoid(color=(0.1, 0.1, 0.1),
                            origin=origin,
                            origin_offset=(origin_offset[0],
                                           0.1+origin_offset[1],
                                           -0.45+origin_offset[2]),
                            axis=axis,
                            theta=theta,
                            size=(1.6, 1.6, 1.7, 1.7, 0.2, 0.25))
        self.solids_list.append(track_2)

        chassis_1 = Trapezoid(color=(0, 0.2, 0),
                              origin=origin,
                              origin_offset=(origin_offset[0],
                                             0.1+origin_offset[1],
                                             origin_offset[2]),
                              axis=axis,
                              theta=theta,
                              size=(1.5, 1.5, 1.7, 1.6, 0.2, 0.6))
        self.solids_list.append(chassis_1)

        chassis_2 = Trapezoid(color=(0, 0.3, 0),
                              origin=origin,
                              origin_offset=(origin_offset[0],
                                             self.solids_list[-1].size[4]/2
                                             + self.solids_list[-1].origin_offset[1]
                                             + 0.05
                                             + origin_offset[1],
                                             origin_offset[2]),
                              axis=axis,
                              theta=theta,
                              size=(1.7, 1.6, 1.3, 1.6, 0.1, 1))
        self.solids_list.append(chassis_2)

        chassis_3 = Trapezoid(color=(0, 0.3, 0),
                              origin=origin,
                              origin_offset=(origin_offset[0],
                                             self.solids_list[-1].size[4]/2
                                             + self.solids_list[-1].origin_offset[1]
                                             + 0.05
                                             + origin_offset[1],
                                             origin_offset[2]),
                              axis=axis,
                              theta=theta,
                              size=(1.2, 1.6, 1.2, 1.3, 0.1, 1))
        self.solids_list.append(chassis_3)

        chassis_4 = Trapezoid(color=(0, 0.3, 0),
                              origin=origin,
                              origin_offset=(origin_offset[0],
                                             self.solids_list[-1].size[4]/2
                                             + self.solids_list[-1].origin_offset[1]
                                             + 0.0125
                                             + origin_offset[1],
                                             origin_offset[2]),
                              axis=axis,
                              theta=theta,
                              size=(1.2, 1.3, 1, 1, 0.025, 1))
        self.solids_list.append(chassis_4)

        turret_1 = Hexagon(color=(0, 0.3, 0),
                           origin=origin,
                           origin_offset=(origin_offset[2],
                                          origin_offset[2]
                                          + self.solids_list[-1].size[4]/2
                                          + self.solids_list[-1].origin_offset[1]
                                          + 0.025
                                          + origin_offset[1],
                                          origin_offset[2]),
                           axis=axis,
                           theta=theta,
                           size=(0.8, 0.05))
        self.solids_list.append(turret_1)

        turret_2 = Hexagon(color=(0, 0.25, 0),
                           origin=origin,
                           origin_offset=(origin_offset[1],
                                          self.solids_list[-1].size[1]/2
                                          + self.solids_list[-1].origin_offset[1]
                                          + 0.05
                                          +origin_offset[1],
                                          origin_offset[2]),
                           axis=axis,
                           theta=theta,
                           size=(1, 0.1))
        self.solids_list.append(turret_2)

        turret_3 = Hexagon(color=(0, 0.30, 0),
                           origin=origin,
                           origin_offset=(origin_offset[0],
                                          self.solids_list[-1].size[1]/2
                                          + self.solids_list[-1].origin_offset[1]
                                          + 0.025
                                          + origin_offset[1],
                                          origin_offset[2]),
                           axis=axis,
                           theta=theta,
                           size=(0.76, 0.05))
        self.solids_list.append(turret_3)

        turret_4 = Hexagon(color=(0, 0.3, 0),
                           origin=origin,
                           origin_offset=(origin_offset[1],
                                          self.solids_list[-1].size[1]/2 +
                                          self.solids_list[-1].origin_offset[1]
                                          + 0.0125
                                          + origin_offset[1],
                                          origin_offset[2]),
                           axis=axis,
                           theta=theta,
                           size=(0.7, 0.025))
        self.solids_list.append(turret_4)

        cannon_1 = HexagonAxis(color=(0, 0.15, 0),
                               origin=origin,
                               origin_offset=(-1,
                                              self.solids_list[-1].size[1]/2
                                              + self.solids_list[-1].origin_offset[1]
                                              - 0.1,
                                              0),
                               axis=axis,
                               theta=theta,
                               size=(0.1, 1.6))
        self.solids_list.append(cannon_1)

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

    tank_1 = Tank(origin=(-2, 0, -5),
                  axis=(1, -1, 0))
    i = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        tank_1.draw()

        tank_1.theta += np.pi/20
        if i < 40:
            tank_1.origin += np.asarray([0.1, 0.0, 0.0])
            i += 1
        if 40 <= i < 80:
            tank_1.origin -= np.asarray([0.1, 0.0, 0.0])
            i += 1
        if i >= 80:
            i = 0

        pygame.display.flip()

        pygame.time.wait(33)


main()