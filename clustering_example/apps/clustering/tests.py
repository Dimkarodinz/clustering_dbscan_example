import random
import unittest
from clustering_example.apps.clustering import services
from .utils import generate_test_blobs


class TestClusterize(unittest.TestCase):
    def setUp(self):
        # 'generated_test_blobs' fn has 3 hardcoded geo centers
        self.test_coords, _ = generate_test_blobs()
        self.subject_fn = services.clusterize

    def test_clusterize_data(self):
        labels, _ = self.subject_fn(self.test_coords)
        unique_labels_cnt = len(set(labels)) - (1 if -1 in labels else 0)
        # between 3 and 4
        self.assertTrue(3 <= unique_labels_cnt <= 4)

    def test_return_indicies(self):
        labels, indicies = self.subject_fn(self.test_coords)
        _sample_valid_label = labels[indicies[0]]
        self.assertNotEqual(_sample_valid_label, -1)


class TestClustersInfo(unittest.TestCase):
    def setUp(self):
        # 'generated_test_blobs' fn has 3 hardcoded geo centers
        self._test_coords, _ = generate_test_blobs()
        self.labels, _ = services.clusterize(self._test_coords)

        self.subject_fn = services.clusters_info

    def test_show_uniq_labels(self):
        uniq_labels, _ = self.subject_fn(self.labels)
        self.assertTrue(3 <= len(uniq_labels) <= 4)

    def test_show_labels_count(self):
        _, labels_cnt = self.subject_fn(self.labels)
        self.assertTrue(3 <= labels_cnt <= 4)


class TestShowPlot(unittest.TestCase):
    def setUp(self):
        # 'generated_test_blobs' fn has 3 hardcoded geo centers
        self.test_coords, _ = generate_test_blobs(cluster_std=0.004)
        self.labels, self.indicies = services.clusterize(self.test_coords)

        self.subject_fn = services.show_plot

    def test_show_plot(self):
        try:
            self.subject_fn(source_data=self.test_coords,
                            labels=self.labels,
                            indicies=self.indicies)
        except SystemExit:
            return True


if __name__ == '__main__':
    unittest.main()
