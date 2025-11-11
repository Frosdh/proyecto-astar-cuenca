import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
from astar import pathfinder
from graph_data import CUENCA_NODES

# Configuración de la página
st.set_page_config(page_title="Búsqueda de Rutas Óptimas en Cuenca", page_icon="🗺️", layout="wide")

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e88e5 0%, #42a5f5 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1.5rem;
    }
    .success-box {
        background: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .metric-box {
        background: white;
        border: 1px solid #ddd;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
    .route-path {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        font-size: 16px;
    }
    .section-header {
        background: #f8f9fa;
        padding: 0.8rem;
        border-left: 4px solid #1e88e5;
        margin: 1.5rem 0 1rem 0;
        font-weight: bold;
    }
    .stButton>button {
        background-color: #1e88e5;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        width: 100%;
    }
    .info-box {
        background: #e7f3ff;
        border: 1px solid #1e88e5;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown("""
<div class="main-header">
    <h1>🗺️ Búsqueda de Rutas Óptimas en Cuenca - Algoritmo A*</h1>
    <p style="margin: 0;">Esta aplicación implementa el algoritmo de búsqueda A* para encontrar la ruta más corta entre dos puntos de interés en la ciudad de Cuenca, Ecuador. El algoritmo combina la búsqueda informada con una heurística basada en distancia euclidiana para optimizar la exploración del espacio.</p>
</div>
""", unsafe_allow_html=True)

# Layout: Sidebar + Contenido principal
col_sidebar, col_main = st.columns([1, 3])

# ============= SIDEBAR =============
with col_sidebar:
    st.markdown("### ⚙️ Configuración de Búsqueda")
    
    st.markdown("**Selecciona el punto de INICIO**")
    start = st.selectbox("", sorted(CUENCA_NODES.keys()), key="start", label_visibility="collapsed")
    
    st.markdown("**Selecciona el punto de DESTINO**")
    goal = st.selectbox("", sorted(CUENCA_NODES.keys()), index=5, key="goal", label_visibility="collapsed")
    
    show_all = st.checkbox("Mostrar todos los nodos visitados en el mapa", value=False)
    
    calc_button = st.button("🔍 Buscar Ruta Óptima", type="primary")
    
    if st.button("🗑️ Limpiar"):
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("### ℹ️ Información")
    st.markdown("""
    **Asignatura:** Inteligencia Artificial  
    **Tema:** Algoritmos de Búsqueda en Python  
    **Aplicación:** Búsqueda de Rutas Óptimas en Cuenca
    
    **Total de Nodos:** 15 puntos de interés  
    **Algoritmo:** A* (A-Star)  
    **Heurística:** Distancia Euclidiana
    
    Desarrollado como parte de la práctica académica sobre algoritmos de búsqueda informada.
    """)
    
    st.markdown("---")
    
    st.markdown("### 📚 Guía Práctica")
    with st.expander("Ver todos los puntos de interés"):
        for node in sorted(CUENCA_NODES.keys()):
            tiempo = CUENCA_NODES[node].get('tiempo', 0)
            st.text(f"• {node} ({tiempo} min)")

# ============= CONTENIDO PRINCIPAL =============
with col_main:
    if calc_button:
        if start == goal:
            st.warning("⚠️ El punto de inicio y destino son el mismo. Por favor selecciona ubicaciones diferentes.")
        else:
            path, distance, visited_nodes = pathfinder.find_path(start, goal)
            
            if path is None:
                st.error("❌ No se encontró una ruta entre los puntos seleccionados.")
            else:
                # Calcular tiempo total de visita
                tiempo_total = sum(CUENCA_NODES[node].get('tiempo', 0) for node in path)
                
                # Mensaje de éxito
                st.markdown(f"""
                <div class="success-box">
                    ✅ <strong>¡Ruta encontrada!</strong> &nbsp;&nbsp; 🔵 Ruta: <strong>{start} → {goal}</strong>
                </div>
                """, unsafe_allow_html=True)
                
                # Métricas en 3 columnas
                metric_col1, metric_col2, metric_col3 = st.columns(3)
                
                with metric_col1:
                    st.markdown(f"""
                    <div class="metric-box">
                        <h4 style="margin: 0; color: #666;">📏 Distancia Total</h4>
                        <h2 style="margin: 10px 0; color: #1e88e5;">{distance:.2f} km</h2>
                    </div>
                    """, unsafe_allow_html=True)
                
                with metric_col2:
                    st.markdown(f"""
                    <div class="metric-box">
                        <h4 style="margin: 0; color: #666;">🔢 Nodos Explorados</h4>
                        <h2 style="margin: 10px 0; color: #1e88e5;">{visited_nodes}</h2>
                    </div>
                    """, unsafe_allow_html=True)
                
                with metric_col3:
                    st.markdown(f"""
                    <div class="metric-box">
                        <h4 style="margin: 0; color: #666;">⏱️ Tiempo Estimado</h4>
                        <h2 style="margin: 10px 0; color: #1e88e5;">{tiempo_total} min</h2>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Ruta encontrada
                route_display = " → ".join(path)
                st.markdown(f"""
                <div class="route-path">
                    <strong>🛣️ Ruta:</strong> {route_display}
                </div>
                """, unsafe_allow_html=True)
                
                # Detalles de la ruta
                st.markdown('<div class="section-header">📋 Detalles de la Ruta</div>', unsafe_allow_html=True)
                
                route_data = []
                for i in range(len(path)):
                    node = path[i]
                    info = CUENCA_NODES[node]
                    
                    if i < len(path) - 1:
                        next_node = path[i + 1]
                        segment_dist = pathfinder.get_distance(node, next_node)
                        accumulated = sum(pathfinder.get_distance(path[j], path[j+1]) for j in range(i+1))
                    else:
                        segment_dist = 0
                        accumulated = distance
                    
                    route_data.append({
                        'Paso': i + 1,
                        'Lugar': node,
                        'Descripción': info['descripcion'],
                        'Tiempo Visita (min)': info.get('tiempo', 0),
                        'Lat': f"{info['lat']:.4f}",
                        'Lon': f"{info['lon']:.5f}",
                        'Distancia Segmento (km)': f"{segment_dist:.3f}" if segment_dist > 0 else "-",
                        'Distancia Acumulada (km)': f"{accumulated:.3f}"
                    })
                
                df = pd.DataFrame(route_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # Información adicional de tiempo
                col_info1, col_info2 = st.columns(2)
                with col_info1:
                    st.info(f"🚶 **Tiempo de recorrido estimado:** ~{int(distance * 12)} minutos caminando")
                with col_info2:
                    st.info(f"⏱️ **Tiempo total (visitas + recorrido):** ~{tiempo_total + int(distance * 12)} minutos")
                
                # Botón descargar
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Descargar detalles (CSV)", csv, f"ruta_{start}_a_{goal}.csv", "text/csv")
                
                # Mapa
                st.markdown('<div class="section-header">🗺️ Visualización de la Ruta en Mapa</div>', unsafe_allow_html=True)
                
                center_lat = sum(CUENCA_NODES[n]["lat"] for n in path) / len(path)
                center_lon = sum(CUENCA_NODES[n]["lon"] for n in path) / len(path)
                
                m = folium.Map(location=[center_lat, center_lon], zoom_start=14)
                
                # Marcadores
                for node_name, node_data in CUENCA_NODES.items():
                    tiempo = node_data.get('tiempo', 0)
                    
                    if node_name == start:
                        color, icon = "green", "play"
                        popup = f"<b>🟢 INICIO</b><br>{node_name}<br>{node_data['descripcion']}<br>⏱️ Tiempo: {tiempo} min"
                    elif node_name == goal:
                        color, icon = "red", "stop"
                        popup = f"<b>🔴 DESTINO</b><br>{node_name}<br>{node_data['descripcion']}<br>⏱️ Tiempo: {tiempo} min"
                    elif node_name in path:
                        color, icon = "blue", "info-sign"
                        popup = f"<b>🔵 EN RUTA</b><br>{node_name}<br>{node_data['descripcion']}<br>⏱️ Tiempo: {tiempo} min"
                    elif show_all and node_name in pathfinder.explored:
                        color, icon = "lightgray", "record"
                        popup = f"<b>Nodo Explorado</b><br>{node_name}<br>⏱️ Tiempo: {tiempo} min"
                    else:
                        continue
                    
                    folium.Marker(
                        [node_data["lat"], node_data["lon"]],
                        popup=folium.Popup(popup, max_width=300),
                        tooltip=f"{node_name} ({tiempo} min)",
                        icon=folium.Icon(color=color, icon=icon, prefix='glyphicon')
                    ).add_to(m)
                
                # Línea de ruta
                coords = [[CUENCA_NODES[n]["lat"], CUENCA_NODES[n]["lon"]] for n in path]
                folium.PolyLine(coords, color="#1e88e5", weight=6, opacity=0.8, 
                               popup=f"Ruta Óptima: {distance:.2f} km").add_to(m)
                
                # Números en los puntos
                for i, node in enumerate(path, 1):
                    folium.Marker(
                        [CUENCA_NODES[node]["lat"], CUENCA_NODES[node]["lon"]],
                        icon=folium.DivIcon(html=f'''
                            <div style="background: white; border: 2px solid #1e88e5; border-radius: 50%; 
                            width: 28px; height: 28px; display: flex; align-items: center; 
                            justify-content: center; font-weight: bold; font-size: 13px; color: #1e88e5;">{i}</div>
                        ''')
                    ).add_to(m)
                
                folium_static(m, width=1000, height=600)
                
                # Resumen final
                st.markdown("---")
                st.markdown("### 📊 Resumen del Recorrido")
                
                summary_col1, summary_col2, summary_col3 = st.columns(3)
                with summary_col1:
                    st.metric("🎯 Puntos en la ruta", len(path))
                with summary_col2:
                    st.metric("📍 Paradas intermedias", len(path) - 2 if len(path) > 2 else 0)
                with summary_col3:
                    st.metric("🚶 Velocidad estimada", "5 km/h")
    
    else:
        # Estado inicial
        st.markdown('<div class="info-box">👆 <strong>Selecciona un punto de inicio y destino</strong>, luego haz clic en <strong>"Buscar Ruta Óptima"</strong></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="section-header">🗺️ Mapa de Cuenca - Puntos de Interés Turístico</div>', unsafe_allow_html=True)
        
        center_lat = sum(n["lat"] for n in CUENCA_NODES.values()) / len(CUENCA_NODES)
        center_lon = sum(n["lon"] for n in CUENCA_NODES.values()) / len(CUENCA_NODES)
        
        m = folium.Map(location=[center_lat, center_lon], zoom_start=13)
        
        for node_name, node_data in CUENCA_NODES.items():
            tiempo = node_data.get('tiempo', 0)
            folium.Marker(
                [node_data["lat"], node_data["lon"]],
                popup=f"<b>{node_name}</b><br>{node_data['descripcion']}<br>⏱️ Tiempo estimado: {tiempo} min",
                tooltip=f"{node_name} ({tiempo} min)",
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(m)
        
        folium_static(m, width=1000, height=600)
        
        # Tabla de todos los puntos
        st.markdown('<div class="section-header">📍 Todos los Puntos de Interés</div>', unsafe_allow_html=True)
        
        all_points = []
        for node_name in sorted(CUENCA_NODES.keys()):
            node_data = CUENCA_NODES[node_name]
            all_points.append({
                'Lugar': node_name,
                'Descripción': node_data['descripcion'],
                'Tiempo Visita (min)': node_data.get('tiempo', 0),
                'Latitud': f"{node_data['lat']:.4f}",
                'Longitud': f"{node_data['lon']:.5f}"
            })
        
        df_all = pd.DataFrame(all_points)
        st.dataframe(df_all, use_container_width=True, hide_index=True)