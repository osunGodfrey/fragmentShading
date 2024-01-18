#version 410 core

in vec3 fragColor;
in vec2 texture_coords;
in vec2 fragCoord;

out vec4 outColor;

uniform float iTime; // time laps
uniform vec2 sResolution;
uniform vec4 mouseInput;
// uniform vec2 iResolution;

// global variables
vec2 iResolution = vec2(1.0, 1.0);

// open code

// call open code
void main(){ 
    // Normalized coordinates
    vec2 p = (2.0*gl_FragCoord.xy - sResolution) / min(sResolution.x, sResolution.y);
    
    // Time-dependent value for animation
    float time = iTime * 0.2;

    // Creating a pattern using sine and cosine functions
    float pattern = sin(p.x * 10.0 + time) * cos(p.y * 10.0 + time);

    // Mapping pattern to color
    vec3 color = vec3(0.5 + 0.5 * cos(pattern + time), pattern, time);

    // Output final color
    outColor = vec4(color, 1.0);
}


