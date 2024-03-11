# Intelligence Artificielle et Apprentissage
# OUKHEMANOU Mohand & LUCCHINI Gabriel L3-Y
# Projet - Ajustement de la BD

import pandas as pd

bd = pd.read_csv("penguins.csv")

bd = bd.drop("sex", axis='columns')

bd = bd.drop("year", axis='columns')

bd = bd.dropna()

bd = bd.reset_index(drop=True)

bd.to_csv('penguins_clean.csv', index=True)

bd = bd.drop("Unnamed: 0", axis='columns')

bd.to_csv('penguins_clean.csv', index=True)

