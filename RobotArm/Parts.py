from random import gauss
import numpy as np


class SolidPart:
    def __init__(self,
                 surface,
                 surface_size,
                 surface_resistance,
                 part_id,
                 category='neutral',
                 color=None,
                 pixel_meter_ratio=None,
                 sample_rate=30,
                 noise_std_deviation=1,
                 main_state='start_state'):

        self.surface = surface
        self.surface_size = surface_size
        self.surface_resistance = surface_resistance
        self.part_id = part_id

        self.category = category

        if color is None:
            self.color = [255]*3
        else:
            self.color = color

        self.pixel_meter_ratio = pixel_meter_ratio
        self.sample_rate = sample_rate
        self.sample_period = 1/sample_rate

        self.noise_std_deviation = noise_std_deviation

        self.main_state = main_state

    def update_ref(self):
        pass

    @property
    def noise(self):
        return gauss(mu=0, sigma=self.noise_std_deviation)

    @property
    def sample_rate(self):
        return int(self._sample_rate)

    @sample_rate.setter
    def sample_rate(self, value):
        self._sample_rate = int(value)
        self._sample_period = 1/value

    @property
    def sample_period(self):
        return self._sample_period

    @sample_period.setter
    def sample_period(self, value):
        self._sample_period = value
        self._sample_rate = 1/value


class MasterPart(SolidPart):
    def __init__(self,
                 surface,
                 surface_size,
                 surface_resistance,
                 part_id,
                 category='leaver',
                 color=None,
                 pixel_meter_ratio=300,
                 sample_rate=30,
                 noise_std_deviation=1,
                 main_state='start_state',
                 init_theta=0,
                 init_phi=0,
                 init_R=300,
                 init_ref=None):

        super().__init__(surface,
                         surface_size,
                         surface_resistance,
                         part_id,
                         category=category,
                         color=color,
                         pixel_meter_ratio=pixel_meter_ratio,
                         sample_rate=sample_rate,
                         noise_std_deviation=noise_std_deviation,
                         main_state=main_state)

        self.dimension = 3

        self.R = init_R
        self._phi = init_phi
        self.r = self.R * np.sin(self._phi)
        self._theta = init_theta

        if init_ref is None:
            self._ref = [surface_size[0] // 2, surface_size[0] // 2, surface_size[1] // 2]
        else:
            self._ref = init_ref

        self.r = init_R * np.sin(init_phi)
        self.x = int(self.r * np.cos(init_theta) + self._ref[0])
        self.y = int(self.r * np.sin(init_theta) + self._ref[1])
        self.z = int(init_R * np.cos(init_phi) + self._ref[2])

    @property
    def ref(self):
        return self._ref

    @ref.setter
    def ref(self, value):
        self._ref = [int(i) for i in value]
        self.x = int(self.r * np.cos(self._theta) + value[0])
        self.y = int(self.r * np.sin(self._theta) + value[1])
        self.z = int(self.R * np.cos(self._phi) + value[2])

    @property
    def theta(self):
        return self._theta

    @theta.setter
    def theta(self, value):
        self._theta = value
        self.x = int(self.r * np.cos(value) + self._ref[0])
        self.y = int(self.r * np.sin(value) + self._ref[1])
        self.z = int(self.R * np.cos(self._phi) + self._ref[2])

    @property
    def phi(self):
        return self._phi

    @phi.setter
    def phi(self, value):
        self._phi = value
        self.r = self.R * np.sin(value)
        self.x = int(self.r * np.cos(self._theta) + self._ref[0])
        self.y = int(self.r * np.sin(self._theta) + self._ref[1])
        self.z = int(self.R * np.cos(value) + self._ref[2])


class SlavePart(SolidPart):
    def __init__(self,
                 master_part,
                 surface,
                 surface_size,
                 surface_resistance,
                 part_id,
                 category='slave',
                 color=None,
                 pixel_meter_ratio=300,
                 sample_rate=30,
                 noise_std_deviation=1,
                 main_state='start_state',
                 init_phi=0,
                 init_R=300):

        super().__init__(surface,
                         surface_size,
                         surface_resistance,
                         part_id,
                         category=category,
                         color=color,
                         pixel_meter_ratio=pixel_meter_ratio,
                         sample_rate=sample_rate,
                         noise_std_deviation=noise_std_deviation,
                         main_state=main_state)

        self.dimension = 3

        self.master = master_part

        self._phi = init_phi
        self.R = init_R
        self.r = self.R * np.sin(self._phi)
        self._theta = self.master.theta
        self._ref = [self.master.x, self.master.y, self.master.z]

        self.x = int(self.r * np.cos(self._theta) + self._ref[0])
        self.y = int(self.r * np.sin(self._theta) + self._ref[1])
        self.z = int(self.R * np.cos(self._phi) + self._ref[2])

    def update_ref(self):
        self._theta = self.master.theta
        self._ref = [self.master.x, self.master.y, self.master.z]
        self.x = int(self.r*np.cos(self._theta) + self._ref[0])
        self.y = int(self.r*np.sin(self._theta) + self._ref[1])
        self.z = int(self.R*np.cos(self._phi) + self._ref[2])

    @property
    def ref(self):
        return self._ref

    @ref.setter
    def ref(self, value):
        self._theta = self.master.theta
        self._ref = [int(i) for i in value]
        self.x = int(self.r * np.cos(self._theta) + value[0])
        self.y = int(self.r * np.sin(self._theta) + value[1])
        self.z = int(self.R * np.cos(self._phi) + value[2])

    @property
    def theta(self):
        return self._theta

    @property
    def phi(self):
        return self._phi

    @phi.setter
    def phi(self, value):
        self._theta = self.master.theta
        self._phi = value
        self._ref = [self.master.x, self.master.y, self.master.z]
        self.r = self.R * np.sin(value)
        self.x = int(self.r * np.cos(self._theta) + self._ref[0])
        self.y = int(self.r * np.sin(self._theta) + self._ref[1])
        self.z = int(self.R * np.cos(value) + self._ref[2])