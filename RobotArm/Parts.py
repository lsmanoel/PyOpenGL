from random import gauss
import numpy as np
from solids.Solids import *


class Part:
    def __init__(self,
                 origin=(0, 0, -5),
                 length=1,
                 theta=None,
                 theta_degree=None,
                 phi=None,
                 phi_degree=None,
                 noise_std_deviation=0.1):

        self._origin = np.asarray(origin, np.dtype('float64'))
        self.length = length
        self._theta = 0
        self._theta_degree = 0
        self._phi = 0
        self._phi_degree = 0
        self.r = length * np.sin(phi)
        self.x = int(self.r * np.cos(theta) + self._origin[0])
        self.z = int(self.r * np.sin(theta) + self._origin[1])
        self.y = int(length * np.cos(phi) + self._origin[2])

        self.noise_std_deviation = noise_std_deviation

        if theta is not None and theta_degree is None:
            self.theta = theta
        elif theta is None and theta_degree is not None:
            self.theta_degree = theta_degree

        if phi is not None and phi_degree is None:
            self.phi = phi
        elif phi is None and phi_degree is not None:
            self.phi_degree = phi_degree

    def draw(self, mode="spherical"):
        pass

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        self._origin = np.asarray(np.asarray(value, np.dtype('float64')))
        self.r = self.length * np.sin(self.phi)
        self.x = self.r * np.cos(self._theta) + self._origin[0]
        self.z = self.r * np.sin(self._theta) + self._origin[1]
        self.y = self.length * np.cos(self._phi) + self._origin[2]

    @property
    def theta(self):
        return self._theta

    @theta.setter
    def theta(self, value):
        self._theta = value
        if self._theta < 0:
            self._theta += 2*np.pi
        elif self._theta > 2*np.pi:
            self._theta -= 2*np.pi
        self._theta_degree = 180 * (value / np.pi)
        self.r = self.length * np.sin(self.phi)
        self.x = self.r * np.cos(self._theta) + self._origin[0]
        self.z = self.r * np.sin(self._theta) + self._origin[1]
        self.y = self.length * np.cos(self._phi) + self._origin[2]

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
        self.r = self.length * np.sin(self.phi)
        self.x = self.r * np.cos(self._theta) + self._origin[0]
        self.z = self.r * np.sin(self._theta) + self._origin[1]
        self.y = self.length * np.cos(self._phi) + self._origin[2]

    @property
    def phi(self):
        return self._phi

    @phi.setter
    def phi(self, value):
        self._phi = value
        if self._phi < 0:
            self._phi += 2 * np.pi
        elif self._phi > 2 * np.pi:
            self._phi -= 2 * np.pi
        self._phi_degree = 180 * (value / np.pi)
        self.r = self.length * np.sin(self.phi)
        self.x = self.r * np.cos(self._theta) + self._origin[0]
        self.z = self.r * np.sin(self._theta) + self._origin[1]
        self.y = self.length * np.cos(self._phi) + self._origin[2]

    @property
    def phi_degree(self):
        return self._phi_degree

    @phi_degree.setter
    def phi_degree(self, value):
        self._phi_degree = value
        if self._phi_degree < 0:
            self._phi_degree += 360
        elif self._phi_degree > 360:
            self._phi_degree -= 360
        self._phi = np.pi * (value / 180)
        self.r = self.length * np.sin(self.phi)
        self.x = self.r * np.cos(self._theta) + self._origin[0]
        self.z = self.r * np.sin(self._theta) + self._origin[1]
        self.y = self.length * np.cos(self._phi) + self._origin[2]

    @property
    def noise(self):
        return gauss(mu=0, sigma=self.noise_std_deviation)


class MasterPart(Part):
    def __init__(self,
                 origin=(0, 0, 0),
                 length=1,
                 theta=None,
                 theta_degree=None,
                 phi=None,
                 phi_degree=None,
                 noise_std_deviation=0.1):

        super().__init__(origin=origin,
                         theta=theta,
                         theta_degree=theta_degree,
                         phi=phi,
                         phi_degree=phi_degree,
                         length=length,
                         noise_std_deviation=noise_std_deviation)

        self.fixed_base_list = []

        self.fixed_base_list.append(Hexagon(color=(0.1, 0.1, 0.7),
                                            origin=(origin[0], origin[1], origin[2]),
                                            origin_offset=(0, 0, 0),
                                            axis=(0, 0, 0),
                                            theta=theta+np.pi/2,
                                            phi=0,
                                            size=(2, 0.10)))

        self.fixed_base_list.append(Hexagon(color=(0.1, 0.1, 0.7),
                                            origin=(origin[0], origin[1], origin[2]),
                                            origin_offset=(0, 0.5, 0),
                                            axis=(0, 0, 0),
                                            theta=theta+np.pi/2,
                                            phi=0,
                                            size=(1.5, 0.10)))

        self.base_list = []

        self.base_list.append(Hexagon(color=(0.1, 0.1, 0.7),
                                      origin=(origin[0], origin[1], origin[2]),
                                      origin_offset=(0, 0.61, 0),
                                      axis=(0, 0, 0),
                                      theta=theta+np.pi/2,
                                      phi=0,
                                      size=(0.9, 0.10)))

        self.base_list.append(Hexagon(color=(0.1, 0.1, 0.7),
                                      origin=(origin[0], origin[1], origin[2]),
                                      origin_offset=(0, 0.8, 0),
                                      axis=(0, 0, 0),
                                      theta=theta+np.pi/2,
                                      phi=0,
                                      size=(1.1, 0.40)))

        self.stalks_list = []

        y_stalk_origin = 1.3

        self.stalks_list.append(Hexagon(color=(0.1, 0.1, 0.7),
                                        origin=(origin[0], origin[1]+y_stalk_origin, origin[2]),
                                        origin_offset=(0, 0, 0),
                                        origin_axis=(0, 0, 1),
                                        axis=(0, 0, 0),
                                        size=(0.5, 0.25)))

        self.stalks_list.append(Trapezoid(color=(0.1, 0.1, 0.7),
                                          origin=(origin[0], origin[1]+y_stalk_origin, origin[2]),
                                          origin_offset=(1, 0, 0),
                                          axis=(0, 0, 0),
                                          theta=theta,
                                          size=(1.6, 1.6, 1.7, 1.7, 0.45, 0.25)))

        self.stalks_list.append(HexagonStalk(color=(0.1, 0.1, 0.9),
                                             origin=(origin[0], origin[1]+y_stalk_origin, origin[2]),
                                             origin_offset=(0, -0.25, -0.15),
                                             axis=(0, 0, 0),
                                             theta=theta,
                                             size=(0.1, 2)))

        self.stalks_list.append(HexagonStalk(color=(0.1, 0.1, 0.9),
                                             origin=(origin[0], origin[1]+y_stalk_origin, origin[2]),
                                             origin_offset=(0, -0.25, 0.15),
                                             axis=(0, 0, 0),
                                             theta=theta,
                                             size=(0.1, 2)))

        self.stalks_list.append(HexagonStalk(color=(0.1, 0.1, 0.9),
                                             origin=(origin[0], origin[1]+y_stalk_origin, origin[2]),
                                             origin_offset=(0, 0.25, -0.15),
                                             axis=(0, 0, 0),
                                             theta=theta,
                                             size=(0.1, 2)))

        self.stalks_list.append(HexagonStalk(color=(0.1, 0.1, 0.9),
                                             origin=(origin[0], origin[1]+y_stalk_origin, origin[2]),
                                             origin_offset=(0, 0.25, 0.15),
                                             axis=(0, 0, 0),
                                             theta=theta,
                                             size=(0.1, 2)))

    def draw(self, mode=None):

        for solid in self.fixed_base_list:
            solid.draw(mode)

        for solid in self.base_list:
            # solid.phi = np.pi/2
            solid.theta = self.theta+np.pi/2
            solid.draw(mode)

        for solid in self.stalks_list:
            solid.phi = self.phi
            solid.theta = self.theta
            solid.draw(mode)


class SlavePart(Part):
    def __init__(self,
                 origin=(0, 0, -5),
                 theta=None,
                 theta_degree=None,
                 phi=None,
                 phi_degree=None,
                 length=1,
                 noise_std_deviation=0.1):

        self.noise_std_deviation = noise_std_deviation
        self.length = length

        self.solids_list = []

        super().__init__(origin=origin,
                         theta=theta,
                         theta_degree=theta_degree,
                         phi=phi,
                         phi_degree=phi_degree,
                         length=length,
                         noise_std_deviation=noise_std_deviation)

