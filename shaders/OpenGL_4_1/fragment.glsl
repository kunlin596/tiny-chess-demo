#version 410

in vec3 pass_color;
in vec3 to_light_vector[2];
in vec3 surface_normal_vector;

uniform vec3 light_color[2];

out vec4 out_color;

void main () {
    vec3 normalized_normal = normalize(surface_normal_vector);
    vec3 total_diffuse = vec3(0.0);
    vec3 total_specular = vec3(0.0);

    for (int i = 0; i < 2; ++i) {
        float distance = length(to_light_vector[i]);
        vec3 normalized_to_light = normalize(to_light_vector[i]);
        float brightness = max(dot(normalized_normal, normalized_to_light), 0.0);

        total_diffuse += total_diffuse + brightness * light_color[i];
    }

    total_diffuse = max(total_diffuse, 0.2);

    out_color = vec4(total_diffuse, 1.0) * vec4(pass_color, 1.0);
}
