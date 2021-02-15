import numpy as np
from glumpy import app, gl, glm, gloo
from helpers import get_fragment, get_vertex
from shape import Shape

surface_vertex = get_vertex('simple')
surface_fragment = get_fragment('simple')

def get_surface(size, color, diff):
    width, length, height = size
    
    w, l = width/2, length/2
    x_start = -w
    y_start = -l

    nx = int(width/diff + 1)
    ny = int(length/diff + 1)
    n_coords = nx * ny

    xs = np.linspace(x_start, x_start + width, nx)
    ys = np.linspace(y_start, y_start + length, ny)

    m = np.array(np.meshgrid(xs, ys)).transpose(1,2,0)
    coordinates = np.insert(m, 2, height, axis=2).reshape(n_coords, 3)
    
    V = np.zeros(n_coords, [("coordinates", np.float32, 3), ("color", np.float32, 4)])
    V["coordinates"] = coordinates
    V["color"] = [color for _ in range(n_coords)]

    V = V.view(gloo.VertexBuffer)

    indexes = []
    for y in range(ny-1):
        for x in range(nx-1):
            i = y*nx + x
            i2 = i + 1
            i3 = (y+1)*nx + x
            indexes.append((i, i2, i3))
            i = i3 + 1
            indexes.append((i, i2, i3))

    I = np.array(indexes, dtype=np.uint32)
    I = I.view(gloo.IndexBuffer)

    surface = gloo.Program(surface_vertex, surface_fragment)
    surface.bind(V)

    return surface, coordinates, I, n_coords

def create_surface(position, size, color, diff=0.1):
    surface, coordinates, I, n_coords = get_surface(size, color, diff)
    surface = Shape("surface", surface, coordinates, I, position, size, color, n_coords)
    return surface
