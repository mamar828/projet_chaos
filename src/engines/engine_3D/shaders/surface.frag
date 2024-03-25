#version 330 core

// Use the fragColor variable to set the color of each pixel.
layout (location = 0) out vec4 fragColor;

in vec2 uv_0;

uniform sampler2D u_texture_0;
uniform vec2 u_resolution;



void main() {
    vec3 color = texture(u_texture_0, uv_0).rgb;
    fragColor = vec4(color, 1.0);
}
