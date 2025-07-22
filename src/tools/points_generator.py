import random
import numpy as np

def generate_initial_points(points, params):
    """Generates initial points based on given parameters."""
    size_of_first_points = params['size_of_first_points']
    x_min = params['x_min']
    x_max = params['x_max']
    y_min = params['y_min']
    y_max = params['y_max']

    while len(points) < size_of_first_points:
        x = random.randint(x_min, x_max)
        y = random.randint(y_min, y_max)

        point = (x, y)
        if point not in points:
            points.add(point)

    return np.array(list(points))

def generate_additional_points(points, params):
    """Generates additional points based on existing points and given parameters."""
    size_of_points_to_generate = params['size_of_points_to_generate']
    size_of_first_points = params['size_of_first_points']
    X_offset_min = params['X_offset_min']
    X_offset_max = params['X_offset_max']
    Y_offset_min = params['Y_offset_min']
    Y_offset_max = params['Y_offset_max']
    x_min = params['x_min']
    x_max = params['x_max']
    y_min = params['y_min']
    y_max = params['y_max']

    while len(points) < size_of_points_to_generate + size_of_first_points:
        take_point = random.choice(list(points))

        x_offset = random.randint(X_offset_min, X_offset_max)
        y_offset = random.randint(Y_offset_min, Y_offset_max)

        new_x = take_point[0] + x_offset
        new_y = take_point[1] + y_offset

        if x_min < new_x < x_max and y_min < new_y < y_max:
            points.add((new_x, new_y))

    return np.array(list(points))