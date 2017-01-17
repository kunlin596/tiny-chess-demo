#version 410

layout (location = 0) in vec3 position;
layout (location = 1) in vec3 color;
layout (location = 2) in vec3 normal;

uniform mat4 model_matrix;
uniform mat4 view_matrix;
uniform mat4 projection_matrix;

uniform vec3 uniform_color;
uniform vec3 light_position[2];

out vec3 to_light_vector[2];
out vec3 pass_color;
out vec3 surface_normal_vector;

void main () {
    vec4 world_position = model_matrix * vec4(position, 1.0);
    vec4 view_position = view_matrix * world_position;
    gl_Position = projection_matrix * view_position;
    pass_color = uniform_color;
    for (int i = 0; i < 2; ++i) {
        to_light_vector[i] = light_position[i] - world_position.xyz;
    }

    surface_normal_vector = (model_matrix * vec4(normal, 0.0)).xyz;

//    pass_color = vec3(uniform_color, uniform_color, uniform_color);
}
