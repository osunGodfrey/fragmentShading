#version 410 core

in vec3 fragColor;
in vec2 texture_coords;

out vec4 outColor;

const float pi = 3.1415;

uniform float time_laps; // time laps

// color palette funtions
vec3 palette( float t ) {
    vec3 a = vec3(0.5, 0.5, 0.5);
    vec3 b = vec3(0.5, 0.5, 0.5);
    vec3 c = vec3(1.0, 1.0, 1.0);
    vec3 d = vec3(0.263,0.416,0.557);

    return a + b*cos( 6.28318*(c*t+d) );
}

void main()
{
    // polar coords
    vec2 coords = vec2(texture_coords.x - 0.5, texture_coords.y - 0.5);
    vec2 coords_0 = coords;
    vec3 finalColor = vec3(0.0);

    for(float i = 0; i < 4; i++){

        coords = vec2(fract(coords.x * 3) - 0.5, fract(coords.y * 3) - 0.5);
        float dist = sqrt( pow(coords.x, 2) + pow(coords.y, 2));

        // colors
        float dist_0 = sqrt( pow(coords_0.x, 2) + pow(coords_0.y, 2));
        vec3 cols = palette(dist_0 + i*0.4 + time_laps/16);

        dist = dist *  exp(- dist_0);
        dist = sin(dist*pi*8 + time_laps) + 1;
        dist = dist / 8;
        dist = abs(dist);
        dist = 0.01 / dist;
        dist = pow(dist, 1.2);

        // set out color
        finalColor += dist * cols;
    }


    outColor = vec4(finalColor, 1);
}
