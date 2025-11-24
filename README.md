# VRP Optimizer – Vehicle Routing Problem con Streamlit

Este proyecto implementa un prototipo funcional para resolver el **Problema de Enrutamiento de Vehículos (VRP)** con capacidades utilizando Python.  
Incluye:

- Cálculo de distancias reales mediante la fórmula de Haversine  
- Modelado matemático del VRP capacitado  
- Resolución mediante solvers lineales enteros (PuLP)  
- Interfaz web construida con **Streamlit** para cargar datos y visualizar rutas  

---

## Descripción General

El sistema permite cargar un archivo Excel con clientes (coordenadas y demanda) y calcular rutas óptimas para una flota de vehículos que:

- Salen desde un depósito (id = 0)
- Tienen capacidad máxima por vehículo
- Deben visitar cada cliente una sola vez
- Deben volver al depósito al finalizar

El solver minimiza la **distancia total recorrida** utilizando una matriz de distancias computada por la fórmula de Haversine.

El resultado final incluye:

- Rutas asignadas por cada vehículo  
- Distancia total recorrida  
- Tablas por vehículo  
- Validación automática de capacidad  

---

## Estructura del Proyecto
/vrp-prototype
│── examples/TAF.xlsx # Ejemplo de archivo de entrada
│── main.py # App principal de Streamlit
│── distance_matrix.py # Función de Haversine + matriz de distancias
│── requirements.txt # Dependencias del proyecto
│── vrp_solver.py # Modelo matemático del VRP (PuLP)


## Archivo de Entrada (Excel o CSV)

El archivo debe tener las siguientes columnas:

| id | lat | lon | demanda |
|----|-----|-----|---------|
| 0  | -34.6037 | -58.3816 | 0 |
| 1  | ...      | ...      | 5 |
| 2  | ...      | ...      | 8 |
| ... | ... | ... | ... |

- El **id = 0 debe ser el depósito** con demanda 0  
- Las coordenadas deben estar en columnas `lat` y `lon` como decimales  
- La demanda de cada cliente debe estar en `demanda` y ser entero

## Uso:
pip install -r requirements.txt

Para **lanzar** la app web:
cd vrp-prototype
streamlit run main.py

Luego **abrir** el navegador en:
http://localhost:8501


## Uso del Sistema

**Cargar** el **archivo** Excel con clientes y depósito

**Seleccionar**:
- **Cantidad** de vehículos
- **Capacidad** por vehículo

**Ejecutar optimización**

Visualizar:
- Rutas por vehículo
- Distancia total
- Tabla de movimientos
