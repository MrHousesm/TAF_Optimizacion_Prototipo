from typing import Tuple, List, Dict, Any
import pulp
import numpy as np

def solve_cvrp(distance_matrix: np.ndarray,
               demands: List[float],
               vehicle_count: int,
               vehicle_capacity: float,
               time_limit: int = None,
               solver_msg: bool = False) -> Dict[str, Any]:
    """
    Resuelve CVRP con PuLP (MTZ subtour elimination).
    Params:
        distance_matrix: NxN numpy array (km)
        demands: list length N (demanda en cada nodo, nodo 0 = deposito, demanda=0)
        vehicle_count: K (número máximo de vehículos)
        vehicle_capacity: Q
        time_limit: segundos para el solver (CBC), None = sin límite
        solver_msg: mostrar mensajes del solver
    Returns:
        dict con keys:
            'status': solution status
            'objective': valor objetivo (distancia)
            'x': dict (i,j) -> 0/1
            'u': dict i -> valor u_i
            'routes': list de rutas (cada ruta es lista de nodos empezando y terminando en 0)
    """
    n = distance_matrix.shape[0]
    nodes = list(range(n))

    # Crear problema
    prob = pulp.LpProblem("CVRP_MTZ", pulp.LpMinimize)

    # Variables x_ij binarias (no i==j)
    x = pulp.LpVariable.dicts('x', (nodes, nodes), lowBound=0, upBound=1, cat=pulp.LpBinary)
    # MTZ u_i continuous (uso rango [0, Q])
    u = pulp.LpVariable.dicts('u', nodes, lowBound=0, upBound=vehicle_capacity, cat=pulp.LpContinuous)

    # Objetivo: minimizar distancia total
    prob += pulp.lpSum(distance_matrix[i][j] * x[i][j] for i in nodes for j in nodes if i != j)

    # Restricciones
    # 1) Cada cliente j != 0 es visitado exactamente una vez (entrada=1)
    for j in nodes:
        if j == 0:
            continue
        prob += pulp.lpSum(x[i][j] for i in nodes if i != j) == 1, f"visit_once_in_{j}"

    # 2) Flujo conservación para clientes i != 0 (salida = entrada)
    for i in nodes:
        if i == 0:
            continue
        prob += (pulp.lpSum(x[i][j] for j in nodes if j != i) -
                 pulp.lpSum(x[j][i] for j in nodes if j != i)) == 0, f"flow_cons_{i}"

    # 3) Limitar número de rutas: salidas desde deposito <= K, entradas a deposito <= K
    prob += pulp.lpSum(x[0][j] for j in nodes if j != 0) <= vehicle_count, "departures_from_depot"
    prob += pulp.lpSum(x[i][0] for i in nodes if i != 0) <= vehicle_count, "returns_to_depot"

    # 4) MTZ subtour elimination + capacidad:
    # fijar u_0 = 0
    prob += u[0] == 0, "u_depot_zero"

    for i in nodes:
        if i == 0:
            continue
        # demanda <= u_i <= Q
        prob += u[i] >= demands[i], f"u_lower_{i}"
        prob += u[i] <= vehicle_capacity, f"u_upper_{i}"

    # MTZ constraints
    Q = vehicle_capacity
    for i in nodes:
        for j in nodes:
            if i == j or j == 0:
                continue
            prob += u[i] - u[j] + Q * x[i][j] <= Q - demands[j], f"mtz_{i}_{j}"

    # Resolver
    solver = pulp.PULP_CBC_CMD(msg=solver_msg, timeLimit=time_limit)  # CBC por defecto
    prob.solve(solver)

    status = pulp.LpStatus[prob.status]
    objective = pulp.value(prob.objective)

    # Extraer variables x
    x_sol = {}
    for i in nodes:
        for j in nodes:
            if i == j:
                continue
            val = pulp.value(x[i][j])
            x_sol[(i, j)] = 1 if val is not None and val > 0.5 else 0

    u_sol = {i: (pulp.value(u[i]) if pulp.value(u[i]) is not None else None) for i in nodes}

    # Reconstruir rutas a partir de x_sol
    routes = _extract_routes_from_x(x_sol, n, depot=0)

    return {
        'status': status,
        'objective': objective,
        'x': x_sol,
        'u': u_sol,
        'routes': routes
    }


# Construye rutas (listas de nodos) a partir de la matriz de adyacencia x_sol.
# Asume soluciones factibles (cada cliente tiene entrada 1 y salida 1).
def _extract_routes_from_x(x_sol: Dict[tuple, int], n: int, depot: int = 0) -> List[List[int]]:

    adjacency = {i: [] for i in range(n)}
    for (i, j), val in x_sol.items():
        if val == 1:
            adjacency[i].append(j)

    routes = []
    used = set()

    # Empezar por cada salida del depósito
    for j in adjacency[depot]:
        route = [depot]
        curr = j
        # Sigue hasta volver al depósito o hasta detectar loop infinito
        while curr != depot and curr not in route:
            route.append(curr)
            next_nodes = adjacency.get(curr, [])
            # si no hay siguiente, rompemos
            if len(next_nodes) == 0:
                break
            curr = next_nodes[0]  # debería ser 1 en soluciones correctas
        route.append(depot)
        # Mark nodes used
        for nd in route:
            used.add(nd)
        routes.append(route)

    # Si quedaron nodos no incluidos (por alguna razón), intentar construirlos
    remaining = set(range(n)) - used
    for node in list(remaining):
        if node == depot:
            continue
        route = [depot, node]
        curr = node
        while True:
            next_nodes = adjacency.get(curr, [])
            if len(next_nodes) == 0:
                route.append(depot)
                break
            curr = next_nodes[0]
            if curr == depot:
                route.append(depot)
                break
            route.append(curr)
        routes.append(route)

    return routes
