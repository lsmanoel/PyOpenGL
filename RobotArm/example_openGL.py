import pygame
from pygame.locals import *
import numpy as np
from RobotArm.Parts import MasterPart, SlavePart
from solids.Solids import *
import time
import threading
import os
import sys
import cv2
from OpenGL.GL import *
from OpenGL.GLU import *


class PgScreen:
    def __init__(self,
                 screen_size=(900, 300),
                 clock_rate=30,
                 pixel_meter=100):

        self.screen_size = screen_size
        self.clock_rate = clock_rate
        self.pixel_meter = pixel_meter

        pygame.init()
        self.screen = pygame.display.set_mode(screen_size, DOUBLEBUF | OPENGL)
        gluPerspective(50, (screen_size[0] / screen_size[1]), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)

        self.main_state = 'start_state'
        self.close_app = False
        self.clock = pygame.time.Clock()

        # --------------------------------------------------------------------------------------------------------------
        self.part_list = []

        self.part_list.append(MasterPart(origin=(0, 0, 0),
                                         theta=0,
                                         phi=np.pi/2,
                                         length=1))

    def check_key_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cv2.destroyAllWindows()
                self.close_app = True

        if self.main_state == 'start_state':
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_SPACE]:
                self.main_state = 'run_state'

        elif self.main_state == 'run_state':
            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_UP]:
                self.part_list[0].phi_degree += 5
            elif pressed[pygame.K_DOWN]:
                self.part_list[0].phi_degree -= 5

            if pressed[pygame.K_LEFT]:
                self.part_list[0].theta_degree += 5
            elif pressed[pygame.K_RIGHT]:
                self.part_list[0].theta_degree -= 5

            if pressed[pygame.K_w]:
                self.part_list[0].origin += np.array([0.1, 0, 0])
            if pressed[pygame.K_s]:
                self.part_list[0].origin -= np.array([0.1, 0, 0])
            if pressed[pygame.K_d]:
                self.part_list[0].origin += np.array([0, 0, 0.1])
            if pressed[pygame.K_a]:
                self.part_list[0].origin -= np.array([0, 0, 0.1])

        elif self.main_state == 'restart_state':
            os.execl(sys.executable, sys.executable, *sys.argv)

    def main_loop(self):
        while not self.close_app:
            self.check_key_events()
            if self.main_state == 'run_state':
                pass

            self.screen_update()
            time.sleep(1 / self.clock_rate)

        pygame.quit()
        quit()

    def screen_update(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        if self.main_state == 'start_state':
            pass

        elif self.main_state == 'run_state':
            for part in self.part_list:
                part.draw()

        pygame.display.flip()


# ======================================================================================================================
PgScreen(screen_size=(1200, 400)).main_loop()

