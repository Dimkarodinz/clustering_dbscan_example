import matplotlib.pyplot as plt
import numpy as np

from django.conf import settings
from sklearn.cluster import DBSCAN


def clusterize(narray, eps=settings.DBSCAN_EPS, min_samples=settings.DBSCAN_MIN_SAMPLES):
    """
    Clusterize numpy array using dbscan algorithm.

    Parameters
    ----------
    narray : array_like
        The shape and cluster data for finding cluster points

    eps : float
        Radius

    min_samples : number
        Number of neighboring points

    Returns
    -------
    labels : array_like
        Clustered labels points

    indicies: array_like
        Clustered label points indicies exluding noice points labels
    """
    # Instantiate dbscan
    dbscan = DBSCAN(eps=eps, min_samples=min_samples).fit(narray)

    # Cluster labels of each point
    labels = dbscan.labels_

    # Not noisy labels indexes (not -1 values) as narray
    indicies = dbscan.core_sample_indices_

    return labels, indicies


def clusters_info(labels):
    """Return uniq cluster labels and
    number of clusters ignoring noise (-1 values) if present.
    Returns
    -------
    labels : array_like
        Clustered labels points

    labels_cnt : int
        Number of unique clusters (excludeing noises)
    """
    unique_labels = set(labels)
    # Remove noisy label if present
    if -1 in unique_labels:
        unique_labels.remove(-1)
    labels_cnt = len(unique_labels)

    return unique_labels, labels_cnt


def show_plot(source_data, labels, indicies):
    # Black removed and is used for noise instead.
    unique_labels = set(labels)
    colors = [plt.cm.Spectral(each)
              for each in np.linspace(0, 1, len(unique_labels))]

    core_samples_mask = np.zeros_like(labels, dtype=bool)
    core_samples_mask[indicies] = True

    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.`
            col = [0, 0, 0, 1]

        # Compare each label and k, returns boolean narray
        class_member_mask = (labels == k)

        # classified results
        # class_member_mask & core_samples_mask > narray
        # if narray[narray] > narray filter (second bool narray)
        xy = source_data[class_member_mask & core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=14)

        # unclassified results
        xy = source_data[class_member_mask & ~core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=6)

    n_clusters_ = len(unique_labels) - (1 if -1 in unique_labels else 0)
    plt.title('Estimated number of clusters: %d' % n_clusters_)

    while True:
        try:
            plt.show()
        except UnicodeDecodeError:
            continue
        break


def clustering_normalize(query_set):
    """
    Transform query set to user locations ndarray
    for dbscan usage

    Return
    ______
    'locations list' : array_like
        Numpy array with lat, long float coorditaes

    'object id list' : array_like
        List with object ids
    """
    locations_list = list()
    user_ids = list()

    for obj in query_set:
        try:
            _l = obj.location
        except _l.DoesNotExist:
            next

        _payload = [float(_l.latitude), float(_l.longitude)]

        locations_list.append(_payload)
        user_ids.append(obj.id)

    return np.array(locations_list), user_ids


def clustering_denormalize(source_data, labels, indicies):
    """
    Transforms clustering payload into readable format

    Parameters
    __________
    source_data : array_like
        initial ndarray of unclustered data, with lat/lng

    labels : array_like
        clustered labels

    indicies : array_like
        clustered indicies

    Return
    ______
    # todo: change format to array-like

    clustered_data : array_like
        [{'label': 1, 'payload': array([1,2,3,4,5])]
    """
    output = list()
    unique_labels = set(labels)

    # Remove noise labels if present
    if -1 in unique_labels:
        unique_labels.remove(-1)

    core_samples_mask = np.zeros_like(labels, dtype=bool)
    core_samples_mask[indicies] = True

    for cluster_label in unique_labels:
        _payload = dict()

        class_member_mask = (labels == cluster_label)

        formatted_data = np.array(source_data)
        classified_results = formatted_data[class_member_mask & core_samples_mask]

        _payload['label'] = cluster_label
        _payload['payload'] = classified_results

        output.append(_payload)

    return output


def get_center(locations):
    """
    Calculate center point

    Parameter
    _________
    locations : array_like
        ndarray of lat and long pairs

    Returns
    _______
        lat_center, lng_center
    """
    def _get_center(points):
        max_point = max(points)
        min_point = min(points)
        center = float((max_point + min_point)) / 2.0
        return center

    # normalize locations data for comprehisions below
    if type(locations[0]) == np.ndarray:
        locations = locations[0]

    lats = [lat[0] for lat in locations]
    lngs = [lng[1] for lng in locations]

    lat_center = _get_center(lats)
    lng_center = _get_center(lngs)

    return lat_center, lng_center
