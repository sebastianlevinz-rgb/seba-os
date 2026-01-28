import json
import os
import datetime
import re

DB_FILE = "database.json"

# Replace this string with new payloads as needed
RAW_PAYLOAD = """
{
  "id": "tech_biz",
  "name": "Tech & Startups",
  "color": "#3B82F6",
  "projects": [
    {
      "name": "SaaS: MAI (Music Audience Insights)",
      "tasks": [
        {"id": "t1_1", "title": "Define Micro-MVP Scope", "status": "process", "xp": 50, "note": "Focus: Spotify Only. Input: Artist URL -> Output: Dashboard"},
        {"id": "t1_2", "title": "Implement Daily Snapshot Logic", "status": "todo", "xp": 60, "note": "Workaround for missing API history: Record followers every 24h to build custom graph"},
        {"id": "t1_3", "title": "Select No-Code Stack", "status": "hold", "xp": 30, "note": "Options: Bubble or Antigravity for rapid validation"}
      ]
    },
    {
      "name": "Business: High-Ticket Affiliates",
      "tasks": [
        {"id": "t2_1", "title": "Select Niche: Managed Hosting", "status": "todo", "xp": 40, "note": "Focus: Cloudways, WP Engine, Sucuri (High CPA + Recurring)"},
        {"id": "t2_2", "title": "Content Strategy: Data-Led Benchmarks", "status": "todo", "xp": 50, "note": "Create 'Hard-to-fake' content: Speed tests, Uptime logs, Security checks"},
        {"id": "t2_3", "title": "Build Funnel Assets", "status": "todo", "xp": 40, "note": "Develop 'VS' Comparison pages and ROI Calculators"}
      ]
    },
    {
      "name": "Tool: Telegram Accountability Bot",
      "tasks": [
        {"id": "t3_1", "title": "Develop Python Script", "status": "todo", "xp": 50, "note": "Core features: /addtask command and scheduled checks"},
        {"id": "t3_2", "title": "Implement 'Coach' Persona", "status": "todo", "xp": 30, "note": "Proactive daily messaging: 'Did you complete X? ✅/❌'"},
        {"id": "t3_3", "title": "Deploy to Cloud", "status": "todo", "xp": 20, "note": "Host on Replit or Railway for 24/7 uptime"}
      ]
    },
    {
      "name": "App: Delayed Gratification",
      "tasks": [
        {"id": "t4_1", "title": "Define Core Logic", "status": "process", "xp": 40, "note": "Flow: Panic Button -> Context (Emotion/Action) -> 20m Timer"},
        {"id": "t4_2", "title": "UI/UX Design", "status": "todo", "xp": 30, "note": "Minimalist interface to reduce friction during impulse"}
      ]
    }
  ]
}
"""

def clean_text(text):
    if not isinstance(text, str):
        return ""
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

def map_area(payload_id):
    # Mapping raw IDs to Dashboard Columns
    if payload_id == "zevah": return "Zevah"
    if payload_id == "shabtailab": return "AI Projects"
    if payload_id == "tech_biz": return "AI Projects" # Merging into AI Projects/Tech
    if payload_id == "health": return "Health"
    return "AI Projects" # Fallback

def ingest():
    print("--- B.L.A.S.T. Payload Ingester ---")
    data = json.loads(RAW_PAYLOAD)
    
    target_area = map_area(data["id"])
    print(f"📡 Payload: {data['name']} -> Target Area: {target_area}")
    
    new_tasks = []
    timestamp = datetime.datetime.now().isoformat()
    
    for project in data["projects"]:
        project_name = project["name"]
        for task in project["tasks"]:
            clean_note = clean_text(task.get("note", ""))
            description = clean_text(task["title"])
            
            if clean_note:
                 description = f"{description} ({clean_note})"

            new_task = {
                "id": task["id"],
                "area": target_area,
                "project": project_name,
                "description": description,
                "status": normalize_status(task["status"]),
                "xp_value": int(task["xp"]),
                "last_updated": timestamp
            }
            new_tasks.append(new_task)
            
    # Load & Merge
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            db_data = json.load(f)
            existing_tasks = db_data.get("tasks", [])
    else:
        existing_tasks = []
        
    existing_ids = {t["id"] for t in existing_tasks}
    final_tasks = list(existing_tasks)
    
    count_new = 0
    count_updated = 0
    
    for nt in new_tasks:
        if nt["id"] in existing_ids:
            # Update
            for i, et in enumerate(final_tasks):
                if et["id"] == nt["id"]:
                    final_tasks[i] = nt
                    count_updated += 1
                    break
        else:
            # Append
            final_tasks.append(nt)
            count_new += 1
            
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump({"tasks": final_tasks}, f, indent=2)
        
    print(f"✅ Success. Added: {count_new}, Updated: {count_updated} tasks to '{target_area}'.")

if __name__ == "__main__":
    ingest()
