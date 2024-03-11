# Intelligence Artificielle et Apprentissage
# OUKHEMANOU Mohand & LUCCHINI Gabriel L3-Y
# Projet
# GMM (Gaussian Mixture Model) Clustering

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score

bd = pd.read_csv(r"../../database/penguins_clean.csv")

data = bd[["bill_length_mm", "bill_depth_mm",
           "flipper_length_mm", "body_mass_g"]]

data_norm = (data - data.mean()) / data.std()

# Silhouette
score = []
for i in range(2, 11):
    gmm = GaussianMixture(n_components=i)
    labels = gmm.fit_predict(data_norm)
    sil_score = silhouette_score(data_norm, labels)
    score.append(sil_score)

plt.plot(range(2, 11), score, marker='o')
plt.title('Clustering Quality')
plt.xlabel('Number of Clusters')
plt.ylabel('Slhouette Score')
plt.show()

# GMM Clustering
gmm = GaussianMixture(n_components=3)
labels = gmm.fit_predict(data_norm)
bd['cluster'] = labels
bd.to_csv('../../database/penguins_gmm_labels.csv', index=False)

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
plt.xlabel("Bill Length (mm)")
plt.ylabel("Bill Depth (mm)")
plt.title("GMM Clustering")
plt.show()
