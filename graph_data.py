import math
from typing import Dict

# Definición de nodos con tiempo estimado de visita (minutos)
# IMPORTANTE: Coordenadas verificadas desde Google Maps
CUENCA_NODES: Dict[str, Dict[str, float]] = {
    # Puntos originales (verificados)
    "Catedral Nueva": {"lat": -2.8975, "lon": -79.0050, "descripcion": "Centro histórico de Cuenca", "tiempo": 60},
    "Parque Calderón": {"lat": -2.89741, "lon": -79.00438, "descripcion": "Corazón de Cuenca", "tiempo": 45},
    "Puente Roto": {"lat": -2.90423, "lon": -79.00142, "descripcion": "Monumento histórico", "tiempo": 30},
    "Museo Pumapungo": {"lat": -2.90607, "lon": -78.99681, "descripcion": "Museo de antropología", "tiempo": 60},
    "Terminal Terrestre": {"lat": -2.89222, "lon": -78.99277, "descripcion": "Terminal de autobuses", "tiempo": 20},
    "Mirador de Turi": {"lat": -2.92583, "lon": -79.00400, "descripcion": "Mirador con vista panorámica", "tiempo": 45},
    
    # 10 NUEVOS LUGARES - COORDENADAS CORREGIDAS (verificadas en Google Maps)
    "Iglesia de Santo Domingo": {"lat": -2.89600, "lon": -79.00450, "descripcion": "Iglesia colonial con arquitectura barroca", "tiempo": 40},
    "Museo de la Ciudad": {"lat": -2.90305, "lon": -79.00161, "descripcion": "Museo de historia local", "tiempo": 50},
    "Plaza de las Flores": {"lat": -2.89742, "lon": -79.00573, "descripcion": "Mercado de flores tradicional", "tiempo": 25},
    "Museo Remigio Crespo Toral": {"lat": -2.90173, "lon": -79.00401, "descripcion": "Museo de arte y cultura", "tiempo": 45},
    "Parque de San Blas": {"lat": -2.89784, "lon": -78.99856, "descripcion": "Parque histórico del barrio bohemio", "tiempo": 30},
    "Iglesia de San Blas": {"lat": -2.89749, "lon": -78.99766, "descripcion": "Iglesia del barrio tradicional", "tiempo": 35},
    "Carmen de la Asunción": {"lat": -2.89759, "lon": -79.00565, "descripcion": "Iglesia colonial con plaza de flores", "tiempo": 35},
    "Puente de Todos Santos": {"lat": -2.90561, "lon": -79.00001, "descripcion": "Puente histórico sobre el río Tomebamba", "tiempo": 20},
    "Museo Manuel Agustín Landívar": {"lat": -2.90470, "lon": -78.99951, "descripcion": "Casa museo de arte religioso", "tiempo": 40},
    "Escalinata": {"lat": -2.90240, "lon": -79.00272, "descripcion": "Escaleras icónicas junto al río", "tiempo": 25},
}

# Definición de aristas (conexiones) - Optimizada según distancias reales
GRAPH_EDGES = {
    # Conexiones originales mejoradas
    "Catedral Nueva": ["Parque Calderón", "Plaza de las Flores", "Carmen de la Asunción", "Iglesia de Santo Domingo"],
    "Parque Calderón": ["Catedral Nueva", "Terminal Terrestre", "Parque de San Blas", "Iglesia de San Blas"],
    "Puente Roto": ["Museo Pumapungo", "Escalinata", "Museo de la Ciudad", "Museo Remigio Crespo Toral"],
    "Museo Pumapungo": ["Puente Roto", "Terminal Terrestre", "Parque de San Blas", "Iglesia de San Blas", "Museo Manuel Agustín Landívar", "Puente de Todos Santos"],
    "Terminal Terrestre": ["Parque Calderón", "Museo Pumapungo", "Mirador de Turi", "Parque de San Blas", "Iglesia de San Blas"],
    "Mirador de Turi": ["Terminal Terrestre"],
    
    # Conexiones de los 10 nuevos lugares (basadas en proximidad geográfica real)
    "Iglesia de Santo Domingo": ["Catedral Nueva", "Plaza de las Flores", "Carmen de la Asunción", "Parque Calderón"],
    "Museo de la Ciudad": ["Puente Roto", "Museo Remigio Crespo Toral", "Escalinata"],
    "Plaza de las Flores": ["Catedral Nueva", "Carmen de la Asunción", "Iglesia de Santo Domingo"],
    "Museo Remigio Crespo Toral": ["Museo de la Ciudad", "Puente Roto", "Escalinata", "Puente de Todos Santos", "Museo Pumapungo"],
    "Parque de San Blas": ["Terminal Terrestre", "Parque Calderón", "Iglesia de San Blas", "Museo Pumapungo"],
    "Iglesia de San Blas": ["Parque de San Blas", "Terminal Terrestre", "Museo Pumapungo", "Parque Calderón", "Museo Manuel Agustín Landívar"],
    "Carmen de la Asunción": ["Plaza de las Flores", "Catedral Nueva", "Iglesia de Santo Domingo"],
    "Puente de Todos Santos": ["Museo Pumapungo", "Museo Manuel Agustín Landívar", "Museo Remigio Crespo Toral"],
    "Museo Manuel Agustín Landívar": ["Puente de Todos Santos", "Museo Pumapungo", "Iglesia de San Blas"],
    "Escalinata": ["Puente Roto", "Museo de la Ciudad", "Museo Remigio Crespo Toral"],
}

# Función de distancia Haversine (más precisa para coordenadas geográficas)
def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calcula la distancia entre dos puntos en la superficie terrestre usando la fórmula de Haversine.
    
    Args:
        lat1, lon1: Coordenadas del primer punto (en grados)
        lat2, lon2: Coordenadas del segundo punto (en grados)
    
    Returns:
        Distancia en kilómetros
    """
    R = 6371.0  # Radio de la Tierra en kilómetros
    
    # Convertir grados a radianes
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    # Fórmula de Haversine
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c

# Función de distancia Euclidiana aproximada (para heurística A*)
def euclidean_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calcula una aproximación de la distancia euclidiana entre dos coordenadas.
    Útil como heurística para el algoritmo A*.
    
    Args:
        lat1, lon1: Coordenadas del primer punto (en grados)
        lat2, lon2: Coordenadas del segundo punto (en grados)
    
    Returns:
        Distancia aproximada en kilómetros
    """
    # Factor de conversión aproximado: 1 grado ≈ 111 km
    return math.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2) * 111.0