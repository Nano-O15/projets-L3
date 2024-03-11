# Intelligence Artificielle et Apprentissage
# OUKHEMANOU Mohand & LUCCHINI Gabriel L3-Y
# Projet
# Classification Ascendante Hiérarchique

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.cluster.hierarchy import fcluster

bd = pd.read_csv(r"../../database/penguins_clean.csv")

data = bd[["bill_length_mm", "bill_depth_mm",
           "flipper_length_mm", "body_mass_g"]]

data_norm = (data - data.mean()) / data.std()

dist_matrix = pdist(data_norm, metric="euclidean")

dist_sq = squareform(dist_matrix)

# Average Linkage
linkage_matrix = linkage(dist_matrix, method="average")

dendrogram(linkage_matrix, labels=bd.index.tolist())

plt.title('Dendrogram Average Linkage')
plt.show()

# Complete Linkage
linkage_matrix2 = linkage(dist_matrix, method="complete")

dendrogram(linkage_matrix2, labels=bd.index.tolist())

plt.title('Dendrogram Complete Linkage')
plt.show()

# Single Linkage
linkage_matrix3 = linkage(dist_matrix, method="single")

dendrogram(linkage_matrix3, labels=bd.index.tolist())

plt.title('Dendrogram Single Linkage')
plt.show()

# Ward Linkage
linkage_matrix4 = linkage(dist_matrix, method="ward")

dendrogram(linkage_matrix4, labels=bd.index.tolist())

plt.title('Dendrogram Ward Linkage')
plt.show()

# CAH Clustering (Ward Linkage)
labels = fcluster(linkage_matrix4, 3, criterion='maxclust')
bd['cluster'] = labels
bd.to_csv('../../database/penguins_cah_labels.csv', index=False)

print(bd)

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

sns.scatterplot(x="bill_length_mm", y="bill_depth_mm",
                hue="cluster", palette="flare", data=bd)
plt.xlabel("Bill Length (mm)")
plt.ylabel("Bill Depth (mm)")
plt.title("CAH Clustering")
plt.show()
