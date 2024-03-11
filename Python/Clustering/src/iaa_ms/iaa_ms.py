# Intelligence Artificielle et Apprentissage
# OUKHEMANOU Mohand & LUCCHINI Gabriel L3-Y
# Projet
# Mean-Shift Clustering

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.cluster import MeanShift
from sklearn.metrics import silhouette_score

bd = pd.read_csv(r"../../database/penguins_clean.csv")

data = bd[["bill_length_mm", "bill_depth_mm"]]

data_norm = (data - data.mean()) / data.std()

# Mean-Shift Clustering
ms = MeanShift(bandwidth=1)
ms.fit_predict(data_norm)
bd['cluster'] = ms.labels_
bd.to_csv('../../database/penguins_ms_labels.csv', index=False)

print(bd)

print("ms - silhouette: ", silhouette_score(data_norm, ms.labels_))

centers = ms.cluster_centers_
num_clusters = len(np.unique(ms.labels_))
print(f"Number of Clusters: {num_clusters}")

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

sns.scatterplot(x=data_norm.iloc[:, 0], y=data_norm.iloc[:,
                1], hue="cluster", palette="flare", data=bd)
sns.scatterplot(x=centers[:, 0], y=centers[:, 1],
                markers='x', s=100, linewidths=1, color='r')
plt.xlabel("Bill Length (mm)")
plt.ylabel("Bill Depth (mm)")
plt.title("Mean-Shift Clustering")
plt.show()
