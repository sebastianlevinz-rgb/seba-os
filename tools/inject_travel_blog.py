import json
import os

DB_PATH = 'database.json'

NEW_PROJECT = {
  "name": "Travel Affiliate Blog (SEO + Viral)",
  "tasks": [
    {"id": "tb1", "title": "Niche Research & Selection", "status": "todo", "xp": 30, "note": "Focus: High-Ticket Tours, Luxury Rail (JR Pass), Jets (Villiers). Source: High-ticket research."},
    {"id": "tb2", "title": "Setup Affiliate Partnerships", "status": "hold", "xp": 40, "note": "Apply to: Skyscanner, Klook, Rail Europe. Role: Deals & Finance."},
    {"id": "tb3", "title": "Deploy Blog Infrastructure", "status": "todo", "xp": 50, "note": "Stack: WordPress or Ghost. Goal: SEO-optimized architecture."},
    {"id": "tb4", "title": "Viral Content Strategy (TikTok/IG)", "status": "process", "xp": 40, "note": "Create influencers visiting cities to drive traffic to blog. Role: Social Media & Content."},
    {"id": "tb5", "title": "Keyword Research: Trails & Tours", "status": "todo", "xp": 30, "note": "Identify high-intent keywords for SEO articles."}
  ]
}

def inject():
    if not os.path.exists(DB_PATH):
        print("❌ Database not found.")
        return

    with open(DB_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Find tech_biz area
    target_area_id = "tech_biz"
    found = False
    
    for area in data.get('areas', []):
        if area.get('id') == target_area_id:
            # Check if project exists
            p_names = [p['name'] for p in area.get('projects', [])]
            if NEW_PROJECT['name'] not in p_names:
                area['projects'].append(NEW_PROJECT)
                print(f"✅ Injected '{NEW_PROJECT['name']}' into {target_area_id}")
                found = True
            else:
                print(f"ℹ️ Project '{NEW_PROJECT['name']}' already exists.")
                found = True
            break
            
    if not found:
        print(f"❌ Area '{target_area_id}' not found.")
        return

    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    inject()
