import numpy as np
from glumpy import app, gl, glm, gloo
from helpers import get_fragment, get_vertex
from shape import Shape

cube_vertex = get_vertex('simple')
cube_fragment = get_fragment('simple')

def get_cube(size, color=[0.5, 0.5, 0.5, 1]):
    width, length, height = size
    V = np.zeros(8, [("coordinates", np.float32, 3), ("color", np.float32, 4)])
    w, l, h = width/2, length/2, height/2
    coordinates = [[ w, l, h ], [-w, l, h], [-w,-l, h], [ w,-l, h],
                    [ w,-l,-h], [ w, l,-h], [-w, l,-h], [-w,-l,-h]]
    V["coordinates"] = coordinates
    V["color"] = [color for _ in range(8)]

    V = V.view(gloo.VertexBuffer)
    I = np.array([0,1,2, 0,2,3,  0,3,4, 0,4,5,  0,5,6, 0,6,1,
                1,6,7, 1,7,2,  7,4,3, 7,3,2,  4,7,6, 4,6,5], dtype=np.uint32)
    I = I.view(gloo.IndexBuffer)

    cube = gloo.Program(cube_vertex, cube_fragment)
    cube.bind(V)

    return cube, coordinates, I, 8

def create_cube(position, size, color):
    cube, coordinates, I, n_coords = get_cube(size, color)
    cube = Shape("cube", cube, coordinates, I, position, size, color, n_coords)
    return cube
