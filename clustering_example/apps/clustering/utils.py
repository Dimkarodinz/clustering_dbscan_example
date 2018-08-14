import random
from sklearn.datasets.samples_generator import make_blobs


def generate_test_blobs(cluster_std=0.004, samples_cnt=100, centers=None):
    """Returs test array and test boolean labels"""

    if not centers:
        centers = [
          [50.434341, 30.527756],  # Kyiv fortress lat/lng
          [50.439966, 30.509405],  # University
          [50.458366, 30.523903]  # Goggle Ukraine
        ]

    return make_blobs(n_samples=samples_cnt, centers=centers,
                      cluster_std=cluster_std, random_state=0)
