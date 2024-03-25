#version 330 core

// Use the fragColor variable to set the color of each pixel.
layout (location = 0) out vec4 fragColor;

in vec2 uv_0;
in vec3 normal;
in vec3 fragPos;
in vec4 shadow_coord;

struct Light {
    vec3 position;
	vec3 Ia;
    vec3 Id;
    vec3 Is;
};

uniform Light light;
uniform sampler2D u_texture_0;
uniform vec3 camPos;
// uniform float texture_width;
// uniform float texture_height;
uniform sampler2DShadow shadow_map;
uniform vec2 u_resolution;



float lookup(float ox, float oy) {
    vec2 pixel_offset = 1 / u_resolution;
    return textureProj(shadow_map, shadow_coord + vec4(ox * pixel_offset.x * shadow_coord.w,
                                                       oy * pixel_offset.x * shadow_coord.w, 0.0, 0.0));

}


float get_soft_shadow_x16() {
    float shadow;
    float swidth = 1.0;
    float endp = swidth * 1.5;
    for (float y = -endp; y <= endp; y += swidth) {
        for (float x = -endp; x <= endp; x += swidth) {
            shadow += lookup(x, y);
        }
    }
    return shadow / 16;
}


float getSoftShadowX4() {
    float shadow;
    float swidth = 2.0;  // shadow spread
    vec2 offset = mod(floor(gl_FragCoord.xy), 2.0) * swidth;
    shadow += lookup(-2.0 * swidth + offset.x, 2.0 * swidth - offset.y);
    shadow += lookup(-2.0 * swidth + offset.x, -1.0 * swidth - offset.y);
    shadow += lookup( 1.0 * swidth + offset.x, 2.0 * swidth - offset.y);
    shadow += lookup( 1.0 * swidth + offset.x, -1.0 * swidth - offset.y);
    return shadow / 4.0;
}


float get_shadow() {
    float shadow = textureProj(shadow_map, shadow_coord);
    return shadow;
}


vec3 get_light(vec3 color) {
    vec3 Normal = normalize(normal);

    //  Ambient lighting
    vec3 ambient = light.Ia;
    
    // Diffuse lighting
    vec3 lightDir = normalize(light.position - fragPos);
    float diff = max(0, dot(lightDir, Normal));
    // diff = min(0.1, diff);
    float diffuseCutoff = 0.1; // Adjust as needed
    diff = max(diff, diffuseCutoff);

    vec3 diffuse = diff * light.Id;
    // vec3 diffuse = clamp(diff * light.Id, vec3(0.0)) * color;

    // Specular lighting
    vec3 viewDir = normalize(camPos - fragPos);
    vec3 reflectDir = reflect(-lightDir, Normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0), 32);     // 32 determines the shining strength (reflection)
    vec3 specular = spec * light.Is;

    // Shadow component
    float shadow = get_shadow();

    return color * (ambient + (diffuse + specular) * shadow);
}

void main() {
    float gamma = 2.2;
    vec3 color = texture(u_texture_0, uv_0).rgb;
    // vec3 color = texture(u_texture_0, uv_0 + vec2(1.0 / texture_width, 1.0 / texture_height) * 0.5).rgb;
    // vec3 color = vec3(uv_0, 0);
    color = pow(color, vec3(gamma));
    color = get_light(color);

    color = pow(color, 1 / vec3(gamma));
    fragColor = vec4(color, 1.0);
}
