import numpy as np
from geopy.geocoders import Nominatim
import pandas as pd

# Initialisation du géocodeur
geolocator = Nominatim(user_agent="my-App")

def get_country_coordinates(country):
    if pd.isna(country):
        return np.nan, np.nan
    location = geolocator.geocode(country)
    print(location)
    if location:
        print(location.latitude, location.longitude)
        return location.latitude, location.longitude
    else:
        return np.nan, np.nan

# Chemin vers le fichier CSV
csv_path = 'netflix_titles.csv'

# Lecture du fichier CSV
df = pd.read_csv(csv_path)

# Obtenir les coordonnées pour chaque pays
df['latitude'], df['longitude'] = zip(*df['country'].apply(get_country_coordinates))


print(df[['country', 'latitude', 'longitude']].head(10))
