# Intelligence Artificielle et Apprentissage
# OUKHEMANOU Mohand & LUCCHINI Gabriel L3-Y
# Projet
# K-Means Clustering 

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

bd = pd.read_csv(r"../../database/penguins_clean.csv")

data = bd[["bill_length_mm", "bill_depth_mm",
           "flipper_length_mm", "body_mass_g"]]

data_norm = (data - data.mean()) / data.std()

# SSE
sse = []
for i in range(1, 11):
    km = KMeans(n_clusters=i, init='random',
                n_init='auto', random_state=0)
    km.fit_predict(data_norm)
    sse.append(km.inertia_)

plt.plot(range(1, 11), sse, marker='o')
plt.title('Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('Inertia')
plt.show()

# Silhouette
score = []
for i in range(2, 11):
    km = KMeans(n_clusters=i, init='random',
                n_init='auto', random_state=0)
    km.fit_predict(data_norm)
    sil_score = silhouette_score(data_norm, km.labels_)
    score.append(sil_score)

plt.plot(range(2, 11), score, marker='o')
plt.title('Clustering Quality')
plt.xlabel('Number of Clusters')
plt.ylabel('Slhouette Score')
plt.show()

# K-Means Clustering
km = KMeans(n_clusters=3, init='random',
            n_init='auto', random_state=0)
km.fit_predict(data_norm)
bd['cluster'] = km.labels_
bd.to_csv('../../database/penguins_km_labels.csv', index=False)

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
plt.title("K-Means Clustering")
plt.show()
