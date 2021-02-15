import numpy as np
from glumpy import app, gl, glm, gloo

from pyramid import get_pyramid
from cube import create_cube
from surface import create_surface
from pyramid import create_pyramid
# from spade_gan import convert_image
# from vid_gan import convert_image
from math import cos, sin
from PIL import Image
# vars
running = False
time = 0
iters = 0
shapes = []
frame = None
segments = []
instances = []
window_width = 0
window_height = 0

vertex = """
    attribute vec2 position;
    attribute vec2 texcoord;
    varying vec2 v_texcoord;
    void main()
    {
        gl_Position = vec4(position, 0.0, 1.0);
        v_texcoord = texcoord;
    }
"""

fragment = """
    uniform sampler2D texture;
    varying vec2 v_texcoord;
    void main()
    {
        gl_FragColor = texture2D(texture, v_texcoord);
    }
"""
image_program = None

def get_color(r,g,b):
    return (r/255, g/255, b/255, 1)

def start_world(width=1024, height=512, overlay=False, frames=60):
    global running, frame, window_height, window_width, image_program, segments, instances
    window_width = width
    window_height = height
    window = app.Window(width=width, height=height, color=get_color(23,23,23))
    frame = np.zeros((window.height, window.width * 3), dtype=np.uint8)

    def render_segments():
        window.clear(get_color(23,23,23))
        for shape in shapes:
            shape.use_segment_color()
            shape.draw()

    def render_instances():
        window.clear((1,1,1, 1))
        for shape in shapes:
            shape.use_instance_color()
            shape.draw()

    def capture_frame():
        gl.glDisable(gl.GL_DEPTH_TEST)
        gl.glReadPixels(0, 0, window_width, window_height, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, frame)
        out = np.flipud(np.array(frame)).reshape(height, width, 3)
        gl.glEnable(gl.GL_DEPTH_TEST)
        return out

    def move_shapes():
        for shape in shapes:
            # shape.set_rotation((time, 0, 1, 0))
            # shape.set_translation((0, -time*5+2, cos(time)/2-1))
            if shape.shape_type == "cube":
                x, y, z= shape.position
                shape.set_translation((x, y - time*25, z))

    @window.event
    def on_resize(width, height):
        for shape in shapes:
            shape.projection(glm.perspective(45.0, width / float(height), 2.0, 100.0))

    @window.event
    def on_init():
        gl.glEnable(gl.GL_DEPTH_TEST)

    @window.event
    def on_draw(dt):
        global iters, time, shapes, frame, window_height, window_width, image_program
        move_shapes()
        time += dt
        # Capture segmentation map
        render_segments()
        segment_map = capture_frame()
        # Capture instance map
        render_instances()
        instance_map = capture_frame()

        
 
        Image.fromarray(segment_map).save('../datasets/test/test_A/image_' + str(iters).zfill(4) + '.png')
        # img = Image.open('./world/examples/segments/image_'+str(iters)+'.png')
        # segment_map = np.array(img)
        Image.fromarray(instance_map).save('../datasets/test/test_inst/image_' + str(iters).zfill(4) + '.png')
        # img = Image.open('./world/examples/instances/image_'+str(iters)+'.png')
        # instance_map = np.array(img)
        # Generate frame
        # segments.append(segment_map)
        # instances.append(instance_map)
        # if len(segments) == 3:
            # gen_frame = convert_image(segments, instances)
            # image_program['texture'] = gen_frame
            # image_program.draw(gl.GL_TRIANGLE_STRIP)
            # segments.pop()
            # instances.pop()
            # Image.fromarray(gen_frame).save('./world/examples/results/image_' + str(iters) + '.png')
        iters += 1
        if (iters >= frames):
            app.quit()


    shapes.append(cube)
    image_program = gloo.Program(vertex, fragment, count=4)
    image_program['position'] = [(-1,-1), (-1,+1), (+1,-1), (+1,+1)]
    image_program['texcoord'] = [( 0, 1), ( 0, 0), ( 1, 1), ( 1, 0)]
    image_program['texture'] = np.random.randint(1, 255, size=(512, 1024, 3), dtype=np.uint8)
    app.run(framerate=60)
    running = True

def add_shape(shape):
    shapes.append(shape)
    if running == True:
        app.quit()
        app.run(framerate=60)

for i in range(10):
    building_color = get_color(11,11,11)
    cube = create_cube((-5, -15 + i * 6, 0), (5, 8, 20), building_color)
    add_shape(cube)
    cube = create_cube((5, -15 + i * 6, 0), (5, 8, 20), building_color)
    add_shape(cube)

    cube = create_cube((-20 + i * 5, 50, 0), (8, 5, 20 + np.random.randint(-3, 3)), building_color)
    add_shape(cube)

    # car_color = get_color(26,26,26)
    # cube = create_cube((1.5, -15 + i * 6, -0.5), (1, 3, 2), car_color)
    # add_shape(cube)

road_color = get_color(7,7,7)
surface = create_surface((0,0,0), (300, 600, -1), road_color, 10)
add_shape(surface)

sidewalk_color = get_color(8,8,8)
sidwalk_left = create_cube((-3, 0, -0.7), (1.5, 165, 1), sidewalk_color)
add_shape(sidwalk_left)

sidewalk_right = create_cube((3, 0, -0.7), (1.5, 165, 1), sidewalk_color)
add_shape(sidewalk_right)

sidewalk_far = create_cube((0, 47, -0.6), (100, 1.5, 1), sidewalk_color)
add_shape(sidewalk_far)
# for i in range(10):
#     width = 44 + np.random.randint(-6, 26)
#     height = 44 + np.random.randint(-20, 20)
#     pyramid = create_pyramid((-100 + i * 15, 75, 0), (width, width, height), (134/255,0,135/255,1))
#     add_shape(pyramid)
#     width = 44 + np.random.randint(-6, 26)
#     height = 44 + np.random.randint(-20, 20)
#     pyramid = create_pyramid((-80 + i * 10, 75, 0), (width, width, height), (134/255,0,135/255,1))
#     add_shape(pyramid)

start_world(frames=120)
