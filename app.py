import streamlit as st
import tools.data_engine as db
import time
import os
from datetime import datetime

# --- CONFIGURACIÓN E INICIALIZACIÓN ---
st.set_page_config(page_title="Seba OS - Life XP", layout="wide", page_icon="🚀")

# Inicializar Estados
if 'selected_area' not in st.session_state:
    st.session_state['selected_area'] = None
if 'completing_task' not in st.session_state:
    st.session_state['completing_task'] = None
if 'editing_task' not in st.session_state:
    st.session_state['editing_task'] = None
if 'view_mode' not in st.session_state:
    st.session_state['view_mode'] = 'dashboard' 

# --- ESTILOS CSS "CYBER-GLOW" ---
st.markdown("""
    <style>
    /* Fondo General */
    .stApp { background-color: #0b0c10; }
    
    /* Imagen de Perfil - Efecto Halo */
    .profile-pic img {
        border-radius: 50%;
        border: 2px solid #66fcf1;
        box-shadow: 0 0 20px rgba(102, 252, 241, 0.4);
        object-fit: cover;
    }

    /* BOTONES PRINCIPALES (TARJETAS) */
    div.element-container button[kind="secondary"] {
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        background: linear-gradient(145deg, #1f2833, #151b22);
        color: #c5c6c7;
        height: auto;
        padding: 35px 20px;
        font-size: 26px;
        font-weight: 700;
        letter-spacing: 1px;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        width: 100%;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    /* EFECTO GLOW AL PASAR EL MOUSE */
    div.element-container button[kind="secondary"]:hover {
        transform: translateY(-5px) scale(1.02);
        border-color: #45a29e;
        color: #66fcf1;
        background-color: #1f2833;
        box-shadow: 0 0 25px rgba(102, 252, 241, 0.6), inset 0 0 10px rgba(102, 252, 241, 0.1);
    }
    
    /* Barra de Energía Global */
    .energy-bar-container {
        background-color: #1f2833;
        border-radius: 12px;
        padding: 4px;
        margin-top: 10px;
        box-shadow: inset 0 2px 5px rgba(0,0,0,0.5);
    }
    .energy-fill {
        height: 12px;
        border-radius: 8px;
        background: linear-gradient(90deg, #ff0055, #ffcc00, #66fcf1);
        box-shadow: 0 0 15px rgba(102, 252, 241, 0.5);
        transition: width 0.5s ease-in-out;
    }

    /* Títulos y Subtítulos */
    h1, h2 { font-family: 'Segoe UI', sans-serif; text-shadow: 0 0 10px rgba(255,255,255,0.1); }
    .subtitle { color: #888; font-size: 14px; margin-top: -15px; margin-bottom: 20px; font-family: monospace;}
    
    /* Ajuste de Barras de Progreso Streamlit */
    .stProgress > div > div > div > div {
        background-color: #45a29e;
    }
    </style>
""", unsafe_allow_html=True)

# --- CARGA DE DATOS ---
user = db.get_user_profile()
current_xp, max_xp = db.calculate_xp()
areas = db.get_areas()

# --- HEADER: PERFIL + HUD ---
col_profile, col_stats = st.columns([1, 6])

with col_profile:
    st.markdown('<div class="profile-pic">', unsafe_allow_html=True)
    if os.path.exists("avatar.png"):
        st.image("avatar.png", width=110)
    elif os.path.exists("avatar.jpg"):
        st.image("avatar.jpg", width=110)
    else:
        st.image("https://api.dicebear.com/9.x/bottts/svg?seed=SebaOS", width=110) 
    st.markdown('</div>', unsafe_allow_html=True)

with col_stats:
    st.title(f"Seba OS v3.0")
    st.markdown(f"<div class='subtitle'>SYSTEM ONLINE | Architect Level {user.get('level', 1)} | {current_xp} XP Total</div>", unsafe_allow_html=True)
    
    # Barra Global
    level_progress = min((current_xp % 500) / 500 * 100, 100)
    st.markdown(f"""
        <div class="energy-bar-container">
            <div class="energy-fill" style="width: {level_progress}%;"></div>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# --- BARRA DE NAVEGACIÓN (Atajos) ---
c1, c2, c3, c4 = st.columns(4)
if c1.button("🏠 MAIN DECK", use_container_width=True):
    st.session_state['view_mode'] = 'dashboard'
    st.session_state['selected_area'] = None
    st.rerun()
if c2.button("🔥 FOCUS WEEK", use_container_width=True):
    st.session_state['view_mode'] = 'focus_week'
    st.rerun()
if c3.button("⚡ QUICK WINS", use_container_width=True):
    st.session_state['view_mode'] = 'quick_wins'
    st.rerun()
if c4.button("📊 DATA LOGS", use_container_width=True):
    st.session_state['view_mode'] = 'stats'
    st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# --- VISTAS PRINCIPALES ---

# 1. DASHBOARD (Tarjetas con Barras de XP)
if st.session_state['view_mode'] == 'dashboard':
    
    if st.session_state['selected_area'] is None:
        
        cols = st.columns(2)
        for i, area in enumerate(areas):
            col = cols[i % 2]
            with col:
                # --- CÁLCULO DE XP POR ÁREA ---
                area_xp_total = 0
                area_xp_earned = 0
                for proj in area['projects']:
                    for task in proj['tasks']:
                        xp_val = task.get('xp', 10)
                        area_xp_total += xp_val
                        if task['status'] == 'complete':
                            area_xp_earned += xp_val
                
                # Evitar división por cero
                if area_xp_total > 0:
                    area_progress = area_xp_earned / area_xp_total
                else:
                    area_progress = 0.0
                
                # --- VISUALIZACIÓN ---
                # Etiqueta de progreso pequeña arriba
                st.markdown(f"<div style='text-align:right; font-size:12px; color:#66fcf1; margin-bottom:2px;'>{int(area_progress*100)}% Charged</div>", unsafe_allow_html=True)
                # Barra de progreso nativa
                st.progress(area_progress)
                
                # Botón "Glow"
                if st.button(f"{area['name']}", key=f"btn_{area['id']}", use_container_width=True):
                    st.session_state['selected_area'] = area['id']
                    st.rerun()
                
                st.markdown("<br>", unsafe_allow_html=True)
        
        # Historial Global
        st.markdown("---")
        with st.expander("📜 Global Quest Log (Reciente)", expanded=False):
            completed = db.get_global_completed_tasks()
            if not completed:
                st.info("Sin registros.")
            for item in completed[:10]:
                c1, c2 = st.columns([0.85, 0.15])
                with c1:
                    st.markdown(f"✅ **{item['task']['title']}**")
                    st.caption(f"📂 {item['area_name']} > {item['project_name']}")
                with c2:
                    if st.button("↺", key=f"gr_{item['task']['id']}"):
                        db.update_task_status(item['area_id'], item['project_index'], item['task']['id'], 'process')
                        st.rerun()
                st.divider()

    else:
        # --- VISTA DETALLE DE ÁREA ---
        area_id = st.session_state['selected_area']
        area = next((a for a in areas if a['id'] == area_id), None)
        
        if area:
            # Header Área
            cb, ct = st.columns([0.15, 0.85])
            with cb:
                if st.button("⬅️ Atrás"):
                    st.session_state['selected_area'] = None
                    st.rerun()
            with ct:
                st.markdown(f"<h2 style='color:#66fcf1; border-bottom:1px solid #333; padding-bottom:10px;'>{area['name']}</h2>", unsafe_allow_html=True)
            
            # Proyectos
            for p_idx, project in enumerate(area['projects']):
                active_c = len([t for t in project['tasks'] if t['status'] != 'complete'])
                
                with st.expander(f"📁 {project['name']}  —  {active_c} misiones activas", expanded=False):
                    
                    active_tasks = [t for t in project['tasks'] if t['status'] != 'complete']
                    if not active_tasks:
                        st.caption("Nada pendiente. ¡Buen trabajo!")
                    
                    for task in active_tasks:
                        # Tarea Row
                        c_info, c_act1, c_act2 = st.columns([0.7, 0.15, 0.15])
                        with c_info:
                            st.write(f"**{task['title']}** <span style='color:#4CAF50; font-size:12px;'>+{task.get('xp', 10)} XP</span>", unsafe_allow_html=True)
                            if task.get('due_date'):
                                st.caption(f"📅 {task['due_date']}")
                        
                        with c_act1:
                            if st.button("✏️", key=f"e_{task['id']}"):
                                st.session_state['editing_task'] = task['id']
                                st.rerun()
                        with c_act2:
                            if st.button("✅", key=f"c_{task['id']}"):
                                st.session_state['completing_task'] = task['id']
                                st.rerun()
                        
                        # Acciones (Completar / Editar)
                        if st.session_state['completing_task'] == task['id']:
                            st.success("Misión Cumplida. Registra el resultado:")
                            with st.form(key=f"fc_{task['id']}"):
                                out = st.text_area("Output / Notas")
                                if st.form_submit_button("Reclamar Recompensa"):
                                    db.update_task_status(area['id'], p_idx, task['id'], 'complete', out)
                                    st.session_state['completing_task'] = None
                                    st.balloons()
                                    time.sleep(1)
                                    st.rerun()
                        
                        if st.session_state['editing_task'] == task['id']:
                            with st.form(key=f"fe_{task['id']}"):
                                nt = st.text_input("Título", task['title'])
                                nx = st.number_input("XP", value=task.get('xp', 10))
                                nd = st.text_input("Fecha", value=task.get('due_date', ''))
                                nc = st.text_area("Notas", value=task.get('comment', ''))
                                c_s, c_d = st.columns(2)
                                with c_s:
                                    if st.form_submit_button("Guardar"):
                                        db.edit_task(area['id'], p_idx, task['id'], nt, nx, nd, nc)
                                        st.session_state['editing_task'] = None
                                        st.rerun()
                                with c_d:
                                    if st.form_submit_button("Eliminar"):
                                        db.delete_task(area['id'], p_idx, task['id'])
                                        st.session_state['editing_task'] = None
                                        st.rerun()
                        st.markdown("---")
                    
                    # Añadir Tarea
                    with st.form(key=f"add_{project['name']}"):
                        ca1, ca2, ca3 = st.columns([3,1,1])
                        with ca1: t_new = st.text_input("Nueva Misión")
                        with ca2: x_new = st.number_input("XP", 10, 100, 10)
                        with ca3: 
                            if st.form_submit_button("➕"):
                                if t_new:
                                    db.add_task(area['id'], p_idx, t_new, xp=x_new)
                                    st.rerun()

            st.markdown("---")
            with st.expander("➕ Iniciar Nuevo Proyecto"):
                with st.form(key=f"np_{area['id']}"):
                    n_proj = st.text_input("Nombre del Proyecto")
                    if st.form_submit_button("Crear"):
                        db.add_project(area['id'], n_proj)
                        st.rerun()

# 2. VISTAS FILTRADAS
elif st.session_state['view_mode'] in ['focus_week', 'quick_wins']:
    title = "🔥 Focus Week" if st.session_state['view_mode'] == 'focus_week' else "⚡ Quick Wins"
    st.title(title)
    if st.button("⬅️ Volver"):
        st.session_state['view_mode'] = 'dashboard'
        st.rerun()
    
    tasks = db.get_filtered_tasks(st.session_state['view_mode'])
    if not tasks: st.info("Nada por aquí.")
    for t in tasks:
        with st.container():
            st.markdown(f"**{t['task']['title']}** ({t['task']['xp']} XP)")
            st.caption(f"📂 {t['project_name']}")
            st.markdown("---")

# 3. INSIGHTS
elif st.session_state['view_mode'] == 'stats':
    st.title("📊 Data Logs")
    if st.button("⬅️ Volver"):
        st.session_state['view_mode'] = 'dashboard'
        st.rerun()
    
    completed = db.get_global_completed_tasks()
    k1, k2, k3 = st.columns(3)
    k1.metric("Completadas", len(completed))
    k2.metric("XP Total", current_xp)
    k3.metric("Nivel", user.get('level', 1))
    
    if completed:
        st.table([{"Fecha": t['completed_at'][:10], "Misión": t['task']['title'], "Area": t['area_name'], "XP": t['task'].get('xp', 10)} for t in completed])
    else:
        st.write("Aún no hay datos.")
