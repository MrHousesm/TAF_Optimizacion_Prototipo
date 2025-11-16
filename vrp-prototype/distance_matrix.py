import numpy as np

# Distancia Haversine entre dos puntos en km.
def haversine(lat1, lon1, lat2, lon2):

    R = 6371  # Radio tierra
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

# Construye una matriz NxN de distancias con los puntos del DataFrame.
def build_distance_matrix(df):

    n = len(df)
    matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i][j] = haversine(df.loc[i, "lat"], df.loc[i, "lon"],
                                         df.loc[j, "lat"], df.loc[j, "lon"])
    return matrix
