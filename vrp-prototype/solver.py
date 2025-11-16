import numpy as np
import pandas as pd
from vrp_model import solve_cvrp
from data_loader import load_data
from distance_matrix import build_distance_matrix


# Carga datos, construye matriz y resuelve CVRP. Guarda resultados en 'solution_routes.csv' y devuelve el dict de resultados.
def run_from_file(file_path: str,
                  vehicle_count: int = 2,
                  vehicle_capacity: float = 10.0,
                  time_limit: int = 60):

    df = load_data(file_path)
    dist = build_distance_matrix(df)
    demands = df['demanda'].tolist()

    result = solve_cvrp(dist, demands, vehicle_count, vehicle_capacity, time_limit=time_limit, solver_msg=False)

    # Crear salida legible
    routes = result['routes']
    routes_str = []
    for idx, r in enumerate(routes):
        # convertir a ids
        routes_str.append({
            'route_id': idx,
            'route_nodes': r,
            'route_length': _route_length(r, dist)
        })

    out_df = pd.DataFrame(routes_str)
    out_df.to_csv("solution_routes.csv", index=False)

    # Imprimir resumen por consola
    print("Status:", result['status'])
    print("Objective (dist):", result['objective'])
    print(out_df)

    return result, out_df

def _route_length(route, dist_matrix):
    total = 0.0
    for i in range(len(route)-1):
        a = route[i]
        b = route[i+1]
        total += dist_matrix[a][b]
    return total

if __name__ == "__main__":
    # ejemplo de uso
    res, df_out = run_from_file("/workspaces/TAF_Optimizacion_Prototipo/vrp-prototype/examples/pedidos.xlsx", vehicle_count=2, vehicle_capacity=10.0, time_limit=30)
