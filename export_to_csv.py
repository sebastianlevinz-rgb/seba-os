import json
import csv
import os
from datetime import datetime

# Rutas de archivos (Corrected logic for root execution)
INPUT_DB = 'database.json'
OUTPUT_CSV = 'export_seba_os.csv'

def export_to_csv():
    # 1. Cargar tu base de datos actual
    if not os.path.exists(INPUT_DB):
        print(f"❌ No encontré {INPUT_DB}")
        return

    with open(INPUT_DB, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 2. Preparar la lista "plana"
    # Columnas: Tarea, Estado, XP, Área, Proyecto, Notas, Fecha Completado
    rows = []
    
    # Check if user_profile exists (safe access)
    user_name = data.get('user_profile', {}).get('name', 'User')
    print(f"🔄 Procesando datos de {user_name}...")

    for area in data.get('areas', []):
        area_name = area.get('name', 'Unknown')
        
        for project in area.get('projects', []):
            proj_name = project.get('name', 'Unknown')
            
            for task in project.get('tasks', []):
                # Mapear estado a términos estándar
                status = "Done" if task.get('status') == 'complete' else "To Do"
                
                # Obtener fecha si existe, o dejar vacío
                date_str = task.get('completed_at', '')
                if not date_str:
                    date_str = task.get('due_date', '')

                row = {
                    'Name': task.get('title', 'Untitled'),
                    'Status': status,
                    'Area': area_name,
                    'Project': proj_name,
                    'XP': task.get('xp', 10),
                    'Notes': task.get('comment', '') or task.get('output', ''),
                    'Date': date_str
                }
                rows.append(row)

    # 3. Escribir el CSV
    headers = ['Name', 'Status', 'Area', 'Project', 'XP', 'Notes', 'Date']
    
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✅ ¡Éxito! Se exportaron {len(rows)} tareas a '{OUTPUT_CSV}'.")
    print("📂 Ahora puedes importar este archivo en Notion, Todoist o Excel.")

if __name__ == "__main__":
    export_to_csv()
