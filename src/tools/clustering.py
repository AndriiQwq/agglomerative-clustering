import math
import copy

import numpy as np
from scipy.spatial.distance import pdist, squareform, cdist

def create_distance_table(clusters, mode=1):
    """Creates a distance table for the clusters."""
    if mode == 2:
        centers = np.array([cluster.metoid for cluster in clusters])
    else:
        centers = np.array([cluster.centroid for cluster in clusters])

    distances = squareform(pdist(centers, metric='euclidean'))
    return np.tril(distances)

def create_min_distances_table(clusters, distances_table):
    """Creates a table of minimum distances between clusters."""
    matrix_size = len(clusters)
    min_distances = [(float('inf'), -1) for _ in range(matrix_size)]

    for i in range(matrix_size):
        for j in range(i):
            distance = distances_table[i, j]
            if distance < min_distances[i][0]:
                min_distances[i] = (distance, j)
            if distance < min_distances[j][0]:
                min_distances[j] = (distance, i)

    return min_distances

def calculate_distance(first_point, second_point):
    """Calculates the Euclidean distance between two points."""
    x_diff = second_point[0] - first_point[0]
    y_diff = second_point[1] - first_point[1]
    return math.sqrt(x_diff ** 2 + y_diff ** 2)

def calculate_distance_between_centroid(first_cluster, second_cluster, mode=1):
    """Calculates distance between centroids or metoids of two clusters."""
    if mode == 2:
        return calculate_distance(first_cluster.metoid, second_cluster.metoid)
    else:
        return calculate_distance(first_cluster.centroid, second_cluster.centroid)

def find_min_distance_in_min_dist_table(min_distances_table):
    """Finds the minimum distance in the min_distances_table."""
    distances = np.array([distance for distance, _ in min_distances_table])
    min_index = np.argmin(distances)
    min_distance, cluster = min_distances_table[min_index]
    return min_index, cluster

def merge_closest_pairs(clusters, distances_table, min_distances_table, linkage=1):
    """Merges the closest pairs of clusters based on the distance table."""
    matrix_size = len(clusters)

    shortest_distance = find_min_distance_in_min_dist_table(min_distances_table)
    first_min_index = shortest_distance[0]
    second_min_index = shortest_distance[1]

    if first_min_index > second_min_index:
        first_min_index, second_min_index = second_min_index, first_min_index


    for j in range(first_min_index):
        if linkage == 1:
            distance = distances_table[first_min_index, j] if distances_table[first_min_index, j] < distances_table[second_min_index, j] else distances_table[second_min_index, j]
        else:
            distance = calculate_distance_between_centroid(clusters[first_min_index], clusters[j])
        distances_table[first_min_index, j] = distance

    for j in range(second_min_index + 1, matrix_size):
        if linkage == 1:
            distance = distances_table[j, first_min_index] if distances_table[j, first_min_index] < distances_table[j, second_min_index] else distances_table[j, second_min_index]
        else:
            distance = calculate_distance_between_centroid(clusters[first_min_index], clusters[j])
        distances_table[j, first_min_index] = distance

    distances_table = np.delete(distances_table, second_min_index, axis=0)
    distances_table = np.delete(distances_table, second_min_index, axis=1)

    clusters[first_min_index].add_points(clusters[second_min_index].points)
    del clusters[second_min_index]

    """Update min_distances_table"""
    matrix_size -= 1
    min_distances_table.pop(second_min_index)

    min_distance_for_first = (float('inf'), -1)
    for i in range(matrix_size):
        if i != first_min_index:
            if linkage == 1:
                distance = distances_table[first_min_index, i] if i < first_min_index else distances_table[
                    i, first_min_index]
            else:
                distance = calculate_distance_between_centroid(clusters[first_min_index], clusters[i])

            if distance < min_distance_for_first[0]:
                min_distance_for_first = (distance, i)

            if min_distances_table[i][1] == first_min_index or distance < min_distances_table[i][0]:
                min_distances_table[i] = (distance, first_min_index)

        if min_distances_table[i][1] == second_min_index:
            min_distances_table[i] = (float('inf'), -1)
        elif min_distances_table[i][1] > second_min_index:
            min_distances_table[i] = (min_distances_table[i][0], min_distances_table[i][1] - 1)

    min_distances_table[first_min_index] = min_distance_for_first
    
    return clusters, distances_table, min_distances_table

def agglomerative_clustering(clusters, distances_table, min_distances_table, mode, linkage, lim):
    """Performs agglomerative clustering on the given clusters."""
    previous_clusters = None

    while True:
        if len(clusters) < lim:
            previous_clusters = copy.deepcopy(clusters)
            clusters, distances_table, min_distances_table = merge_closest_pairs(clusters, distances_table, min_distances_table, linkage)

            for cluster in clusters:
                if mode == 2:
                    distances = cdist(cluster.points, [cluster.metoid])
                else:
                    distances = cdist(cluster.points, [cluster.centroid])

                if np.mean(distances) >= 500:
                    print("Go back")
                    clusters = previous_clusters
                    return clusters, distances_table, min_distances_table
        else:
            clusters, distances_table, min_distances_table = merge_closest_pairs(clusters, distances_table, min_distances_table, linkage)


def print_clustering_results(clusters, mode=1):
    """Prints clustering results and calculates success rate."""
    successful_clusters = 0
    total_clusters = len(clusters)
    it = 1
    for cluster in clusters:
        if mode == 2:
            distances = cdist(cluster.points, [cluster.metoid])
            print(f"Cluster {it} with {len(cluster.points)} points, Metoid: {cluster.metoid}, Mean distance: {np.mean(distances)}")
        else:
            distances = cdist(cluster.points, [cluster.centroid])
            print(f"Cluster {it} with {len(cluster.points)} points, Centroid: {cluster.centroid}, Mean distance: {np.mean(distances)}")

        if np.mean(distances) < 500:
            print("Successful clustering")
            successful_clusters += 1
        else:
            print("Unsuccessful clustering")
        it += 1
    success_rate = (successful_clusters / total_clusters) * 100
    print(f"Success rate of clustering: {success_rate:.2f}%")

def calculate_average_center(clusters, mode=1):
    """Calculates the average center of all clusters for visualization centroid/medoid."""
    if mode == 2:
        centers = np.array([cluster.metoid for cluster in clusters])
    else:
        centers = np.array([cluster.centroid for cluster in clusters])

    return np.mean(centers, axis=0)