import numpy as np
from OpenGL.GL import *


class Solids:
    def __init__(self,
                 vertices=None,
                 edges=None,
                 surfaces=None,
                 color=None,
                 color_offset=(0, 0, 0),
                 origin=(0, 0, 0),
                 origin_offset=(0, 0, 0),
                 axis=(0, 1, 0),
                 axis_offset=(0, 1, 0),
                 theta=None,
                 theta_offset=None,
                 theta_degree=None,
                 theta_degree_offset=None,
                 phi=None,
                 phi_offset=None,
                 phi_degree=None,
                 phi_degree_offset=None,
                 size=None,
                 size_offset=None):

        self._origin = np.asarray(origin, np.dtype('float64'))
        self._origin_offset = np.asarray(origin_offset, np.dtype('float64'))
        self._axis = np.asarray(axis, np.dtype('float64'))
        self._axis_offset = np.asarray(axis_offset, np.dtype('float64'))

        self.origin_vertices = vertices
        self.vertices = vertices
        if vertices is not None:
            for i, vertex in enumerate(self.origin_vertices):
                self.vertices[i][:] = [vertex[0] + self._origin_offset[0],
                                       vertex[1] + self._origin_offset[1],
                                       vertex[2] + self._origin_offset[2]]

        self.edges = edges
        self.surface = surfaces

        self.color = np.asarray(color)
        self.color_offset = np.asarray(color_offset)
        self.size = size
        self.size_offset = size_offset

        self._theta = 0
        self._theta_offset = 0
        self._theta_degree = 0
        self._theta_degree_offset = 0
        self._phi = 0
        self._phi_offset = 0
        self._phi_degree = 0
        self._phi_degree_offset = 0

        if theta is not None and theta_degree is None:
            self.theta = theta
        elif theta is None and theta_degree is not None:
            self.theta_degree = theta_degree

        if theta_offset is not None and theta_degree_offset is None:
            self.theta_offset = theta_offset
        elif theta is None and theta_degree is not None:
            self.theta_degree_offset = theta_degree_offset

        if phi is not None and phi_degree is None:
            self.phi = phi
        elif phi is None and phi_degree is not None:
            self.phi_degree = phi_degree

        if phi_offset is not None and phi_degree_offset is None:
            self.phi_offset = phi_offset
        elif phi is None and phi_degree is not None:
            self.phi_degree_offset = phi_degree_offset

    def draw(self, mode=None):
        glPushMatrix()

        self._translate()
        self._rotate(mode)

        if self.vertices is not None and self.edges is not None:
            self._draw_edges()
            if self.surface is not None:
                self._draw_surfaces()
        glPopMatrix()

    def _draw_edges(self):
        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                if self.color is not None:
                    glColor3fv((0, 0, 0))
                glVertex3fv(self.vertices[vertex])
        glEnd()

    def _draw_surfaces(self):
        glBegin(GL_QUADS)
        for surface in self.surface:
            for vertex in surface:
                if self.color is not None:
                    glColor3fv(self.color + self.color_offset)
                glVertex3fv(self.vertices[vertex])
        glEnd()

    def _translate(self):
        glTranslatef(self._origin[0], self._origin[1], self._origin[2])

    def _rotate(self, mode=None):
        if mode == "spherical":
            glRotatef(self._theta_degree + self._theta_degree_offset, 0, 1, 0)
            glRotatef(self._phi_degree + self._phi_degree_offset, 0, 0, 1)
        else:
            glRotatef(self._theta_degree + self._theta_degree_offset,
                      self._axis[0] + self._axis_offset[0],
                      self._axis[1] + self._axis_offset[1],
                      self._axis[2] + self._axis_offset[2])

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = np.asarray(value)

    @property
    def color_offset(self):
        return self._color_offset

    @color_offset.setter
    def color_offset(self, value):
        self._color_offset = np.asarray(value)

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        self._origin = np.asarray(np.asarray(value, np.dtype('float64')))

    @property
    def origin_offset(self):
        return self._origin_offset

    @origin_offset.setter
    def origin_offset(self, value):
        self._origin_offset = np.asarray(value, np.dtype('float64'))
        for i, vertex in enumerate(self.origin_vertices):
            self.vertices[i][:] = [vertex[0]+self._origin_offset[0],
                                   vertex[1]+self._origin_offset[1],
                                   vertex[2]+self._origin_offset[2]]

    @property
    def axis(self):
        return self._axis

    @axis.setter
    def axis(self, value):
        self._axis = np.asarray(value, np.dtype('float64'))

    @property
    def axis_offset(self):
        return self._axis_offset

    @axis_offset.setter
    def axis_offset(self, value):
        self._axis_offset = np.asarray(value, np.dtype('float64'))

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

    @property
    def theta_offset(self):
        return self._theta_offset

    @theta_offset.setter
    def theta_offset(self, value):
        self._theta_offset = value
        if self._theta_offset < 0:
            self._theta_offset += 2*np.pi
        elif self._theta_offset > 2*np.pi:
            self._theta_offset -= 2*np.pi
        self._theta_degree_offset = 180 * (value / np.pi)

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

    @property
    def theta_degree_offset(self):
        return self._theta_degree_offset

    @theta_degree_offset.setter
    def theta_degree_offset(self, value):
        self._theta_degree_offset = value
        if self._theta_degree_offset < 0:
            self._theta_degree_offset += 360
        elif self._theta_degree_offset > 360:
            self._theta_degree_offset -= 360
        self._theta_offset = np.pi * (value / 180)

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

    @property
    def phi_offset(self):
        return self._phi_offset

    @phi_offset.setter
    def phi_offset(self, value):
        self._phi_offset = value
        if self._phi_offset < 0:
            self._phi_offset += 2 * np.pi
        elif self._phi_offset > 2 * np.pi:
            self._phi_offset -= 2 * np.pi
        self._phi_degree_offset = 180 * (value / np.pi)

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

    @property
    def phi_degree_offset(self):
        return self._phi_degree_offset

    @phi_degree_offset.setter
    def phi_degree_offset(self, value):
        self._phi_degree_offset = value
        if self._phi_degree_offset < 0:
            self._phi_degree_offset += 360
        elif self._phi_degree_offset > 360:
            self._phi_degree_offset -= 360
        self._phi_offset = np.pi * (value / 180)


class Pyramid(Solids):
    def __init__(self,
                 color=(1, 1, 1),
                 color_offset=(0, 0, 0),
                 origin=(0, 0, 0),
                 origin_offset=(0, 0, 0),
                 axis=(0, 1, 0),
                 axis_offset=(0, 1, 0),
                 theta=None,
                 theta_offset=None,
                 theta_degree=None,
                 theta_degree_offset=None,
                 phi=None,
                 phi_offset=None,
                 phi_degree=None,
                 phi_degree_offset=None,
                 size=(0.5, 0.3, 0.5),
                 size_offset=(0, 0, 0)):  # size = (x, y, z)

        vertices = np.array([[-size[0]/2+size_offset[0], -size[1]/2+size_offset[1], +size[2]/2+size_offset[2]],  # 0
                             [-size[0]/2+size_offset[0], -size[1]/2+size_offset[1], -size[2]/2+size_offset[2]],  # 1
                             [+size[0]/2+size_offset[0], -size[1]/2+size_offset[1], -size[2]/2+size_offset[2]],  # 2
                             [+size[0]/2+size_offset[0], -size[1]/2+size_offset[1], +size[2]/2+size_offset[2]],  # 3
                             [size_offset[0], size[1]/2+size_offset[1], size_offset[2]],  # 4
                             [size_offset[0], size[1]/2+size_offset[1], size_offset[2]]])  # 5

        '''


                  4=5 __y
                 /|\  
                / | \    
               /  |  \    
              /   |   \     
             /__  |  __\ 2 __-z   
            / 1   |    / 
           /      |   /     
          /       |  /
         /        | /   
        0__ ______|/ 3
                 /                   
                x                            
        '''

        edges = np.array([[0, 1],  # 0
                          [1, 4],  # 1
                          [4, 5],  # 2
                          [5, 0],  # 3
                          [0, 3],  # 4
                          [3, 4],  # 5
                          [3, 2],  # 6
                          [2, 5],  # 7
                          [2, 1]])  # 8

        surfaces = ((0, 1, 4, 5),
                    (0, 3, 4, 5),
                    (3, 2, 4, 5),
                    (2, 1, 4, 5),
                    (0, 1, 2, 3))

        super().__init__(vertices=vertices,
                         edges=edges,
                         surfaces=surfaces,
                         color=color,
                         color_offset=color_offset,
                         origin=origin,
                         origin_offset=origin_offset,
                         axis=axis,
                         axis_offset=axis_offset,
                         theta=theta,
                         theta_offset=theta_offset,
                         theta_degree=theta_degree,
                         theta_degree_offset=theta_degree_offset,
                         phi=phi,
                         phi_offset=phi_offset,
                         phi_degree=phi_degree,
                         phi_degree_offset=phi_degree_offset,
                         size=size,
                         size_offset=size_offset)


class Cube(Solids):
    def __init__(self,
                 color=(1, 1, 1),
                 color_offset=(0, 0, 0),
                 origin=(0, 0, 0),
                 origin_offset=(0, 0, 0),
                 axis=(0, 1, 0),
                 axis_offset=(0, 0, 0),
                 theta=None,
                 theta_offset=None,
                 theta_degree=None,
                 theta_degree_offset=None,
                 phi=None,
                 phi_offset=None,
                 phi_degree=None,
                 phi_degree_offset=None,
                 size=0.6,
                 size_offset=0):

        vertices = np.array([[-size/2+size_offset, -size/2+size_offset, +size/2+size_offset],
                             [-size/2+size_offset, +size/2+size_offset, +size/2+size_offset],
                             [+size/2+size_offset, +size/2+size_offset, +size/2+size_offset],
                             [+size/2+size_offset, -size/2+size_offset, +size/2+size_offset],
                             [-size/2+size_offset, -size/2+size_offset, -size/2+size_offset],
                             [-size/2+size_offset, +size/2+size_offset, -size/2+size_offset],
                             [+size/2+size_offset, +size/2+size_offset, -size/2+size_offset],
                             [+size/2+size_offset, -size/2+size_offset, -size/2+size_offset]])
        '''
               5____________6
               /           /|
              /           / |
        y__ 1/__________2/  |
            |           |   |  
            |   |__     |   | __-z
        0__ |   4       |   7   
            |  /        |  /__0
            |           | /
        -y__0___________3/__z  
            /     /     /
          -x     0     x
        '''

        edges = np.array([[0, 1],
                          [0, 3],
                          [0, 4],
                          [2, 1],
                          [2, 3],
                          [2, 6],
                          [5, 1],
                          [5, 4],
                          [5, 6],
                          [7, 3],
                          [7, 4],
                          [7, 6]])

        surfaces = ((0, 1, 2, 3),
                    (3, 2, 6, 7),
                    (7, 6, 5, 4),
                    (4, 5, 1, 0),
                    (1, 5, 6, 2),
                    (4, 0, 3, 7))

        super().__init__(vertices=vertices,
                         edges=edges,
                         surfaces=surfaces,
                         color=color,
                         color_offset=color_offset,
                         origin=origin,
                         origin_offset=origin_offset,
                         axis=axis,
                         axis_offset=axis_offset,
                         theta=theta,
                         theta_offset=theta_offset,
                         theta_degree=theta_degree,
                         theta_degree_offset=theta_degree_offset,
                         phi=phi,
                         phi_offset=phi_offset,
                         phi_degree=phi_degree,
                         phi_degree_offset=phi_degree_offset,
                         size=size,
                         size_offset=size_offset)


class Parallelepiped(Solids):
    def __init__(self,
                 color=(1, 1, 1),
                 color_offset=(0, 0, 0),
                 origin=(0, 0, 0),
                 origin_offset=(0, 0, 0),
                 axis=(0, 1, 0),
                 axis_offset=(0, 0, 0),
                 theta=None,
                 theta_offset=None,
                 theta_degree=None,
                 theta_degree_offset=None,
                 phi=None,
                 phi_offset=None,
                 phi_degree=None,
                 phi_degree_offset=None,
                 alpha=np.pi/2,
                 size=(0.5, 0.7, 0.2),
                 size_offset=(0, 0, 0)):  # size = (x, y, z)

        vertices = np.array([[-size[0]/2+size_offset[0], -size[1]/2+size_offset[1], +size[2]/2+size_offset[2]],   # 0
                             [-size[0]/2+size_offset[0], +size[1]/2+size_offset[1], +size[2]/2+size_offset[2]],   # 1
                             [+size[0]/2+size_offset[0], +size[1]/2+size_offset[1], +size[2]/2+size_offset[2]],   # 2
                             [+size[0]/2+size_offset[0], -size[1]/2+size_offset[1], +size[2]/2+size_offset[2]],   # 3
                             [-size[0]/2+size_offset[0], -size[1]/2+size_offset[1], -size[2]/2+size_offset[2]],   # 4
                             [-size[0]/2+size_offset[0], +size[1]/2+size_offset[1], -size[2]/2+size_offset[2]],   # 5
                             [+size[0]/2+size_offset[0], +size[1]/2+size_offset[1], -size[2]/2+size_offset[2]],   # 6
                             [+size[0]/2+size_offset[0], -size[1]/2+size_offset[1], -size[2]/2+size_offset[2]]])  # 7

        slope = size[1]/np.tan(alpha)

        vertices[1, 0] += slope
        vertices[2, 0] += slope
        vertices[5, 0] += slope
        vertices[6, 0] += slope
        '''
               5____________6                            5___________6            
               /           /|                           /           /
              /           / |                          /           / 
        y__ 1/__________2/  |           slope--> y__ 1/__________2/   
            |           |   |                        /           /   
            |           |   |                       /           /   
            |           |   |                      /           /   np.pi/2
            |           |   |                     /           /   
            |           |   |                    /           /     
            |   |__     |   | __-z              /__         /__-z 
            |   4       |   7                  /4          / 7    
            |  /        |  /                  /           /
            |           | /                  /\ alpha    / 
            0___________3/                  0__)________3  
                        /                               /
                       x                                x
        '''

        edges = np.array([[0, 1],
                          [0, 3],
                          [0, 4],
                          [2, 1],
                          [2, 3],
                          [2, 6],
                          [5, 1],
                          [5, 4],
                          [5, 6],
                          [7, 3],
                          [7, 4],
                          [7, 6]])

        surfaces = ((0, 1, 2, 3),
                    (3, 2, 6, 7),
                    (7, 6, 5, 4),
                    (4, 5, 1, 0),
                    (1, 5, 6, 2),
                    (4, 0, 3, 7))

        super().__init__(vertices=vertices,
                         edges=edges,
                         surfaces=surfaces,
                         color=color,
                         color_offset=color_offset,
                         origin=origin,
                         origin_offset=origin_offset,
                         axis=axis,
                         axis_offset=axis_offset,
                         theta=theta,
                         theta_offset=theta_offset,
                         theta_degree=theta_degree,
                         theta_degree_offset=theta_degree_offset,
                         phi=phi,
                         phi_offset=phi_offset,
                         phi_degree=phi_degree,
                         phi_degree_offset=phi_degree_offset,
                         size=size,
                         size_offset=size_offset)


class Trapezoid(Solids):
    def __init__(self,
                 color=(1, 1, 1),
                 color_offset=(0, 0, 0),
                 origin=(0, 0, 0),
                 origin_offset=(0, 0, 0),
                 axis=(0, 1, 0),
                 axis_offset=(0, 0, 0),
                 theta=None,
                 theta_offset=None,
                 theta_degree=None,
                 theta_degree_offset=None,
                 phi=None,
                 phi_offset=None,
                 phi_degree=None,
                 phi_degree_offset=None,
                 size=(0.5, 0.5, 0.2, 0.3, 0.2, 0.3),
                 size_offset=(0, 0, 0)):  # size = (x1_b, x2_b, x1_t, x2_t, y, z)

        vertices = np.array([[-size[0]/2+size_offset[0], -size[4]/2+size_offset[1], +size[5]/2+size_offset[2]],   # 0
                             [-size[2]/2+size_offset[0], +size[4]/2+size_offset[1], +size[5]/2+size_offset[2]],   # 1
                             [+size[3]/2+size_offset[0], +size[4]/2+size_offset[1], +size[5]/2+size_offset[2]],   # 2
                             [+size[1]/2+size_offset[0], -size[4]/2+size_offset[1], +size[5]/2+size_offset[2]],   # 3
                             [-size[0]/2+size_offset[0], -size[4]/2+size_offset[1], -size[5]/2+size_offset[2]],   # 4
                             [-size[2]/2+size_offset[0], +size[4]/2+size_offset[1], -size[5]/2+size_offset[2]],   # 5
                             [+size[3]/2+size_offset[0], +size[4]/2+size_offset[1], -size[5]/2+size_offset[2]],   # 6
                             [+size[1]/2+size_offset[0], -size[4]/2+size_offset[1], -size[5]/2+size_offset[2]]])  # 7

        '''
               5____________6                            5___________6 <--x2_t                   5=6
               /           /|                           /           /\                          /\
              /           / |                          /           /  \                        /  \
        y__ 1/__________2/  |            x1_t--> y__ 1/__________2/    \                      /    \ 
            |           |   |                        /            \     \                    /\1=2  \
            |           |   |                       /              \     \                  /  \     \
            |           |   |                      /                \     \                /    \     \
            |           |   |                     /                  \     \              /      \     \
            |           |   |                    /                    \     \            /        \     \
            |   |__     |   | __-z              /__                    \   __\  __-z    /___       \   __\  __-z
            |   4       |   7                  /4                       \     7        /4           \     7   
            |  /        |  /                  /                          \   /        /              \   /
            |           | /                  /\ alpha               beta /\ /        /\ alpha   beta /\ /
            0___________3/          x1_b--> 0__)________________________(__3        0__)____________(__3 <--x2_b
                        /                                                 /                           /
                       x                                                 x                           x
        '''

        edges = np.array([[0, 1],
                          [0, 3],
                          [0, 4],
                          [2, 1],
                          [2, 3],
                          [2, 6],
                          [5, 1],
                          [5, 4],
                          [5, 6],
                          [7, 3],
                          [7, 4],
                          [7, 6]])

        surfaces = ((0, 1, 2, 3),
                    (3, 2, 6, 7),
                    (7, 6, 5, 4),
                    (4, 5, 1, 0),
                    (1, 5, 6, 2),
                    (4, 0, 3, 7))

        super().__init__(vertices=vertices,
                         edges=edges,
                         surfaces=surfaces,
                         color=color,
                         color_offset=color_offset,
                         origin=origin,
                         origin_offset=origin_offset,
                         axis=axis,
                         axis_offset=axis_offset,
                         theta=theta,
                         theta_offset=theta_offset,
                         theta_degree=theta_degree,
                         theta_degree_offset=theta_degree_offset,
                         phi=phi,
                         phi_offset=phi_offset,
                         phi_degree=phi_degree,
                         phi_degree_offset=phi_degree_offset,
                         size=size,
                         size_offset=size_offset)


class PyramidTrunk(Solids):
    def __init__(self,
                 color=(1, 1, 1),
                 color_offset=(0, 0, 0),
                 origin=(0, 0, 0),
                 origin_offset=(0, 0, 0),
                 axis=(0, 1, 0),
                 axis_offset=(0, 0, 0),
                 theta=None,
                 theta_offset=None,
                 theta_degree=None,
                 theta_degree_offset=None,
                 phi=None,
                 phi_offset=None,
                 phi_degree=None,
                 phi_degree_offset=None,
                 size=(0.5, 0.3, 0.5, 0.3, 0.2),
                 size_offset=(0, 0, 0)):  # size = (x, y, z, x, y)

        vertices = np.array([[-size[0]/2+size_offset[0], -size[1]/2+size_offset[1], +size[2]/2+size_offset[2]],   # 0
                             [-size[3]/2+size_offset[0], +size[1]/2+size_offset[1], +size[4]/2+size_offset[2]],   # 1
                             [+size[3]/2+size_offset[0], +size[1]/2+size_offset[1], +size[4]/2+size_offset[2]],   # 2
                             [+size[0]/2+size_offset[0], -size[1]/2+size_offset[1], +size[2]/2+size_offset[2]],   # 3
                             [-size[0]/2+size_offset[0], -size[1]/2+size_offset[1], -size[2]/2+size_offset[2]],   # 4
                             [-size[3]/2+size_offset[0], +size[1]/2+size_offset[1], -size[4]/2+size_offset[2]],   # 5
                             [+size[3]/2+size_offset[0], +size[1]/2+size_offset[1], -size[4]/2+size_offset[2]],   # 6
                             [+size[0]/2+size_offset[0], -size[1]/2+size_offset[1], -size[2]/2+size_offset[2]]])  # 7
        '''
               5____________6                                                    
               /           /|                           5___________6                         
              /           / |                          /           /\                          
        y__ 1/__________2/  |                    y__ 1/__________2/  \                  y__ 1=2=5=6   
            |           |   |                        /           |    \                   /|\  
            |           |   |                       /            |     \                 / | \    
            |           |   |                      /             |      \ __-z          /  |  \    
            |           |   |                     /___           |      |7             /   |   \     
            |           |   |                    / 4             |      /             /    |    \    
            |   |__     |   | __-z              /                |     /             /___  |    /\ __-z
            |   4       |   7                  /                 |    /             /4     |    |7   
            |  /        |  /                  /                  |   /             /       |   /
            |           | /                  /\                 /|\ /             /\      /|\ /   
            0___________3/__z               0__)_______________(_|3              0__)____( |3
                        /                                                                    /                   
                       x                                                                    x                           
        '''

        edges = np.array([[0, 1],
                          [0, 3],
                          [0, 4],
                          [2, 1],
                          [2, 3],
                          [2, 6],
                          [5, 1],
                          [5, 4],
                          [5, 6],
                          [7, 3],
                          [7, 4],
                          [7, 6]])

        surfaces = ((0, 1, 2, 3),
                    (3, 2, 6, 7),
                    (7, 6, 5, 4),
                    (4, 5, 1, 0),
                    (1, 5, 6, 2),
                    (4, 0, 3, 7))

        super().__init__(vertices=vertices,
                         edges=edges,
                         surfaces=surfaces,
                         color=color,
                         color_offset=color_offset,
                         origin=origin,
                         origin_offset=origin_offset,
                         axis=axis,
                         axis_offset=axis_offset,
                         theta=theta,
                         theta_offset=theta_offset,
                         theta_degree=theta_degree,
                         theta_degree_offset=theta_degree_offset,
                         phi=phi,
                         phi_offset=phi_offset,
                         phi_degree=phi_degree,
                         phi_degree_offset=phi_degree_offset,
                         size=size,
                         size_offset=size_offset)


class Hexagon(Solids):
    def __init__(self,
                 color=(1, 1, 1),
                 color_offset=(0, 0, 0),
                 origin=(0, 0, 0),
                 origin_offset=(0, 0, 0),
                 origin_axis=(0, 1, 0),
                 axis=(0, 1, 0),
                 axis_offset=(0, 0, 0),
                 theta=None,
                 theta_offset=None,
                 theta_degree=None,
                 theta_degree_offset=None,
                 phi=None,
                 phi_offset=None,
                 phi_degree=None,
                 phi_degree_offset=None,
                 size=(0.5, 0.2),
                 size_offset=(0, 0)):

        higher_hexagon = size[0]*np.sin(np.pi / 3)
        side_hexagon = size[0]*np.cos(np.pi/3)

        '''
             side_hexagon                           side_hexagon
        ____|_______|_____                         |_______|_
        |  / \      \  |                            \     |
        | /   \     |\ |  higher_hexagon/2           \    |
        |/_____\____|_\|__                       size \   | higher_hexagon
        |\    size  | /|                               \  |
        | \       \ |/ |                                \ |
        |__\_______\/__|                                 \|__
        '''
        if origin_axis == (1, 0, 0):
            vertices = np.array([[+size[1]/2+size_offset[0],
                                  -side_hexagon/2+size_offset[1],
                                  +higher_hexagon/2+size_offset[0]],   # 0
                                 [-size[1]/2+size_offset[0],
                                  -side_hexagon/2+size_offset[1],
                                  +higher_hexagon/2+size_offset[0]],   # 1
                                 [-size[1]/2+size_offset[0],
                                  +side_hexagon/2+size_offset[1],
                                  +higher_hexagon/2+size_offset[0]],   # 2
                                 [+size[1]/2+size_offset[0],
                                  +side_hexagon/2+size_offset[1],
                                  +higher_hexagon/2+size_offset[0]],   # 3
                                 [+size[1]/2+size_offset[0],
                                  -side_hexagon/2+size_offset[1],
                                  -higher_hexagon/2+size_offset[0]],   # 4
                                 [-size[1]/2+size_offset[0],
                                  -side_hexagon/2+size_offset[1],
                                  -higher_hexagon/2+size_offset[0]],   # 5
                                 [-size[1]/2+size_offset[0],
                                  +side_hexagon/2+size_offset[1],
                                  -higher_hexagon/2+size_offset[0]],   # 6
                                 [+size[1]/2+size_offset[0],
                                  +side_hexagon/2+size_offset[1],
                                  -higher_hexagon/2+size_offset[0]],   # 7
                                 [+size[1]/2+size_offset[0], -size[0]/2+size_offset[1], size_offset[0]],    # 8
                                 [-size[1]/2+size_offset[0], -size[0]/2+size_offset[1], size_offset[0]],    # 9
                                 [-size[1]/2+size_offset[0], +size[0]/2+size_offset[1], size_offset[0]],    # 10
                                 [+size[1]/2+size_offset[0], +size[0]/2+size_offset[1], size_offset[0]]])   # 11
        elif origin_axis == (0, 1, 0):
            vertices = np.array([[-side_hexagon/2+size_offset[0],
                                  -size[1]/2+size_offset[1],
                                  +higher_hexagon/2+size_offset[0]],   # 0
                                 [-side_hexagon/2+size_offset[0],
                                  +size[1]/2+size_offset[1],
                                  +higher_hexagon/2+size_offset[0]],   # 1
                                 [+side_hexagon/2+size_offset[0],
                                  +size[1]/2+size_offset[1],
                                  +higher_hexagon/2+size_offset[0]],   # 2
                                 [+side_hexagon/2+size_offset[0],
                                  -size[1]/2+size_offset[1],
                                  +higher_hexagon/2+size_offset[0]],   # 3
                                 [-side_hexagon/2+size_offset[0],
                                  -size[1]/2+size_offset[1],
                                  -higher_hexagon/2+size_offset[0]],   # 4
                                 [-side_hexagon/2+size_offset[0],
                                  +size[1]/2+size_offset[1],
                                  -higher_hexagon/2+size_offset[0]],   # 5
                                 [+side_hexagon/2+size_offset[0],
                                  +size[1]/2+size_offset[1],
                                  -higher_hexagon/2+size_offset[0]],   # 6
                                 [+side_hexagon/2+size_offset[0],
                                  -size[1]/2+size_offset[1],
                                  -higher_hexagon/2+size_offset[0]],   # 7
                                 [-size[0]/2+size_offset[0], -size[1]/2+size_offset[1], size_offset[0]],    # 8
                                 [-size[0]/2+size_offset[0], +size[1]/2+size_offset[1], size_offset[0]],    # 9
                                 [+size[0]/2+size_offset[0], +size[1]/2+size_offset[1], size_offset[0]],    # 10
                                 [+size[0]/2+size_offset[0], -size[1]/2+size_offset[1], size_offset[0]]])   # 11
        elif origin_axis == (0, 0, 1):
            vertices = np.array([[-side_hexagon/2+size_offset[0],
                                  -higher_hexagon/2+size_offset[1],
                                  -size[1]/2+size_offset[0]],   # 0
                                 [-side_hexagon/2+size_offset[0],
                                  -higher_hexagon/2+size_offset[1],
                                  +size[1]/2+size_offset[0]],   # 1
                                 [+side_hexagon/2+size_offset[0],
                                  -higher_hexagon/2+size_offset[1],
                                  +size[1]/2+size_offset[0]],   # 2
                                 [+side_hexagon/2+size_offset[0],
                                  -higher_hexagon/2+size_offset[1],
                                  -size[1]/2+size_offset[0]],   # 3
                                 [-side_hexagon/2+size_offset[0],
                                  +higher_hexagon/2+size_offset[1],
                                  -size[1]/2+size_offset[0]],   # 4
                                 [-side_hexagon/2+size_offset[0],
                                  +higher_hexagon/2+size_offset[1],
                                  +size[1]/2+size_offset[0]],   # 5
                                 [+side_hexagon/2+size_offset[0],
                                  +higher_hexagon/2+size_offset[1],
                                  +size[1]/2+size_offset[0]],   # 6
                                 [+side_hexagon/2+size_offset[0],
                                  +higher_hexagon/2+size_offset[1],
                                  -size[1]/2+size_offset[0]],   # 7
                                 [-size[0]/2+size_offset[0], size_offset[1], -size[1]/2+size_offset[0]],    # 8
                                 [-size[0]/2+size_offset[0], size_offset[1], +size[1]/2+size_offset[0]],    # 9
                                 [+size[0]/2+size_offset[0], size_offset[1], +size[1]/2+size_offset[0]],    # 10
                                 [+size[0]/2+size_offset[0], size_offset[1], -size[1]/2+size_offset[0]]])   # 11
        '''
                      y                              origin_axis
                      |                                  / \ 
               5 _____|_________6                   5_____|_____6                                              
               /|     |         /|                  /|    |    |\                                               
              /       |        / |                 /      |      \                               
             /  |__   |      _/  |               9/  |4__ |  __|7 \ 10 
           9/| 4/          10/  7/               |\  /         \  /|       
           / |8             /   /                | \             / |  
          /________________/   /__x              |8 \___________/  | __x           
         1|               2|11/                   \  1         |2 / 11               
          |                | /                     \ |         | /   
         0|_______________3|/                       \|____ ____|/   
                  /                                  0   /     3  
                 /                                      /     
                z                                      z                                                                               
        '''

        edges = np.array([[0, 1],
                          [0, 3],
                          [0, 8],
                          [1, 2],
                          [1, 9],
                          [2, 3],
                          [2, 10],
                          [3, 11],
                          [10, 11],
                          [10, 6],
                          [11, 7],
                          [6, 7],
                          [6, 5],
                          [7, 4],
                          [4, 5],
                          [4, 8],
                          [8, 9],
                          [5, 9]])

        surfaces = ((0, 1, 2, 3),
                    (3, 2, 10, 11),
                    (10, 11, 7, 6),
                    (6, 7, 4, 5),
                    (4, 5, 9, 9),
                    (0, 1, 9, 8),
                    (1, 2, 10, 6),
                    (1, 6, 5, 9),
                    (0, 3, 11, 7),
                    (0, 7, 4, 8))

        super().__init__(vertices=vertices,
                         edges=edges,
                         surfaces=surfaces,
                         color=color,
                         color_offset=color_offset,
                         origin=origin,
                         origin_offset=origin_offset,
                         axis=axis,
                         axis_offset=axis_offset,
                         theta=theta,
                         theta_offset=theta_offset,
                         theta_degree=theta_degree,
                         theta_degree_offset=theta_degree_offset,
                         phi=phi,
                         phi_offset=phi_offset,
                         phi_degree=phi_degree,
                         phi_degree_offset=phi_degree_offset,
                         size=size,
                         size_offset=size_offset)


class HexagonAxis(Solids):
    def __init__(self,
                 color=(1, 1, 1),
                 color_offset=(0, 0, 0),
                 origin=(0, 0, 0),
                 origin_offset=(0, 0, 0),
                 axis=(0, 1, 0),
                 axis_offset=(0, 0, 0),
                 theta=None,
                 theta_offset=None,
                 theta_degree=None,
                 theta_degree_offset=None,
                 phi=None,
                 phi_offset=None,
                 phi_degree=None,
                 phi_degree_offset=None,
                 size=(1, 1.5),
                 size_offset=(0, 0)):

        higher_hexagon = size[0]*np.sin(np.pi / 3)
        side_hexagon = size[0]*np.cos(np.pi/3)

        '''
                               origin 
            5___6_______________ | _________4____7
           /     \               |         /     \
          /       \             \|/               \
       9 /         \ 10__________o________________ \
         \         /                    8\       11/
          \       /                               /
           \____ /________________________ \____ /
            1   2                           0   3
        '''
        vertices = np.array([[-size[1]/2+size_offset[0],
                              +higher_hexagon/2+size_offset[1],
                              -side_hexagon/2+size_offset[0]],    # 0
                             [+size[1]/2+size_offset[0],
                              +higher_hexagon/2+size_offset[1],
                              -side_hexagon/2+size_offset[0]],   # 1
                             [+size[1]/2+size_offset[0],
                              +higher_hexagon/2+size_offset[1],
                              +side_hexagon/2+size_offset[0]],    # 2
                             [-size[1]/2+size_offset[0],
                              +higher_hexagon/2+size_offset[1],
                              +side_hexagon/2+size_offset[0]],    # 3
                             [-size[1]/2+size_offset[0],
                              -higher_hexagon/2+size_offset[1],
                              -side_hexagon/2+size_offset[0]],  # 4
                             [+size[1]/2+size_offset[0],
                              -higher_hexagon/2+size_offset[1],
                              -side_hexagon/2+size_offset[0]],   # 5
                             [+size[1]/2+size_offset[0],
                              -higher_hexagon/2+size_offset[1],
                              +side_hexagon/2+size_offset[0]],    # 6
                             [-size[1]/2+size_offset[0],
                              -higher_hexagon/2+size_offset[1],
                              +side_hexagon/2+size_offset[0]],   # 7
                             [-size[1]/2+size_offset[0], +size_offset[1], -size[0]/2+size_offset[0]],           # 8
                             [+size[1]/2+size_offset[0], +size_offset[1], -size[0]/2+size_offset[0]],           # 9
                             [+size[1]/2+size_offset[0], +size_offset[1], +size[0]/2+size_offset[0]],             # 10
                             [-size[1]/2+size_offset[0], +size_offset[1], +size[0]/2+size_offset[0]]])           # 11

        edges = np.array([[0, 1],
                          [0, 3],
                          [0, 8],
                          [1, 2],
                          [1, 9],
                          [2, 3],
                          [2, 10],
                          [3, 11],
                          [10, 11],
                          [10, 6],
                          [11, 7],
                          [6, 7],
                          [6, 5],
                          [7, 4],
                          [4, 5],
                          [4, 8],
                          [8, 9],
                          [5, 9]])

        surfaces = ((0, 1, 2, 3),
                    (3, 2, 10, 11),
                    (10, 11, 7, 6),
                    (6, 7, 4, 5),
                    (4, 5, 9, 9),
                    (0, 1, 9, 8),
                    (1, 2, 10, 6),
                    (1, 6, 5, 9),
                    (0, 3, 11, 7),
                    (0, 7, 4, 8))

        super().__init__(vertices=vertices,
                         edges=edges,
                         surfaces=surfaces,
                         color=color,
                         color_offset=color_offset,
                         origin=origin,
                         origin_offset=origin_offset,
                         axis=axis,
                         axis_offset=axis_offset,
                         theta=theta,
                         theta_offset=theta_offset,
                         theta_degree=theta_degree,
                         theta_degree_offset=theta_degree_offset,
                         phi=phi,
                         phi_offset=phi_offset,
                         phi_degree=phi_degree,
                         phi_degree_offset=phi_degree_offset,
                         size=size,
                         size_offset=size_offset)


class HexagonStalk(Solids):
    def __init__(self,
                 color=(1, 1, 1),
                 color_offset=(0, 0, 0),
                 origin=(0, 0, 0),
                 origin_offset=(0, 0, 0),
                 axis=(0, 1, 0),
                 axis_offset=(0, 0, 0),
                 theta=None,
                 theta_offset=None,
                 theta_degree=None,
                 theta_degree_offset=None,
                 phi=None,
                 phi_offset=None,
                 phi_degree=None,
                 phi_degree_offset=None,
                 size=(1, 1.5),
                 size_offset=(0, 0)):  # size = (size, x)

        higher_hexagon = size[0]*np.sin(np.pi / 3)
        side_hexagon = size[0]*np.cos(np.pi/3)

        '''
               |------------- size[1] -------------|
            7__|_4____________________________6____5
           /   |  \                          /      \
          /    |   \                                 \
       11/    \|/   \ 8______________________________ \
         \  origin  /                    10\         9/
          \        /                                 /
           \______/__________________________\______/
            3    0                            2     1
        '''
        vertices = np.array([[size_offset[0], +higher_hexagon/2+size_offset[1], -side_hexagon/2+size_offset[0]],    # 0
                             [+size[1]+size_offset[0], +higher_hexagon/2+size_offset[1], -side_hexagon/2+size_offset[0]],    # 1
                             [+size[1]+size_offset[0], +higher_hexagon/2+size_offset[1], +side_hexagon/2+size_offset[0]],    # 2
                             [size_offset[0], +higher_hexagon/2+size_offset[1], +side_hexagon/2+size_offset[0]],    # 3
                             [size_offset[0], -higher_hexagon/2+size_offset[1], -side_hexagon/2+size_offset[0]],  # 4
                             [size[1]+size_offset[0], -higher_hexagon/2+size_offset[1], -side_hexagon/2+size_offset[0]],   # 5
                             [size[1]+size_offset[0], -higher_hexagon/2+size_offset[1], +side_hexagon/2+size_offset[0]],    # 6
                             [size_offset[0], -higher_hexagon/2+size_offset[1], +side_hexagon/2+size_offset[0]],   # 7
                             [size_offset[0], +size_offset[1], -size[0]/2+size_offset[0]],           # 8
                             [size[1]+size_offset[0], +size_offset[1], -size[0]/2+size_offset[0]],           # 9
                             [size[1]+size_offset[0], +size_offset[1], +size[0]/2+size_offset[0]],             # 10
                             [size_offset[0], +size_offset[1], +size[0]/2+size_offset[0]]])           # 11

        edges = np.array([[0, 1],
                          [0, 3],
                          [0, 8],
                          [1, 2],
                          [1, 9],
                          [2, 3],
                          [2, 10],
                          [3, 11],
                          [10, 11],
                          [10, 6],
                          [11, 7],
                          [6, 7],
                          [6, 5],
                          [7, 4],
                          [4, 5],
                          [4, 8],
                          [8, 9],
                          [5, 9]])

        surfaces = ((0, 1, 2, 3),
                    (3, 2, 10, 11),
                    (10, 11, 7, 6),
                    (6, 7, 4, 5),
                    (4, 5, 9, 9),
                    (0, 1, 9, 8),
                    (1, 2, 10, 6),
                    (1, 6, 5, 9),
                    (0, 3, 11, 7),
                    (0, 7, 4, 8))

        super().__init__(vertices=vertices,
                         edges=edges,
                         surfaces=surfaces,
                         color=color,
                         color_offset=color_offset,
                         origin=origin,
                         origin_offset=origin_offset,
                         axis=axis,
                         axis_offset=axis_offset,
                         theta=theta,
                         theta_offset=theta_offset,
                         theta_degree=theta_degree,
                         theta_degree_offset=theta_degree_offset,
                         phi=phi,
                         phi_offset=phi_offset,
                         phi_degree=phi_degree,
                         phi_degree_offset=phi_degree_offset,
                         size=size,
                         size_offset=size_offset)


class SolidsGroup(Solids):
    def __init__(self,
                 solids_list,
                 origin=(0, 0, 0),
                 origin_offset=(0, 0, 0),
                 axis=(0, 1, 0),
                 axis_offset=(0, 0, 0),
                 theta=None,
                 theta_offset=None,
                 theta_degree=None,
                 theta_degree_offset=None,
                 phi=None,
                 phi_offset=None,
                 phi_degree=None,
                 phi_degree_offset=None,):

        self.solids_list = solids_list
        self._origin = np.asarray(origin, np.dtype('float64'))
        self._origin_offset = np.asarray(origin_offset, np.dtype('float64'))
        self._axis = np.asarray(axis, np.dtype('float64'))
        self._axis_offset = np.asarray(axis_offset, np.dtype('float64'))
        self._theta = theta
        self._theta = theta_offset
        self._theta_degree = theta_degree

        super().__init__(origin=origin,
                         origin_offset=origin_offset,
                         axis=axis,
                         axis_offset=axis_offset,
                         theta=theta,
                         theta_offset=theta_offset,
                         theta_degree=theta_degree,
                         theta_degree_offset=theta_degree_offset,
                         phi=phi,
                         phi_offset=phi_offset,
                         phi_degree=phi_degree,
                         phi_degree_offset=phi_degree_offset)

    def draw(self, mode=None):
        for solid in self.solids_list:
            solid.draw(mode)

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        self._origin = np.asarray(value, np.dtype('float64'))
        for solid in self.solids_list:
            solid.origin = self._origin

    @property
    def axis(self):
        return self._axis

    @axis.setter
    def axis(self, value):
        self._axis = np.asarray(value, np.dtype('float64'))
        for solid in self.solids_list:
            solid.axis = np.asarray(self._axis)

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
