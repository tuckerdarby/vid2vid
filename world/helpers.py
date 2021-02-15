
def get_fragment(name):
    fragment = ''
    file_name = 'fragments/{name}.glsl'.format(name=name)
    with open(file_name, 'r') as file:
        fragment = file.read().replace('\n', '')
    return fragment

def get_vertex(name):
    vertex = ''
    file_name = 'vertices/{name}.glsl'.format(name=name)
    with open(file_name, 'r') as file:
        vertex = file.read().replace('\n', '')
    return vertex
