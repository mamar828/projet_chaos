#version 330 core
layout (location = 0) out vec4 fragColor;

uniform vec2 u_resolution; 
uniform float u_time;
const float EPSILON = 0.001;
const float MAX_DIST = 1000.0;
const float STEPS = 300.0;
const float PI = acos(-1.0);

float noise(vec2 p) {
    return sin(p[0]) + sin(p[1]);
}

float getTerrain(vec3 p) {
    float d = 0;
    d += noise(p.xz);
    d += p.y + 2.0;
    return d;
}


float map(vec3 p) {
    float d = 0.0;
    d += getTerrain(p);
    return d;
}

float rayMarch(vec3 ro, vec3 rd) {
    float dist = 0.0;
    for (int i = 0; i < STEPS; i++) {
        vec3 p = ro + dist * rd;
        float hit = map(p);
        if (abs(hit) < EPSILON) break;
        dist += hit;
        if (dist > MAX_DIST) break;
    }
    return dist;
}


vec3 getNormal (vec3 p) {
    vec2 e = vec2(EPSILON, 0.0);
    vec3 n = vec3(map(p)) - vec3(map(p - e.xyy), map(p - e.yxy), map(p - e.yyx));
    return normalize(n);
}

vec3 lightPos = vec3(250.0, 100.0, -300.0);

vec3 getLight(vec3 p, vec3 rd) {
    vec3 color = vec3(1);
    vec3 l = normalize(lightPos - p);
    vec3 normal = getNormal(p);
    vec3 v = -rd;
    vec3 r = reflect(-l, normal);
    
    float diff = 0.85 * max(dot(l, normal), 0.0);
    float specular = 0.4 * pow(clamp(dot(r, v), 0.0, 1.0), 10.0);
    float ambient = 0.2;
    return (ambient + specular + diff) * color;
}

mat3 getCam(vec3 ro, vec3 lookAt) {
    vec3 camF = normalize(vec3(lookAt - ro));
    vec3 camR = normalize(cross(vec3(0, 1, 0), camF));
    vec3 camU = cross(camF, camR);
    return mat3(camR, camU, camF);
}

vec3 render(vec2 uv) {
    vec3 col = vec3(0);
    vec3 ro = vec3(0.0, 1.0, -3.0);
    vec3 lookAt = vec3(0, 0, 0) ;
    vec3 rd = getCam(ro, lookAt) * normalize(vec3(uv, 2.0));

    float dist = rayMarch(ro, rd);
    vec3 p = ro + dist * rd;
    if (dist < MAX_DIST) {
        col += getLight(p, rd);
    }
    return col;
}

void main() {
    vec2 uv = (2.0 * gl_FragCoord.xy - u_resolution.xy) / u_resolution.y;
    vec3 color = render(uv);
    fragColor = vec4(pow(color, vec3(2.2)), 1.0);
}