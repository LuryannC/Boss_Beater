#version 330 core
#define FRAG_COLOUR     0

/// Reference: https://www.shadertoy.com/view/3sscRs#

in VertexData
{
    vec2 uvs;
    vec4 rgba;
} fs_in;

uniform float time;
layout (location = FRAG_COLOUR, index = 0) out vec4 fragColor;


void main()
{
    float scale = 930.9;
    mat3 rot = mat3(-2,-1,2, 3,-2,1, 1,2,2);
	vec3 pos = vec3(fs_in.uvs + time * 1e2, time * 1e1);
    float dist = 1.;

    float s[5] = float[5](.32,.28,.26, .22, .30);
    for(int i = 0; i < 5; i++)
    {
        pos *= rot * s[i] * 1.2;
        dist = min(dist, length(.5 - fract(pos / 1e1 * scale)));
    }
    fragColor = pow((dist), 7.)*10.+vec4(0.03,.61,.87,1.);
}


