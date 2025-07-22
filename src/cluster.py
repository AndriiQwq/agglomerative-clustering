import numpy as np
from scipy.spatial.distance import cdist

class Cluster:
    def __init__(self, points, mode=1):
        self.points = np.array(points)
        self.mode = mode

        if self.mode == 2:
            self.metoid = self.calculate_metoid()
        else:
            self.centroid = self.calculate_centroid()

    def calculate_centroid(self) -> np.ndarray:
        return np.mean(self.points, axis=0)

    def calculate_metoid(self) -> np.ndarray:
        distances = cdist(self.points, [self.calculate_centroid()])  # [self.centroid]
        closest = distances.argmin()
        return self.points[closest]

    def add_points(self, points: np.ndarray):
        self.points = np.vstack((self.points, points))

        if self.mode == 2:
            self.metoid = self.calculate_metoid()
        else:
            self.centroid = self.calculate_centroid()

    def __str__(self):
        if self.mode == 2:
            return f"Cluster with {len(self.points)} points, Metoid: {self.metoid}"
        else:
            return f"Cluster with {len(self.points)} points, Centroid: {self.centroid}"
