from data_loader import load_data
from distance_matrix import build_distance_matrix
from solver import run_from_file

if __name__ == "__main__":
    # Ajustar estos parámetros para pruebas
    file_path = "/workspaces/TAF_Optimizacion_Prototipo/vrp-prototype/examples/pedidos.xlsx"
    vehicle_count = 3
    vehicle_capacity = 7.0
    time_limit = 30  # segundos

    result, out_df = run_from_file(file_path, vehicle_count, vehicle_capacity, time_limit)
