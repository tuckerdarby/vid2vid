uniform mat4   model;
uniform mat4   view;
uniform mat4   projection;
attribute vec3 coordinates;
attribute vec4 color;
varying vec4 v_color;
void main()
{
    gl_Position = projection * view * model * vec4(coordinates,1.0);
    v_color = color;
}