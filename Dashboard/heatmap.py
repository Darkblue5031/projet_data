import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np

csv_path = 'netflix_titles.csv'
df = pd.read_csv(csv_path)

country_counts = df['country'].value_counts()


plt.figure(figsize=(10, 5))
m = Basemap(projection='mill', llcrnrlat=-60, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180)


m.drawcoastlines()
m.drawcountries()

# Convertir les noms de pays en coordonnées de la carte
for country, count in country_counts.items():
    try:
        # Obtenir les coordonnées du centre du pays
        country_latlon = m(0, 0)  # Emplacement fictif
        m.scatter(country_latlon[0], country_latlon[1], s=count, c=count, cmap='YlOrRd', alpha=0.7, edgecolors='k', zorder=10)
    except IndexError:
        # Ignorer les pays sans coordonnées
        pass

# Ajouter une barre de couleur
sm = plt.cm.ScalarMappable(cmap='YlOrRd', norm=plt.Normalize(vmin=0, vmax=max(country_counts)))
sm._A = []
plt.colorbar(sm, ax=plt.gca(), label='Nombre de titres Netflix')

# Titre et affichage
plt.title('Heatmap du monde basée sur le nombre de titres Netflix par pays')
plt.show()
