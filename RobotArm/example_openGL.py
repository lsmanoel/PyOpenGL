import pygame
from pygame.locals import *
import numpy as np
from RobotArm.Parts import MasterPart, SlavePart
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

        # self.screen_array = pygame.surfarray.pixels3d(self.screen)

        self.main_state = 'run_state'
        self.close_app = False
        self.clock = pygame.time.Clock()

        self.image_set_path = 'sprites'
        self.hand_image_name = 'hand_1.png'
        self.hand_image_path = os.path.join(self.image_set_path, self.hand_image_name)
        self.hand_sprite = pygame.image.load(self.hand_image_path)
        self.hand_sprite = pygame.transform.scale(self.hand_sprite,
                                                  (self.hand_sprite.get_width()//4,
                                                   self.hand_sprite.get_height()//4))

        # --------------------------------------------------------------------------------------------------------------
        self.part_list = []

        self.part_list.append(MasterPart(None,
                                         (screen_size[0]//3, screen_size[1]),
                                         None,
                                         'master',
                                         init_ref=[screen_size[0]//6, screen_size[1]//2, 0],
                                         init_theta=0,
                                         init_phi=np.pi/5,
                                         init_R=75))

        self.part_list.append(SlavePart(self.part_list[-1],
                                        None,
                                        (screen_size[0]//3, screen_size[1]),
                                        None,
                                        'slave',
                                        init_phi=2*np.pi/3,
                                        init_R=60))

        self.part_list.append(SlavePart(self.part_list[-1],
                                        None,
                                        (screen_size[0]//3, screen_size[1]),
                                        None,
                                        'slave',
                                        color=(255, 255, 0),
                                        init_phi=np.pi/2,
                                        init_R=40))

        main_thread = threading.Thread(target=self.main_loop)
        main_thread.start()

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
                self.part_list[1].master.phi -= 0.1
                self.part_list[1].update_ref()
                self.part_list[2].update_ref()
            if pressed[pygame.K_DOWN]:
                self.part_list[1].master.phi += 0.1
                self.part_list[1].update_ref()
                self.part_list[2].update_ref()
            if pressed[pygame.K_LEFT]:
                self.part_list[1].master.theta -= 0.1
                self.part_list[1].update_ref()
                self.part_list[2].update_ref()
            if pressed[pygame.K_RIGHT]:
                self.part_list[1].master.theta += 0.1
                self.part_list[1].update_ref()
                self.part_list[2].update_ref()
            if pressed[pygame.K_w]:
                self.part_list[1].phi -= 0.1
                self.part_list[2].update_ref()
            if pressed[pygame.K_s]:
                self.part_list[1].phi += 0.1
                self.part_list[2].update_ref()

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

        if self.main_state == 'start_state':
            pass

        elif self.main_state == 'run_state':
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            pygame.draw.rect(self.screen, (0, 255, 255), [0,
                                                          0,
                                                          self.screen_size[0]//3,
                                                          self.screen_size[1]], 2)

            pygame.draw.rect(self.screen, (0, 255, 255), [self.screen_size[0]//3,
                                                          0,
                                                          2*self.screen_size[0]//6,
                                                          self.screen_size[1]], 2)

            for part in self.part_list:
                # ------------------------------------------------------------------------------------------------------
                pygame.draw.circle(self.screen,
                                   part.color,
                                   [part.ref[0], 7*self.screen_size[1]//10 - part.ref[2]],
                                   5)

                pygame.draw.aaline(self.screen,
                                   part.color,
                                   [part.ref[0], 7*self.screen_size[1]//10 - part.ref[2]],
                                   [part.x, 7*self.screen_size[1]//10 - part.z],
                                   True)

                pygame.draw.circle(self.screen,
                                   (0, 255, 0),
                                   [part.ref[0], 7*self.screen_size[1]//10 - part.ref[2]],
                                   part.R,
                                   1)

                # ------------------------------------------------------------------------------------------------------
                pygame.draw.circle(self.screen,
                                   part.color,
                                   [self.screen_size[0]//3+part.ref[1], 7*self.screen_size[1]//10 - part.ref[2]],
                                   5)

                pygame.draw.aaline(self.screen,
                                   part.color,
                                   [self.screen_size[0]//3+part.ref[1], 7*self.screen_size[1]//10 - part.ref[2]],
                                   [self.screen_size[0]//3+part.y, 7*self.screen_size[1]//10 - part.z],
                                   True)

        pygame.display.flip()


# ======================================================================================================================
screen_1 = PgScreen(screen_size=(1200, 400))
