/// Reference from: https://thebookofshaders.com/13/

#version 330 core
#define FRAG_COLOUR     0

precision mediump float;

in VertexData
{
    vec2 uvs;
    vec4 rgba;
} fs_in;

uniform float time;
uniform sampler2D image;
layout (location = FRAG_COLOUR, index = 0) out vec4 fragColor;

float random (in vec2 st)
{
    return fract(sin(dot(st.xy, vec2(0.630, 0.610))) *  43758.5453123);
}

float noise (in vec2 st)
{
    vec2 i = floor(st);
    vec2 f = fract(st);

        float a = random(i);
    float b = random(i + vec2(1.0, 0.0));
    float c = random(i + vec2(0.0, 1.0));
    float d = random(i + vec2(1.0, 1.0));

    vec2 u = f * f * (3.0 - 2.0 * f);

    return mix(a, b, u.x) +
            (c - a)* u.y * (1.0 - u.x) +
            (d - b) * u.x * u.y;
}

#define NUM_OCTAVES 5

float fbm(in vec2 st)
{
    float v = 0.0;
    float a = 0.5;
    vec2 shift = vec2(100.);
    float frequency = 0.;
    float t = 0.01*(-time*130.0);

    mat2 rot = mat2(cos(0.5), sin(0.5), -sin(0.5), cos(0.50));

    for (int i = 0; i < NUM_OCTAVES; ++i) {
        v += a * noise(st);
        st.x += sin(st.y*frequency*2.221 + t*1.109)*0.0162;
        st = rot * st * 2.0 + shift;
        a *= 0.5;
    }
    return v;
}

void main()
{
    //vec2 map_resolution = {1600, 1600};
    float scale = 12.2;
    vec3 colour = vec3(0.);

    vec2 q = vec2(0.);
    q.x = fbm(fs_in.uvs + 0.00*abs(sin(time)));
    q.y = fbm(fs_in.uvs + vec2(1.0));


    vec2 r = vec2(0.);
    r.x = fbm(fs_in.uvs * scale + 1.0*q + vec2(1.7, 9.2)+ 0.15*time);
    r.y = fbm(fs_in.uvs * scale + 1.0*q + vec2(8.3, 2.8)+ 0.126*time);
    r.y += fbm(fs_in.uvs * scale + 1.568*q + vec2(0.490, 0.360)+0.126*time);
    r.y += fbm(fs_in.uvs * scale + 0.848*q + vec2(0.490, 0.360)+0.126*time);
    r.y += fbm(fs_in.uvs * scale + 2.192*q + vec2(0.490, 0.360)+0.014*time);

    float f = fbm((fs_in.uvs * scale) +r);

    colour = mix(vec3(0.575, 0.530, 0.560),
    vec3(0.405, 0.399, 0.350),
    clamp((f*f)*3.808, 0.0, 1.0));

    colour = mix(colour,
    vec3(0.156, 0.157, 0.165),
    clamp(length(q), 0.0, 0.240));

    colour = mix(colour,
    vec3(0.890, 0.834, 0.851),
    clamp(length(r.x), 0.0, 1.0));

    fragColor = vec4((f+.6*f+.5)*colour, 1.) * texture(image, fs_in.uvs);
}
