#version 330

uniform sampler2D p3d_Texture2;

// Input from vertex shader
in vec2 texcoord;
in vec3 NORMAL;
in vec3 POSITION;

uniform mat4 p3d_ViewMatrix;
uniform mat4 p3d_ViewMatrixInverse;

const float PI = 3.1415926535897932384626433832795;

uniform struct p3d_LightSourceParameters {
  vec4 color;
  vec4 position;
  float constantAttenuation;
} p3d_LightSource[20];


uniform int LIGHTS;

// Output to the screen
out vec4 p3d_FragColor;



void main() {
  vec3 VIEW = vec3(p3d_ViewMatrix[2][0], p3d_ViewMatrix[2][1], p3d_ViewMatrix[2][2]);

  vec3 DIFFUSE_LIGHT = vec3(0);
  vec3 AMBIENT_LIGHT = vec3(0.45);
  vec3 SPECULAR_LIGHT = vec3(0);

  float roughness = .5;
  float power = 5;
  float multi = 1.6;

  vec3 d;

  int lights = 0;
  for (int i = 0; i < LIGHTS; i++) {
    if (p3d_LightSource[i].color == vec4(0)) {
      break;
    }
    lights++;
    bool IS_DIRECTIONAL = p3d_LightSource[i].position.w == 0.;
    vec3 direction = vec3(0);
    float directionalMultiplier = 1.;
    if (IS_DIRECTIONAL) {
      direction = -(p3d_ViewMatrixInverse * p3d_LightSource[i].position).xyz;
      d = direction;
      directionalMultiplier = 0.;
    } else {
      direction = -normalize(POSITION - (p3d_ViewMatrixInverse * p3d_LightSource[i].position).xyz);
    }
    vec3 LIGHT_COLOR = p3d_LightSource[i].color.xyz;
    float ATTENUATION = p3d_LightSource[i].constantAttenuation;

    vec3 contribution = round(clamp(dot(NORMAL, direction) + 0.2, 0.0, 1.0) * ATTENUATION * LIGHT_COLOR) / PI;
    contribution = clamp(contribution, 0., 1.);
    contribution *= multi;
    contribution = pow(contribution, vec3(power));
    contribution /= multi;
    DIFFUSE_LIGHT += contribution * PI;

    vec3 R = -reflect(direction, NORMAL);
    float RdotV = dot(R, VIEW);
    float mid = 1.0 - roughness;
    mid *= mid;
    float intensity = smoothstep(mid - roughness * 0.5, mid + roughness * 0.5, RdotV) * mid * 0.5;
    SPECULAR_LIGHT += 1.0 * clamp(round(intensity + 0.5) - 0.5 - roughness / 2., 0, 1) * ATTENUATION * LIGHT_COLOR;
  }

  vec4 color = vec4(texture(p3d_Texture2, texcoord).rgb * (SPECULAR_LIGHT + DIFFUSE_LIGHT + AMBIENT_LIGHT), texture(p3d_Texture2, texcoord).a);
//  color = vec4(d, 1);
//  color = vec4(d, 1);
  p3d_FragColor = color;
}