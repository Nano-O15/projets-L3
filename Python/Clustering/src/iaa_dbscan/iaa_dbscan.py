# Intelligence Artificielle et Apprentissage
# OUKHEMANOU Mohand & LUCCHINI Gabriel L3-Y
# Projet
# DBSCAN (Density-Based Spatial Clustering of Applications with Noise) Clustering

import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors

bd = pd.read_csv(r"../../database/penguins_clean.csv")

data = bd[["bill_length_mm", "bill_depth_mm"]]

data_norm = (data - data.mean()) / data.std()

x = data.loc[:, ['bill_length_mm', 'bill_depth_mm']].values

# K-Nearest Neighbors
neighb = NearestNeighbors(n_neighbors=2)
nbrs = neighb.fit(x)
distances, indices = nbrs.kneighbors(x)

distances = np.sort(distances, axis=0)
distances = distances[:, 1]

plt.xlabel("Numbers of Data")
plt.ylabel("Distance between each Data")
plt.title("Nearest Neighbors")
plt.plot(distances)
plt.show()

# DBSCAN Clustering
dbscan = DBSCAN(eps=0.9, min_samples=4).fit(x)
labels = dbscan.labels_
bd['cluster'] = labels
bd.to_csv('../../database/penguins_dbscan_labels.csv', index=False)

print(bd)

n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)
print("Estimated number of clusters: %d" % n_clusters_)
print("Estimated number of noise points: %d" % n_noise_)

sns.scatterplot(x="bill_length_mm", y="bill_depth_mm",
                hue="species", palette="flare", data=bd)
plt.xlabel("Bill Length (mm)")
plt.ylabel("Bill Depth (mm)")
plt.title("Penguins Species Distribution")
plt.show()

sns.scatterplot(x="bill_length_mm", y="bill_depth_mm",
                hue="island", palette="flare", data=bd)
plt.xlabel("Bill Length (mm)")
plt.ylabel("Bill Depth (mm)")
plt.title("Penguins Island Distribution")
plt.show()

sns.scatterplot(x=x[:, 0], y=x[:, 1], hue="cluster", palette="flare", data=bd)
plt.xlabel("Bill Length (mm)")
plt.ylabel("Bill Depth (mm)")
plt.title("DBSCAN Clustering")
plt.show()
