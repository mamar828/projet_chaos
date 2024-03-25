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
uniform vec2 u_resolution;


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

    return color * (ambient + (diffuse + specular));
}

void main() {
    float gamma = 2.2;
    vec3 color = texture(u_texture_0, uv_0).rgb;
    color = pow(color, vec3(gamma));
    color = get_light(color);

    color = pow(color, 1 / vec3(gamma));
    fragColor = vec4(color, 1.0);
}


/* #version 330 core

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
uniform vec2 u_resolution;


vec3 get_light(vec3 color) {
    vec3 Normal = normalize(normal);

    //  Ambient lighting
    vec3 ambient = light.Ia;
    
    // Diffuse lighting
    vec3 lightDir = normalize(light.position - fragPos);
    float diff = max(0, dot(lightDir, Normal));
    float diffuseCutoff = 0.1; // Adjust as needed
    diff = max(diff, diffuseCutoff);

    vec3 diffuse = diff * light.Id;

    // Specular lighting
    vec3 viewDir = normalize(camPos - fragPos);
    vec3 reflectDir = reflect(-lightDir, Normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0), 32);     // 32 determines the shining strength (reflection)
    vec3 specular = spec * light.Is;

    return color * (ambient + (diffuse + specular));
}

void main() {
    // Normal
    float gamma = 2.2;
    vec3 color = texture(u_texture_0, uv_0).rgb;
    color = pow(color, vec3(gamma));
    color = get_light(color);

    // Additional
    // Calculate normalized coordinates in the range [-1, 1]
    vec2 uv = (2.0 * gl_FragCoord.xy - u_resolution) / min(u_resolution.x, u_resolution.y);
    
    // Calculate sinusoidal function along the x-axis
    float sinValue = sin(uv.x * 10.0); // Adjust frequency as needed
    
    // Map sinusoidal function to color along the x-axis
    vec3 sinusoidalColor = vec3(sinValue * 0.5 + 0.5); // Map [-1, 1] to [0, 1]
    
    // Apply sinusoidal color to the final color
    color *= sinusoidalColor;

    // Apply gamma correction and output final color
    color = pow(color, 1 / vec3(gamma));
    fragColor = vec4(color, 1.0);
}
 */