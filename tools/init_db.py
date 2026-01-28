import json
import os
import datetime

DB_FILE = "database.json"

def get_timestamp():
    return datetime.datetime.now().isoformat()

SEED_DATA = {
    "tasks": [
        # Health
        {"id": "h1", "area": "Health", "project": "General", "description": "Osempic", "status": "Complete", "xp_value": 50, "last_updated": get_timestamp()},
        {"id": "h2", "area": "Health", "project": "General", "description": "Tennis", "status": "Process", "xp_value": 20, "last_updated": get_timestamp()},
        {"id": "h3", "area": "Health", "project": "General", "description": "Gym or Effort", "status": "Hold", "xp_value": 10, "last_updated": get_timestamp()},
        
        # AI Projects
        {"id": "a1", "area": "AI Projects", "project": "Impulse Tracker", "description": "Delay Gratification App", "status": "Process", "xp_value": 100, "last_updated": get_timestamp()},
        {"id": "a2", "area": "AI Projects", "project": "Dashboard", "description": "Shabtai XP Dashboard", "status": "Process", "xp_value": 100, "last_updated": get_timestamp()},
        {"id": "a3", "area": "AI Projects", "project": "Shabtai Lab", "description": "AI Art + Workflows", "status": "Todo", "xp_value": 50, "last_updated": get_timestamp()},
        
        # Zevah
        {"id": "z1", "area": "Zevah", "project": "Lavado de Cara", "description": "EP 2016", "status": "Hold", "xp_value": 30, "last_updated": get_timestamp()},
        {"id": "z2", "area": "Zevah", "project": "Lavado de Cara", "description": "3 Lineas de Subte", "status": "Hold", "xp_value": 30, "last_updated": get_timestamp()},
        {"id": "z3", "area": "Zevah", "project": "Lanzamientos", "description": "EP Dinosaurio", "status": "Todo", "xp_value": 40, "last_updated": get_timestamp()},
    ]
}

def init_db():
    print("--- Local Database Initialization ---")
    if os.path.exists(DB_FILE):
        print(f"ℹ️  '{DB_FILE}' already exists. Skipping init.")
        return True
    
    try:
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(SEED_DATA, f, indent=2)
        print(f"✅ SUCCESS: Created '{DB_FILE}' with seed data.")
        return True
    except Exception as e:
        print(f"❌ ERROR: Failed to create database. {e}")
        return False

if __name__ == "__main__":
    init_db()
