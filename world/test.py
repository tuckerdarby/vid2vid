import numpy as np
diff = 0.5
size = (10, 8, 1)

width, length, height = size

w, l = width/2, length/2
x_start = -w
y_start = -l

nx = int(width/diff + 1)
ny = int(length/diff + 1)
n_coords = nx * ny

xs = np.linspace(x_start, x_start + width, nx)
ys = np.linspace(y_start, y_start + length, ny)

m = np.array(np.meshgrid(xs, ys)).transpose(1, 2,0)
coordinates = np.insert(m, 2, height, axis=2).reshape(n_coords, 3)

indexes = []

for y in range(ny-1):
    for x in range(nx-1):
        i = y*nx + x
        i2 = i + 1
        i3 = (y+1)*nx + x
        indexes.append((i, i2, i3))
        i = i3 + 1
        indexes.append((i, i2, i3))

print(indexes)