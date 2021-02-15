import numpy as np
from glumpy import app, gl, glm, gloo

standard_rotation = (-90, 1, 0, 0)
n_instance = 0

def get_next_instance():
    global n_instance
    n_instance += 1
    return n_instance

class Shape:
    def __init__(self, shape_type, program, coordinates, indexes, position, size, color, n_coords):
        # init
        self.shape_type = shape_type
        self.program = program
        self.coordinates = coordinates
        self.indexes = indexes
        self.position = position
        self.color = color
        self.size = size
        self.n_coords = n_coords

        self.rotation = None
        self.instance = get_next_instance()

        self.random_color = [(np.random.rand()*255, np.random.rand()*255, np.random.rand()*255, 1) for _ in range(n_coords)]

        # model
        self.model = np.eye(4, dtype=np.float32)
        program['model'] = self.model

        # view
        x, y, z = self.position
        view = glm.translation(x, y, z)
        # deg, rx, ry, rz = self.rotation
        # view = glm.rotate(view, deg, rx, ry, rz)
        program['view'] = view
        self.translation = (0, 0, 0)

    def use_instance_color(self):
        inst = self.instance / 255
        color = (inst,inst, inst, 1)
        self.program['color'] = [color for _ in range(self.n_coords)]

    def use_segment_color(self):
        self.program['color'] = [self.color for _ in range(self.n_coords)]

    def use_random_color(self):
        self.program['color'] = self.random_color

    def set_translation(self, translation):
        self.translation = translation

    def set_rotation(self, rotation):
        self.rotation = rotation

    def update_view(self):
        x, y, z = self.position
        dx, dy, dz = self.translation
        nx, ny, nz = x + dx, y + dy, z + dz
        view = glm.translate(np.eye(4, dtype=np.float32), nx, ny , nz)
        view = glm.rotate(view, -90, 1, 0, 0)
        if self.rotation is not None:
            deg, rx, ry, rz = self.rotation
            view = glm.rotate(view, deg, rx, ry, rz)
        self.view = view

    def draw(self):
        self.update_view()
        self.program['coordinates'] = self.coordinates
        self.program['model'] = self.model
        self.program['view'] = self.view
        self.program.draw(gl.GL_TRIANGLES, self.indexes)

    def projection(self, projection):
        self.program['projection'] = projection
