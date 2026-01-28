import json
import os
from datetime import datetime
import streamlit as st
import pymongo

# Configuración
# Corrected path: database.json is at the project root, not inside tools/
DB_LOCAL_PATH = 'database.json'
MONGO_URI = st.secrets.get("MONGO_URI", None)

# --- TURBO MODE: CACHING DE CONEXIÓN ---
@st.cache_resource
def init_connection():
    """Esta función se ejecuta SOLO UNA VEZ y mantiene la conexión viva."""
    if not MONGO_URI:
        return None
    try:
        # tlsAllowInvalidCertificates=True ayuda a veces con redes lentas/corporativas
        return pymongo.MongoClient(MONGO_URI)
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return None

def get_db_collection():
    """Obtiene la colección usando la conexión en caché"""
    client = init_connection()
    if client:
        return client["seba_os_db"]["user_data"]
    return None

# --- LÓGICA DE CARGA ---

def load_db():
    collection = get_db_collection()
    
    # MODO NUBE (MongoDB)
    if collection is not None:
        try:
            data = collection.find_one({"_id": "main_data"})
            if not data:
                # Inicializar si vacío
                initial_data = {
                    "_id": "main_data", 
                    "user_profile": {"name": "Seba", "level": 1, "total_xp": 0}, 
                    "areas": []
                }
                collection.insert_one(initial_data)
                return initial_data
            return data
        except Exception as e:
            # Fallback silencioso si falla la red momentáneamente
            st.warning(f"Usando modo offline temporalmente... ({e})")
    
    # MODO LOCAL (Fallback)
    if not os.path.exists(DB_LOCAL_PATH):
        return {"user_profile": {"name": "Seba", "level": 1, "total_xp": 0}, "areas": []}
    with open(DB_LOCAL_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_db(data):
    collection = get_db_collection()
    
    # MODO NUBE
    if collection is not None:
        try:
            collection.replace_one({"_id": "main_data"}, data, upsert=True)
            return
        except:
            pass # Si falla, intentará guardar local

    # MODO LOCAL
    with open(DB_LOCAL_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# --- FUNCIONES DE LÓGICA (CRUD) ---

def get_user_profile():
    return load_db().get("user_profile", {})

def get_areas():
    return load_db().get("areas", [])

def calculate_xp():
    data = load_db()
    total_earned = 0
    total_possible = 0
    for area in data['areas']:
        for project in area['projects']:
            for task in project['tasks']:
                xp = task.get('xp', 10)
                total_possible += xp
                if task['status'] == 'complete':
                    total_earned += xp
    
    # Solo guardamos si hubo cambios reales en XP para ahorrar escrituras
    if data['user_profile'].get('total_xp') != total_earned:
        data['user_profile']['total_xp'] = total_earned
        data['user_profile']['level'] = 1 + (total_earned // 500)
        save_db(data)
        
    return total_earned, total_possible

def update_task_status(area_id, project_index, task_id, new_status, output_text=None):
    data = load_db()
    for area in data['areas']:
        if area['id'] == area_id:
            project = area['projects'][project_index]
            for task in project['tasks']:
                if task['id'] == task_id:
                    task['status'] = new_status
                    if new_status == 'complete':
                        task['completed_at'] = datetime.now().isoformat()
                        if output_text: task['output'] = output_text
                    save_db(data)
                    return True
    return False

def add_project(area_id, project_name):
    data = load_db()
    for area in data['areas']:
        if area['id'] == area_id:
            area['projects'].append({"name": project_name, "tasks": []})
            save_db(data)
            return True
    return False

def add_task(area_id, project_index, title, xp=10, due_date=None):
    data = load_db()
    new_task = {
        "id": f"t_{int(datetime.now().timestamp())}", 
        "title": title, "status": "todo", "xp": xp, "due_date": due_date
    }
    for area in data['areas']:
        if area['id'] == area_id:
            area['projects'][project_index]['tasks'].append(new_task)
            save_db(data)
            return True
    return False

def edit_task(area_id, project_index, task_id, new_title, new_xp, new_date, new_comment):
    data = load_db()
    for area in data['areas']:
        if area['id'] == area_id:
            for task in area['projects'][project_index]['tasks']:
                if task['id'] == task_id:
                    task.update({'title': new_title, 'xp': new_xp, 'due_date': new_date, 'comment': new_comment})
                    save_db(data)
                    return True
    return False

def delete_task(area_id, project_index, task_id):
    data = load_db()
    for area in data['areas']:
        if area['id'] == area_id:
            proj = area['projects'][project_index]
            proj['tasks'] = [t for t in proj['tasks'] if t['id'] != task_id]
            save_db(data)
            return True
    return False

def get_global_completed_tasks():
    data = load_db()
    completed = []
    for area in data['areas']:
        for p_idx, proj in enumerate(area['projects']):
            for task in proj['tasks']:
                if task.get('status') == 'complete':
                    completed.append({
                        'task': task, 'area_id': area['id'], 'area_name': area['name'],
                        'project_index': p_idx, 'project_name': proj['name'],
                        'completed_at': task.get('completed_at', '')
                    })
    completed.sort(key=lambda x: x['completed_at'], reverse=True)
    return completed

def get_filtered_tasks(filter_mode):
    data = load_db()
    tasks_list = []
    today = datetime.now().date()
    for area in data['areas']:
        for p_idx, proj in enumerate(area['projects']):
            for task in proj['tasks']:
                if task.get('status') != 'complete':
                    include = False
                    if filter_mode == 'all_tasks': include = True
                    elif filter_mode == 'quick_wins' and task.get('xp', 0) <= 20: include = True
                    elif filter_mode == 'focus_week':
                        if task.get('due_date'):
                            try:
                                delta = (datetime.strptime(task['due_date'], "%Y-%m-%d").date() - today).days
                                if 0 <= delta <= 7: include = True
                            except: pass
                    if include:
                        tasks_list.append({'task': task, 'area_id': area['id'], 'project_name': proj['name']})
    return tasks_list
