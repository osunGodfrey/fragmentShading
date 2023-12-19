#version 410 core

in vec3 fragColor;
in vec2 texture_coords;

uniform sampler2D textureSample; 

out vec4 outColor;

void main()
{
    // outColor = vec4(1.0, 1.0, 1.0, 1.0);
    // outColor = vec4(fragColor, 0.0);
    vec4 textureColor = texture(textureSample, -1*texture_coords);
    outColor = textureColor * vec4(fragColor, 1.0);
}
