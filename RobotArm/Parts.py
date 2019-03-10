from random import gauss
import numpy as np
from solids.Solids import *


class Part(SolidsGroup):
    def __init__(self,
                 solids_list=[],
                 origin=(0, 0, -5),
                 offset=(0, 0, 0),
                 axis=(0, 1, 0),
                 angle=np.pi/2,
                 length=1,
                 noise_std_deviation=0.1):

        self.noise_std_deviation = noise_std_deviation
        self.length = length

        super().__init__(solids_list=solids_list,
                         origin=origin,
                         offset=offset,
                         axis=axis,
                         angle=angle)

    @property
    def noise(self):
        return gauss(mu=0, sigma=self.noise_std_deviation)


class MasterPart(Part):
    def __init__(self,
                 origin=(0, 0, -5),
                 offset=(0, 0, 0),
                 axis=(0, 1, 0),
                 angle=np.pi/2,
                 length=1,
                 noise_std_deviation=0.1):

        self.noise_std_deviation = noise_std_deviation
        self.length = length
        self.solids_list = []

        super().__init__(solids_list=self.solids_list,
                         origin=origin,
                         offset=offset,
                         axis=axis,
                         angle=angle,
                         length=length,
                         noise_std_deviation=noise_std_deviation)


class SlavePart(Part):
    def __init__(self,
                 origin=(0, 0, -5),
                 offset=(0, 0, 0),
                 axis=(0, 1, 0),
                 angle=np.pi / 2,
                 length=1,
                 noise_std_deviation=0.1):

        self.noise_std_deviation = noise_std_deviation
        self.length = length
        self.solids_list = []

        super().__init__(solids_list=self.solids_list,
                         origin=origin,
                         offset=offset,
                         axis=axis,
                         angle=angle,
                         length=length,
                         noise_std_deviation=noise_std_deviation)

