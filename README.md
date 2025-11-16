# TAF_Optimizacion_Prototipo
Trabajo final de optimización hecho por el grupo 1: Balda Javier, Caracoix Juan y Casas Facundo. Este trabajo busca resolver un problema de optimización de rutas de vehículos capacitados con ventanas de tiempo (CVRPTW)

# Notas importantes
PuLP y solver: El wrapper usa CBC (el solver que viene con PuLP). Si tenés Gurobi o CPLEX en tu ambiente, podés cambiar el solver para mejor rendimiento (y tiempos más cortos).

MTZ es simple pero aumenta variables: Para instancias grandes (> 100 clientes) MTZ puede volver lento. Para TAF de curso, con datasets pequeños/medianos funciona bien.

Si el solver tarda o no encuentra soluciones integrales:

Aumentá time_limit.

Reducí K o usá heurísticas (Clarke-Wright, savings, k-means + TSP).

Considerá ortools (en un TAF se ve bien y es rápido para VRP).

Validaciones: data_loader.load_data ya valida columnas. Asegurate que la suma de demandas ≤ K*Q, si no el problema es infactible.

Interpretación de rutas: El output routes es una lista de rutas que empiezan y terminan en 0 (depósito). solution_routes.csv guarda route_id, route_nodes y route_length.