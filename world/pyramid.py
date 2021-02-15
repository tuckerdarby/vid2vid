import numpy as np
from glumpy import app, gl, glm, gloo
from helpers import get_fragment, get_vertex
from shape import Shape

pyramid_vertex = get_vertex('simple')
pyramid_fragment = get_fragment('simple')

def get_pyramid(size, color=[0.5, 0.5, 0.5, 1]):
    width, length, height = size
    w, l, h = width/2, length/2, height/2
    V = np.zeros(5, [("coordinates", np.float32, 3), ("color", np.float32, 4)])
    coordinates = [[ w, l, -h], [-w, l, -h], [-w,-l, -h], [ w,-l, -h], [0, 0, h]]
    V["coordinates"] = coordinates
    V["color"] = [color for _ in range(5)]

    V = V.view(gloo.VertexBuffer)
    I = np.array([0,1,2, 0,2,3,  
                0,1,4, 0,3,4,  2,3,4, 2, 1,4], dtype=np.uint32)
    I = I.view(gloo.IndexBuffer)

    pyramid = gloo.Program(pyramid_vertex, pyramid_fragment)
    pyramid.bind(V)

    return pyramid, coordinates, I, 5

def create_pyramid(position, size, color):
    pyramid, coordinates, I, n_coords = get_pyramid(size, color)
    pyramid = Shape("pyramid", pyramid, coordinates, I, position, size, color, n_coords)
    return pyramid
