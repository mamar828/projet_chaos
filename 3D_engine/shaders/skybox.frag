#version 330 core

out vec4 frag_color;

in vec3 tex_cube_coords;

uniform samplerCube u_texture_skybox;

void main() {
    frag_color = texture(u_texture_skybox, tex_cube_coords);
}