
Clustering DBSCAN example
=========================

## About
It's an example django app with implementation of clustering DBSCAN algorithm. It allows group some table data (users, for example) by given criteria (location + related table data, e.g. hobby name).

As DBSCAN is unsupervised ml algorithm, number of clusters will calculates dinamically.
Clusterization may took some time, so preferable to run it asyncrhoniously.
To make installation more plastic, use Docker containers: `docker-compose up`