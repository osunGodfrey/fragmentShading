#version 410 core

layout(location = 0) in vec3 inPosition;
layout(location = 1) in vec3 inColor;
layout(location = 2) in vec2 tex_coords;

out vec3 fragColor;
out vec2 texture_coords;

void main()
{
    gl_Position = vec4(inPosition, 1.0);
    fragColor = inColor;
    texture_coords = tex_coords;
}