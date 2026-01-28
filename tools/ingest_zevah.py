import json
import os
import datetime
import re
import pandas as pd

DB_FILE = "database.json"

RAW_PAYLOAD = """
{
  "id": "zevah",
  "name": "Zevah (Music Artist)",
  "color": "#9333EA",
  "projects": [
    {
      "name": "Identity & Rebranding",
      "tasks": [
        {"id": "z1_1", "title": "Fix Spotify Identity (Zev vs Zevah)", "status": "process", "xp": 50, "note": "Contact Distributor Support to separate profiles"},
        {"id": "z1_2", "title": "Update Bio (EN/ES)", "status": "todo", "xp": 20, "note": "Focus: Solo project, Israel based, Spinetta/Cerati influence"},
        {"id": "z1_3", "title": "Unify Social Visuals", "status": "todo", "xp": 20, "note": "Match aesthetics across IG, TikTok, Spotify"}
      ]
    },
    {
      "name": "Relaunch: EP 'Seba' (Amarillo 2016)",
      "tasks": [
        {"id": "z2_1", "title": "Fix 'Gativideo' Metadata", "status": "todo", "xp": 30, "note": "Add 'Livelli y Los Saravia' as Featured Artist"},
        {"id": "z2_2", "title": "Restore Original Artwork", "status": "todo", "xp": 30, "note": "Upload high-res 3000x3000px version (La Chola design)"},
        {"id": "z2_3", "title": "Production: Spotify Canvases", "status": "todo", "xp": 40, "note": "Assets: Pablito Biólogo (Ver Real), Feli/Mateo (Palermo), Uruguay footage (Aprender)"},
        {"id": "z2_4", "title": "Spotify Pitch Strategy", "status": "todo", "xp": 20, "note": "Pitch as '2026 Remaster/Relaunch'"}
      ]
    },
    {
      "name": "Relaunch: EP 'Tres Líneas de Subte'",
      "tasks": [
        {"id": "z3_1", "title": "Generate AI Canvases", "status": "process", "xp": 30, "note": "Style: Lo-Fi/Anime vibes"},
        {"id": "z3_2", "title": "Content: Storytelling", "status": "todo", "xp": 20, "note": "Script stories about rehearsals at Manusa's house"}
      ]
    },
    {
      "name": "Launch: Single 'Dinosaurio'",
      "tasks": [
        {"id": "z4_1", "title": "Distributor Upload", "status": "todo", "xp": 50, "note": "DEADLINE: June 21, 2026 (for July 21 Release)"},
        {"id": "z4_2", "title": "Visuals & Artwork", "status": "process", "xp": 30, "note": "Execute using Midjourney/AI workflows"},
        {"id": "z4_3", "title": "Record Live Session", "status": "todo", "xp": 40, "note": "Self-produced. Location: Balcony or iconic spot in Israel"}
      ]
    },
    {
      "name": "Launch: Single 'The Face'",
      "tasks": [
        {"id": "z5_1", "title": "Upload to Distributor", "status": "hold", "xp": 50, "note": "Target Release: August 2026"},
        {"id": "z5_2", "title": "Create Visualizer", "status": "hold", "xp": 30, "note": "Concept: Térmical Inserrations"}
      ]
    },
    {
      "name": "Project Abbey Road",
      "tasks": [
        {"id": "z6_1", "title": "Growth Goal: 1k Listeners", "status": "hold", "xp": 100, "note": "Unlock EP release only after reaching 1,000 monthly listeners"}
      ]
    }
  ]
}
"""

def clean_text(text):
    if not isinstance(text, str):
        return ""
    # Remove [cite_start] and [cite: ...]
    text = re.sub(r'\[cite_start\]', '', text)
    text = re.sub(r'\[cite:.*?\]', '', text)
    return text.strip()

def normalize_status(status):
    status = status.lower()
    if status == "todo": return "Todo"
    if status == "process": return "Process"
    if status == "hold": return "Hold"
    if status == "complete": return "Complete"
    return "Todo"

def ingest():
    print("--- Ingesting Zevah Payload ---")
    
    # 1. Parse JSON (simulated from raw string to avoid file IO issues with citation tags if they were in a file)
    # I already cleaned the string in the variable definition above (removed [cite_start] manually in logic? No, let's process the dictionary directly)
    # Actually the string above is valid JSON except for potential hidden chars. 
    # The Prompt had [cite_start] outside the string quotes sometimes?
    # Let's assume the INPUT `RAW_PAYLOAD` in this script is Clean JSON for valid python syntax.
    # The user request had `[cite_start]{...}`. I have manually removed them in the string literal above 
    # to make it valid python dict or json.
    
    data = json.loads(RAW_PAYLOAD)
    
    new_tasks = []
    timestamp = datetime.datetime.now().isoformat()
    
    area_name = "Zevah" # Mapping "Zevah (Music Artist)" to our short code "Zevah"
    
    for project in data["projects"]:
        project_name = project["name"]
        for task in project["tasks"]:
            clean_note = clean_text(task.get("note", ""))
            description = clean_text(task["title"])
            
            # Combine note if useful, or just store. 
            # For now, sticking to schema: description only.
            # actually lets append note to description for context
            if clean_note:
                 description = f"{description} ({clean_note})"

            new_task = {
                "id": task["id"],
                "area": area_name,
                "project": project_name,
                "description": description,
                "status": normalize_status(task["status"]),
                "xp_value": int(task["xp"]),
                "last_updated": timestamp
            }
            new_tasks.append(new_task)
            
    # 2. Load Existing DB
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            db_data = json.load(f)
            existing_tasks = db_data.get("tasks", [])
    else:
        existing_tasks = []
        
    # 3. Merge (Upsert based on ID)
    # Remove old Zevah placeholder tasks if we want to replace?
    # Let's just keep everything and append unique IDs. 
    # The new IDs are specific (z1_1). existing were z1, z2.
    # To be clean, I will remove the intersection or just append.
    # User likely wants these to BE the Zevah tasks.
    
    existing_ids = {t["id"] for t in existing_tasks}
    final_tasks = list(existing_tasks)
    
    for nt in new_tasks:
        if nt["id"] in existing_ids:
            # Update existing
            for i, et in enumerate(final_tasks):
                if et["id"] == nt["id"]:
                    final_tasks[i] = nt
                    break
        else:
            # Append new
            final_tasks.append(nt)
            
    # 4. Save
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump({"tasks": final_tasks}, f, indent=2)
        
    print(f"✅ Ingested {len(new_tasks)} tasks for {area_name}")

if __name__ == "__main__":
    ingest()
