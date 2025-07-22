import matplotlib
import numpy as np
import matplotlib.colors as mcolors
import random

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def plot_initial_points(initial_points: np.ndarray):
    """Plots the initial 20 points."""
    plt.figure(figsize=(6, 6))
    plt.scatter(initial_points[:, 0], initial_points[:, 1], c='blue', s=10, label='Initial 20 Points')
    plt.title("Initial 20 Points")
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_all_points(all_points, params):
    """Plots all points including initial and generated points."""
    x_min = params['x_min']
    x_max = params['x_max']
    y_min = params['y_min']
    y_max = params['y_max']

    plt.figure(figsize=(6, 6))
    plt.scatter(all_points[:, 0], all_points[:, 1], c='red', s=1,
                label='All n Points')  # s=1 for better visibility
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.title("All n Points (Initial + Generated)")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.legend()
    plt.grid(True)
    plt.show()

def visualize_clusters(clusters, params):
    """Visualizes clusters and their centroids/medoids."""
    mode = params.get('mode', 1) # Default to centroid if mode is not set

    color_list = [
        'pink', 'lime', 'teal', 'lavender', 'turquoise', 'tan', 'gold', 'salmon', 'navy', 'coral',
        'blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'orange', 'purple', 'brown', 'black'
    ]
    num_clusters = len(clusters)
    if num_clusters > len(color_list):
        additional_colors = list(mcolors.CSS4_COLORS.keys())
        random.shuffle(additional_colors)
        color_list.extend(additional_colors[:num_clusters - len(color_list)])

    plt.figure(figsize=(10, 7))

    for i, cluster in enumerate(clusters):
        points = cluster.points
        color = color_list[i % len(color_list)]
        plt.scatter(points[:, 0], points[:, 1], s=30, color=color, label=f'Cluster {i + 1}')

        if mode == 2:
            plt.scatter(cluster.metoid[0], cluster.metoid[1], s=100, color=color, marker='X', edgecolor='k')
        else:
            plt.scatter(cluster.centroid[0], cluster.centroid[1], s=100, color=color, marker='X', edgecolor='k')

    from tools.clustering import calculate_average_center
    average_center = calculate_average_center(clusters, mode)
    plt.scatter(average_center[0], average_center[1], s=150, color='red', marker='o', edgecolor='k',
                label='Average Center')

    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("Cluster Visualization with Average Center")
    plt.legend()
    plt.show()