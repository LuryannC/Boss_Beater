#version 330 core
#define FRAG_COLOUR     0
in VertexData
{
    vec2    uvs;
    vec4    rgba;
} fs_in;

uniform float time;
uniform vec2 sprite_size;
uniform vec2 u_mouse;
uniform vec3 rgb;
uniform sampler2D image;
layout  (location = FRAG_COLOUR, index = 0) out vec4 fragColor;

void main()
{
    vec2 st = fragColor.xy / sprite_size;

    fragColor = vec4(abs(cos(time)), abs(sin(time)), abs(atan(time)), 1.0) * texture(image, fs_in.uvs);
}
