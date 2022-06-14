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
    return fract(sin(dot(st.xy, vec2(0.830,0.290)))*  43758.5453123);
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

#define NUM_OCTAVES 4

float fbm(in vec2 st)
{
    float v = 0.0;
    float a = 0.5;
    vec2 shift = vec2(-0.550,-0.660);
    float frequency = 0.;
    float t = 0.01*(-time*130.0);

    mat2 rot = mat2((0.284), (0.5), (0.892), (0.292));

    for (int i = 0; i < NUM_OCTAVES; ++i) {
        v += a * noise(st);
        v += a * noise(st);
        st.x += st.y*frequency*2.221 + t*1.109*0.0162;
        st = rot * st * 2.0 + shift;
        a *= 0.5;
    }
    return v;
}

void main()
{

    float scale = 2.2;
    vec3 colour = vec3(0.);

    vec2 q = vec2(0.);
    q.x = fbm( fs_in.uvs + 0.02*time);
    q.y = fbm( fs_in.uvs + vec2(1.0));


    vec2 r = vec2(0.);
    r.x = fbm( fs_in.uvs + 0.13*q + vec2(-0.900,0.140)+ 0.030 * time );
    r.y = fbm( fs_in.uvs + -0.624*q + vec2(0.570,0.280)+ 0.606 * time);
    r.x += fbm( fs_in.uvs * scale + 1.568*q + vec2(0.490,0.360)+0.126*time);
    r.x -= fbm( fs_in.uvs * scale + 0.848*q + vec2(0.490,0.360)+0.126*time);
    r.x -= fbm( fs_in.uvs * scale + 2.192*q + vec2(0.490,0.360)+0.014*time);

    float f = fbm((fs_in.uvs * scale) +r);

    colour = mix(vec3(0.565,0.529,0.357),
                vec3(0.570,0.467,0.394),
                clamp((f*f)*3.552,0.9,1.0));

    colour = mix(colour,
                vec3(0.645,0.484,0.336),
                clamp(length(q),0.2,1.0));

    colour = mix(colour,
                vec3(0.785,0.616,0.384),
                clamp(length(r.x),0.6,1.0));

    fragColor = vec4(((f+.120*f*f+.6)*colour) * 0.676 ,1.) * texture(image, fs_in.uvs);
}