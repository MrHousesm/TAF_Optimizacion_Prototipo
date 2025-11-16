import pandas as pd

REQUIRED_COLUMNS = ["id", "lat", "lon", "demanda"]

# Carga archivo CSV/XLSX y valida columnas y tipos de datos.
def load_data(file_path):

    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Formato no soportado. Cargar CSV o XLSX.")

    # Validar esquema
    if not all(col in df.columns for col in REQUIRED_COLUMNS):
        raise ValueError(f"Columnas requeridas: {REQUIRED_COLUMNS}")

    # Validar tipos
    if not pd.api.types.is_numeric_dtype(df["lat"]) or not pd.api.types.is_numeric_dtype(df["lon"]):
        raise ValueError("Las columnas lat y lon deben ser numéricas.")


    if not pd.api.types.is_numeric_dtype(df["demanda"]):
        raise ValueError("La columna demanda debe ser numérica.")

    # Opcional: ordenar por id ascendente
    df = df.sort_values("id").reset_index(drop=True)

    return df
