import numpy as np
from OpenGL.GL import *


class Solids:
    def __init__(self,
                 vertices=None,
                 edges=None,
                 surfaces=None,
                 color=None,
                 origin=(0, 0, -5),
                 offset=(0, 0, 0),
                 axis=(0, 1, 0),
                 theta=None,
                 theta_degree=None,
                 size=None):

        self.vertices = vertices
        self.edges = edges
        self.surface = surfaces
        self.color = np.asarray(color)
        self.size = size
        self._origin = np.asarray(origin, np.dtype('float64'))
        self._offset = np.asarray(offset, np.dtype('float64'))
        self._axis = np.asarray(axis, np.dtype('float64'))

        if theta is not None and theta_degree is None:
            self.theta = theta
        elif theta is None and theta_degree is not None:
            self.theta_degree = theta_degree
        else:
            self._theta = 0
            self._theta_degree = 0

    def draw(self):
        glPushMatrix()

        self._translate()
        self._rotate()

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
                    glColor3fv(self.color)
                glVertex3fv(self.vertices[vertex])
        glEnd()

    def _translate(self):
        glTranslatef(self._origin[0], self._origin[1], self._origin[2])

    def _rotate(self):
        glRotatef(self._theta_degree, self._axis[0], self._axis[1], self._axis[2])

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = np.asarray(value)

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        self._origin = np.asarray(np.asarray(value, np.dtype('float64')))

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = np.asarray(value, np.dtype('float64'))
        for i, vertex in enumerate(self.vertices):
            self.vertices[i][:] = [vertex[0]+self._offset[0],
                                   vertex[1]+self._offset[1],
                                   vertex[2]+self._offset[2]]

    @property
    def axis(self):
        return self._axis

    @axis.setter
    def axis(self, value):
        self._axis = np.asarray(value, np.dtype('float64'))

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


class Pyramid(Solids):
    def __init__(self,
                 color=(1, 1, 1),
                 origin=(0, 0, -5),  # (x, y, z)
                 offset=(0, 0, 0),  # (x, y, z)
                 axis=(0, 1, 0),  # (x, y, z)
                 theta=None,
                 theta_degree=None,
                 size=(0.5, 0.3, 0.5)):  # size = (x, y, z)

        vertices = np.array([[-size[0]/2+offset[0], -size[1]/2+offset[1], +size[2]/2+offset[2]],  # 0
                             [-size[0]/2+offset[0], -size[1]/2+offset[1], -size[2]/2+offset[2]],  # 1
                             [+size[0]/2+offset[0], -size[1]/2+offset[1], -size[2]/2+offset[2]],  # 2
                             [+size[0]/2+offset[0], -size[1]/2+offset[1], +size[2]/2+offset[2]],  # 3
                             [offset[0], size[1]/2+offset[1], offset[2]],  # 4
                             [offset[0], size[1]/2+offset[1], offset[2]]])  # 5

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
                         origin=origin,
                         axis=axis,
                         theta=theta,
                         theta_degree=theta_degree,
                         size=size)


class Cube(Solids):
    def __init__(self,
                 color=(1, 1, 1),
                 origin=(0, 0, -5),  # (x, y, z)
                 offset=(0, 0, 0),  # (x, y, z)
                 axis=(0, 1, 0),  # (x, y, z)
                 theta=None,
                 theta_degree=None,
                 size=0.6):

        vertices = np.array([[-size/2+offset[0], -size/2+offset[1], +size/2+offset[2]],
                             [-size/2+offset[0], +size/2+offset[1], +size/2+offset[2]],
                             [+size/2+offset[0], +size/2+offset[1], +size/2+offset[2]],
                             [+size/2+offset[0], -size/2+offset[1], +size/2+offset[2]],
                             [-size/2+offset[0], -size/2+offset[1], -size/2+offset[2]],
                             [-size/2+offset[0], +size/2+offset[1], -size/2+offset[2]],
                             [+size/2+offset[0], +size/2+offset[1], -size/2+offset[2]],
                             [+size/2+offset[0], -size/2+offset[1], -size/2+offset[2]]])
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
                         origin=origin,
                         offset=offset,
                         axis=axis,
                         theta=theta,
                         theta_degree=theta_degree,
                         size=size)


class Parallelepiped(Solids):
    def __init__(self,
                 color=(1, 1, 1),
                 origin=(0, 0, -5),  # origin = (x, y, z)
                 offset=(0, 0, 0),  # (x, y, z)
                 axis=(0, 1, 0),  # axis = (x, y, z)
                 theta=None,
                 theta_degree=None,
                 alpha=np.pi/2,
                 size=(0.5, 0.7, 0.2)):  # size = (x, y, z)

        vertices = np.array([[-size[0]/2+offset[0], -size[1]/2+offset[1], +size[2]/2+offset[2]],   # 0
                             [-size[0]/2+offset[0], +size[1]/2+offset[1], +size[2]/2+offset[2]],   # 1
                             [+size[0]/2+offset[0], +size[1]/2+offset[1], +size[2]/2+offset[2]],   # 2
                             [+size[0]/2+offset[0], -size[1]/2+offset[1], +size[2]/2+offset[2]],   # 3
                             [-size[0]/2+offset[0], -size[1]/2+offset[1], -size[2]/2+offset[2]],   # 4
                             [-size[0]/2+offset[0], +size[1]/2+offset[1], -size[2]/2+offset[2]],   # 5
                             [+size[0]/2+offset[0], +size[1]/2+offset[1], -size[2]/2+offset[2]],   # 6
                             [+size[0]/2+offset[0], -size[1]/2+offset[1], -size[2]/2+offset[2]]])  # 7

        offset = size[1]/np.tan(alpha)

        vertices[1, 0] += offset
        vertices[2, 0] += offset
        vertices[5, 0] += offset
        vertices[6, 0] += offset
        '''
               5____________6                            5___________6            
               /           /|                           /           /
              /           / |                          /           / 
        y__ 1/__________2/  |          offset--> y__ 1/__________2/   
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
                         origin=origin,
                         offset=offset,
                         axis=axis,
                         theta=theta,
                         theta_degree=theta_degree,
                         size=size)


class Trapezoid(Solids):
    def __init__(self,
                 color=(1, 1, 1),
                 origin=(0, 0, -5),  # origin = (x, y, z)
                 offset=(0, 0, 0),  # (x, y, z)
                 axis=(0, 1, 0),  # axis = (x, y, z)
                 theta=None,
                 theta_degree=None,
                 size=(0.5, 0.5, 0.2, 0.3, 0.2, 0.3)):  # size = (x1_b, x2_b, x1_t, x2_t, y, z)

        vertices = np.array([[-size[0]/2+offset[0], -size[4]/2+offset[1], +size[5]/2+offset[2]],   # 0
                             [-size[2]/2+offset[0], +size[4]/2+offset[1], +size[5]/2+offset[2]],    # 1
                             [+size[3]/2+offset[0], +size[4]/2+offset[1], +size[5]/2+offset[2]],     # 2
                             [+size[1]/2+offset[0], -size[4]/2+offset[1], +size[5]/2+offset[2]],    # 3
                             [-size[0]/2+offset[0], -size[4]/2+offset[1], -size[5]/2+offset[2]],  # 4
                             [-size[2]/2+offset[0], +size[4]/2+offset[1], -size[5]/2+offset[2]],   # 5
                             [+size[3]/2+offset[0], +size[4]/2+offset[1], -size[5]/2+offset[2]],    # 6
                             [+size[1]/2+offset[0], -size[4]/2+offset[1], -size[5]/2+offset[2]]])  # 7

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
                         origin=origin,
                         offset=offset,
                         theta=theta,
                         theta_degree=theta_degree,
                         axis=axis,
                         size=size)


class PyramidTrunk(Solids):
    def __init__(self,
                 color=(1, 1, 1),
                 origin=(0, 0, -5),  # origin = (x, y, z)
                 offset=(0, 0, 0),  # (x, y, z)
                 axis=(0, 1, 0),  # axis = (x, y, z)
                 theta=None,
                 theta_degree=None,
                 size=(0.5, 0.3, 0.5, 0.3, 0.2)):  # size = (x, y, z, x, y)

        vertices = np.array([[-size[0]/2+offset[0], -size[1]/2+offset[1], +size[2]/2+offset[2]],   # 0
                             [-size[3]/2+offset[0], +size[1]/2+offset[1], +size[4]/2+offset[2]],    # 1
                             [+size[3]/2+offset[0], +size[1]/2+offset[1], +size[4]/2+offset[2]],     # 2
                             [+size[0]/2+offset[0], -size[1]/2+offset[1], +size[2]/2+offset[2]],    # 3
                             [-size[0]/2+offset[0], -size[1]/2+offset[1], -size[2]/2+offset[2]],  # 4
                             [-size[3]/2+offset[0], +size[1]/2+offset[1], -size[4]/2+offset[2]],   # 5
                             [+size[3]/2+offset[0], +size[1]/2+offset[1], -size[4]/2+offset[2]],    # 6
                             [+size[0]/2+offset[0], -size[1]/2+offset[1], -size[2]/2+offset[2]]])  # 7
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
                         origin=origin,
                         offset=offset,
                         axis=axis,
                         theta=theta,
                         theta_degree=theta_degree,
                         size=size)


class Hexagon(Solids):
    def __init__(self,
                 color=(1, 1, 1),
                 origin=(0, 0, -5),  # origin = (x, y, z)
                 offset=(0, 0, 0),  # (x, y, z)
                 axis=(0, 1, 0),  # axis = (x, y, z)
                 theta=None,
                 theta_degree=None,
                 size=(0.5, 0.2)):  # size = (size, y)

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
        vertices = np.array([[-side_hexagon/2+offset[0], -size[1]/2+offset[1], higher_hexagon/2+offset[2]],   # 0
                             [-side_hexagon/2+offset[0], size[1]/2+offset[1], higher_hexagon/2+offset[2]],    # 1
                             [side_hexagon/2+offset[0], size[1]/2+offset[1], higher_hexagon/2+offset[2]],     # 2
                             [side_hexagon/2+offset[0], -size[1]/2+offset[1], higher_hexagon/2+offset[2]],    # 3
                             [-side_hexagon/2+offset[0], -size[1]/2+offset[1], -higher_hexagon/2+offset[2]],  # 4
                             [-side_hexagon/2+offset[0], size[1]/2+offset[1], -higher_hexagon/2+offset[2]],   # 5
                             [side_hexagon/2+offset[0], size[1]/2+offset[1], -higher_hexagon/2+offset[2]],    # 6
                             [side_hexagon/2+offset[0], -size[1]/2+offset[1], -higher_hexagon/2+offset[2]],   # 7
                             [-size[0]/2+offset[0], -size[1]/2+offset[1], offset[2]],           # 8
                             [-size[0]/2+offset[0], size[1]/2+offset[1], offset[2]],            # 9
                             [size[0]/2+offset[0], size[1]/2+offset[1], offset[2]],             # 10
                             [size[0]/2+offset[0], -size[1]/2+offset[1], offset[2]]])           # 11

        '''
               5 _______________6                   5__________6                                              
               /|               /|                  /|        |\                                               
              /                / |                 /            \ ______-z                              
          y__/  |__          _/  |__-z       y__ 9/  |4__   __|7 \ 10 
           9/| 4/          10/  7/               |\  /        \  /|       
           / |8             /   /                | \            / |  
          /________________/   /__0              |8 \__________/  | __0           
         1|               2|11/                   \  1        |2 / 11               
          |                | /                 /   \ |        | /   
         0|_______________3|/                 /     \|________|/   
         /                                   /       0        3  
        /                                   /     
      -x                                  -x                                                                               
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
                         origin=origin,
                         offset=offset,
                         axis=axis,
                         theta=theta,
                         theta_degree=theta_degree,
                         size=size)


class HexagonAxis(Solids):
    def __init__(self,
                 color=(1, 1, 1),
                 origin=(0, 0, -5),  # origin = (x, y, z)
                 offset=(0, 0, 0),  # (x, y, z)
                 axis=(0, 1, 0),  # axis = (x, y, z)
                 theta=None,
                 theta_degree=None,
                 size=(1, 1.5)):  # size = (size, x)

        higher_hexagon = size[0]*np.sin(np.pi / 3)
        side_hexagon = size[0]*np.cos(np.pi/3)

        '''
                               origin 
            5____6_______________ | _________4____7
           /      \               |         /      \
          /        \             \|/                \
       9 /          \ 10__________o_________________ \
         \          /                    8\        11/
          \        /                                /
           \_____ /________________________ \_____ /
            1    2                          0     3
        '''
        vertices = np.array([[-size[1]/2+offset[0], +higher_hexagon/2+offset[1], -side_hexagon/2+offset[2]],    # 0
                             [+size[1]/2+offset[0], +higher_hexagon/2+offset[1], -side_hexagon/2+offset[2]],   # 1
                             [+size[1]/2+offset[0], +higher_hexagon/2+offset[1], +side_hexagon/2+offset[2]],    # 2
                             [-size[1]/2+offset[0], +higher_hexagon/2+offset[1], +side_hexagon/2+offset[2]],    # 3
                             [-size[1]/2+offset[0], -higher_hexagon/2+offset[1], -side_hexagon/2+offset[2]],  # 4
                             [+size[1]/2+offset[0], -higher_hexagon/2+offset[1], -side_hexagon/2+offset[2]],   # 5
                             [+size[1]/2+offset[0], -higher_hexagon/2+offset[1], +side_hexagon/2+offset[2]],    # 6
                             [-size[1]/2+offset[0], -higher_hexagon/2+offset[1], +side_hexagon/2+offset[2]],   # 7
                             [-size[1]/2+offset[0], +offset[1], -size[0]/2+offset[2]],           # 8
                             [+size[1]/2+offset[0], +offset[1], -size[0]/2+offset[2]],           # 9
                             [+size[1]/2+offset[0], +offset[1], +size[0]/2+offset[2]],             # 10
                             [-size[1]/2+offset[0], +offset[1], +size[0]/2+offset[2]]])           # 11

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
                         origin=origin,
                         offset=offset,
                         theta=theta,
                         theta_degree=theta_degree,
                         axis=axis,
                         size=size)


class HexagonStalk(Solids):
    def __init__(self,
                 color=(1, 1, 1),
                 origin=(0, 0, -5),  # origin = (x, y, z)
                 offset=(0, 0, 0),  # (x, y, z)
                 axis=(0, 1, 0),  # axis = (x, y, z)
                 theta=None,
                 theta_degree=None,
                 size=(1, 1.5)):  # size = (size, x)

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
        vertices = np.array([[offset[0], +higher_hexagon/2+offset[1], -side_hexagon/2+offset[2]],    # 0
                             [+size[1]+offset[0], +higher_hexagon/2+offset[1], -side_hexagon/2+offset[2]],    # 1
                             [+size[1]+offset[0], +higher_hexagon/2+offset[1], +side_hexagon/2+offset[2]],    # 2
                             [offset[0], +higher_hexagon/2+offset[1], +side_hexagon/2+offset[2]],    # 3
                             [offset[0], -higher_hexagon/2+offset[1], -side_hexagon/2+offset[2]],  # 4
                             [size[1]+offset[0], -higher_hexagon/2+offset[1], -side_hexagon/2+offset[2]],   # 5
                             [size[1]+offset[0], -higher_hexagon/2+offset[1], +side_hexagon/2+offset[2]],    # 6
                             [offset[0], -higher_hexagon/2+offset[1], +side_hexagon/2+offset[2]],   # 7
                             [offset[0], +offset[1], -size[0]/2+offset[2]],           # 8
                             [size[1]+offset[0], +offset[1], -size[0]/2+offset[2]],           # 9
                             [size[1]+offset[0], +offset[1], +size[0]/2+offset[2]],             # 10
                             [offset[0], +offset[1], +size[0]/2+offset[2]]])           # 11

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
                         origin=origin,
                         offset=offset,
                         theta=theta,
                         theta_degree=theta_degree,
                         axis=axis,
                         size=size)


class Stalk(Solids):
    def __init__(self,
                 color=(1, 1, 1),
                 origin=(0, 0, -5),  # origin = (x, y, z)
                 offset=(0, 0, 0),  # (x, y, z)
                 axis=(0, 1, 0),  # axis = (x, y, z)
                 theta=None,
                 theta_degree=None,
                 thickness=0.2,
                 xyz=(1, 1, 1)):

        """
               5__________________________________________6
               /                                         /|
              /                                         / |
        y__ 1/________________________________________2/  |
            |   |__                                   |    __-z
            |   4                                     |   7
        0-- |  /                                      |  /__0
            | /                                       | /
        -y__0__________________________________________3__z
            /                                         /
          -x                                         x






               5__________________________________________6
               /                                         /|
              /                                         / |
        y__ 1/________________________________________2/  |
            |   |__                                   |    __-z
            |   4                                     |   7
        0-- |  /                                      |  /__0
            | /                                       | /
        -y__0__________________________________________3__z
            /                                         /
          -x                                         x
        """
        vertices = np.array([[offset[0], -thickness/2+xyz[1]+offset[1], +thickness/2+xyz[2]+offset[2]],
                             [offset[0], +thickness/2+xyz[1]+offset[1], +thickness/2+xyz[2]+offset[2]],
                             [xyz[0]+offset[0], +thickness/2+xyz[1]+offset[1], +thickness/2+xyz[2]+offset[2]],
                             [xyz[0]+offset[0], -thickness/2+xyz[1]+offset[1], +thickness/2+xyz[2]+offset[2]],
                             [offset[0], -thickness/2+xyz[1]+offset[1], -thickness/2+xyz[2]+offset[2]],
                             [offset[0], +thickness/2+xyz[1]+offset[1], -thickness/2+xyz[2]+offset[2]],
                             [xyz[0]+offset[0], +thickness/2+xyz[1]+offset[1], -thickness/2+xyz[2]+offset[2]],
                             [xyz[0]+offset[0], -thickness/2+xyz[1]+offset[1], -thickness/2+xyz[2]+offset[2]]])

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
                         origin=origin,
                         offset=offset,
                         theta=theta,
                         theta_degree=theta_degree,
                         axis=axis,
                         size=thickness)

        self._xyz = xyz
        self.thickness = thickness

    @property
    def xyz(self):
        return self._xyz

    @xyz.setter
    def xyz(self, value):
        self._xyz = np.asarray(value)
        self.vertices = np.array([[self.offset[0],
                                   -self.thickness/2+self.xyz[1]+self.offset[1],
                                   +self.thickness/2+self.xyz[2]+self.offset[2]],
                                  [self.offset[0],
                                   +self.thickness/2+self.xyz[1]+self.offset[1],
                                   +self.thickness/2+self.xyz[2]+self.offset[2]],
                                  [self.xyz[0]+self.offset[0],
                                   +self.thickness/2+self.xyz[1]+self.offset[1],
                                   +self.thickness/2+self.xyz[2]+self.offset[2]],
                                  [self.xyz[0]+self.offset[0],
                                   -self.thickness/2+self.xyz[1]+self.offset[1],
                                   +self.thickness/2+self.xyz[2]+self.offset[2]],
                                  [self.offset[0],
                                   -self.thickness/2+self.xyz[1]+self.offset[1],
                                   -self.thickness/2+self.xyz[2]+self.offset[2]],
                                  [self.offset[0],
                                   +self.thickness/2+self.xyz[1]+self.offset[1],
                                   -self.thickness/2+self.xyz[2]+self.offset[2]],
                                  [self.xyz[0]+self.offset[0],
                                   +self.thickness/2+self.xyz[1]+self.offset[1],
                                   -self.thickness/2+self.xyz[2]+self.offset[2]],
                                  [self.xyz[0]+self.offset[0],
                                   -self.thickness/2+self.xyz[1]+self.offset[1],
                                   -self.thickness/2+self.xyz[2]+self.offset[2]]])


class SolidsGroup(Solids):
    def __init__(self,
                 solids_list,
                 origin=(0, 0, -5),
                 offset=(0, 0, 0),
                 axis=(0, 1, 0),
                 theta=None,
                 theta_degree=None):

        self.solids_list = solids_list
        self._origin = np.asarray(origin, np.dtype('float64'))
        self._offset = np.asarray(offset, np.dtype('float64'))
        self._axis = np.asarray(axis, np.dtype('float64'))
        self._theta_degree = theta_degree
        self._theta = theta

        super().__init__(origin=origin,
                         offset=offset,
                         axis=axis,
                         theta=theta,
                         theta_degree=theta_degree)

    def draw(self):
        for solid in self.solids_list:
            solid.draw()

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        self._origin = np.asarray(value, np.dtype('float64'))
        for solid in self.solids_list:
            solid.origin = self._origin

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = np.asarray(value, np.dtype('float64'))
        for solid in self.solids_list:
            solid.offset = np.asarray(self._offset)

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
