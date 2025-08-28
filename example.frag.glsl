#version 150

#define NUM_LIGHTS 2

uniform struct p3d_LightSourceParameters {
    vec4 color;
    vec4 position;
} p3d_LightSource[NUM_LIGHTS];

out vec4 fragColor;

void main() {
  fragColor = vec4(p3d_LightSource[0].position.xyz, 1);
}