#version 410

in vec3 pass_color;
in vec3 to_light_vector[2];
in vec3 surface_normal_vector;
in vec3 to_camera_vector;

uniform vec3 light_color[2];
uniform float shine_damper;
uniform float reflectivity;
out vec4 out_color;

void main () {
    vec3 normalized_normal = normalize(surface_normal_vector);
    vec3 normalized_camera = normalize(to_camera_vector);
    vec3 total_diffuse = vec3(0.0);
    vec3 total_specular = vec3(0.0);

    for (int i = 0; i < 2; ++i) {
        float distance = length(to_light_vector[i]);
        vec3 normalized_to_light = normalize(to_light_vector[i]);
        vec3 reflected_light_direction = reflect(-normalized_to_light, normalized_normal);

        float brightness = max(dot(normalized_normal, normalized_to_light), 0.0);
        float specular_factor = max(dot(reflected_light_direction, normalized_camera), 0.0);
        float dampedFactor = pow(specular_factor, shine_damper);

        total_diffuse = total_diffuse + brightness * light_color[i];
        total_specular = total_specular + dampedFactor * reflectivity * light_color[i];
    }

    total_diffuse = max(total_diffuse, 0.2);

    out_color = vec4(total_diffuse, 1.0) * vec4(pass_color, 1.0) + vec4(total_specular, 1.0);
}
