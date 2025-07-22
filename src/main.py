import time
import os
from visualizer import plot_initial_points, plot_all_points, visualize_clusters
from config_manager import ConfigManager
from tools.points_generator import generate_initial_points, generate_additional_points

from tools.clustering import agglomerative_clustering, create_distance_table, create_min_distances_table, print_clustering_results
from cluster import Cluster

def main():
    program_start_time = time.time()

    # Load configuration
    config_manager = ConfigManager()
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.ini')
    config_manager.load_ini_config(os.path.abspath(config_path))
    
    # Extract parameters from config
    params = {
        'size_of_points_to_generate': config_manager.get('size_of_points_to_generate'),
        'size_of_first_points': config_manager.get('size_of_first_points'),
        'X_offset_min': config_manager.get('X_offset_min'),
        'X_offset_max': config_manager.get('X_offset_max'),
        'Y_offset_min': config_manager.get('Y_offset_min'),
        'Y_offset_max': config_manager.get('Y_offset_max'),
        'x_min': config_manager.get('x_min'),
        'x_max': config_manager.get('x_max'),
        'y_min': config_manager.get('y_min'),
        'y_max': config_manager.get('y_max'),
        'mode': config_manager.get('mode'),
        'linkage': config_manager.get('linkage')
    }

    points = set()

    # Generate initial points
    initial_points_array = generate_initial_points(points, params)

    # Create additional points
    all_points_array = generate_additional_points(points, params)

    # Create clusters
    start_time = time.time()
    clusters = [Cluster([point], params['mode']) for point in points]
    end_time = time.time()
    print(f"clusters creation time: {end_time - start_time} seconds")

    # Create distance table with [dist and cluster]
    start_time = time.time()
    distances_table = create_distance_table(clusters, params['mode'])
    end_time = time.time()
    print(f"distances_table creation time: {end_time - start_time} seconds")

    # Create min distances table
    start_time = time.time()
    min_distances_table = create_min_distances_table(clusters, distances_table)
    end_time = time.time()
    print(f"create_min_distances_table creation time: {end_time - start_time} seconds")

    lim = int(params['size_of_first_points'] * 1.5)
    clusters, distances_table, min_distances_table = agglomerative_clustering(clusters, distances_table, min_distances_table, params['mode'], params['linkage'], lim)

    print_clustering_results(clusters, params['mode'])

    program_end_time = time.time()
    print(f"Program execution time: {program_end_time - program_start_time} seconds")

    # Visualization 
    plot_initial_points(initial_points_array)
    plot_all_points(all_points_array, params)
    visualize_clusters(clusters, params)


if __name__ == "__main__":
    main()