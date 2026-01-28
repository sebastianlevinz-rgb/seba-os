import json
import os

DB_PATH = 'database.json'

def update_zevah():
    if not os.path.exists(DB_PATH):
        print("❌ Database not found")
        return

    with open(DB_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    new_zevah_data = {
      "id": "zevah",
      "name": "Zevah (Music Artist)",
      "color": "#9333EA",
      "projects": [
        {
          "name": "Identity & Rebranding",
          "tasks": [
            {"id": "z1_1", "title": "Fix Spotify Identity (Zev vs Zevah)", "status": "process", "xp": 50, "note": "Contact Distributor/Guille to separate profiles."},
            {"id": "z1_2", "title": "Update Bio & Photos", "status": "todo", "xp": 20, "note": "Highlight: Solo project, Israel based, Spinetta/Cerati influence."},
            {"id": "z1_3", "title": "Social Media Reset", "status": "todo", "xp": 30, "note": "Archive old posts, apply new visual identity (Logo/Palette)."}
          ]
        },
        {
          "name": "Relaunch: EP 'Seba' (Amarillo 2016)",
          "tasks": [
            {"id": "z2_1", "title": "Restore Cover Art", "status": "todo", "xp": 30, "note": "Replace blurry version with high-res original 'La Chola' design."},
            {"id": "z2_2", "title": "Fix Metadata: Gativideo", "status": "todo", "xp": 20, "note": "Add 'Livelli y Los Saravia' as Featured Artist."},
            {"id": "z2_3", "title": "Canvas: Amarillo", "status": "todo", "xp": 20, "note": "Design new AI/Loop visual."},
            {"id": "z2_4", "title": "Canvas: Gativideo", "status": "todo", "xp": 20, "note": "Edit using video cuts from original footage."},
            {"id": "z2_5", "title": "Canvas: Ver Real", "status": "todo", "xp": 20, "note": "Recycle 'Pablito Biólogo' video (cactus flower opening)."},
            {"id": "z2_6", "title": "Canvas: Palermo", "status": "todo", "xp": 20, "note": "Edit using footage of Feli and Mateo."},
            {"id": "z2_7", "title": "Canvas: Aprender", "status": "todo", "xp": 20, "note": "Check archive for images/footage from Uruguay."}
          ]
        },
        {
          "name": "Relaunch: EP 'Tres Líneas de Subte'",
          "tasks": [
            {"id": "z3_1", "title": "Canvas: Minimalist Redhead", "status": "todo", "xp": 20, "note": "Style: Lo-Fi/Anime vibes."},
            {"id": "z3_2", "title": "Canvas: Montana", "status": "todo", "xp": 20, "note": "Visuals reflecting the 'mountain/Seibos' theme."},
            {"id": "z3_3", "title": "Canvas: Manantial", "status": "todo", "xp": 20, "note": "Water-themed visuals/ambient vibe."},
            {"id": "z3_4", "title": "Storytelling Content", "status": "todo", "xp": 30, "note": "Create posts about rehearsals at Manusa's house with Bicha & Mecha."}
          ]
        },
        {
          "name": "Launch: Single 'Dinosaurio'",
          "tasks": [
            {"id": "z4_1", "title": "Distributor Upload", "status": "todo", "xp": 50, "note": "Target: July 21 (Upload deadline June 21)."},
            {"id": "z4_2", "title": "Generate Cover Art", "status": "process", "xp": 30, "note": "Use Midjourney/AI. Theme: Nostalgic/Retro."},
            {"id": "z4_3", "title": "Edit Backstage Trailer", "status": "todo", "xp": 30, "note": "Compile footage from the recording session (Viet)."},
            {"id": "z4_4", "title": "Create Main Visualizer", "status": "todo", "xp": 40, "note": "Full track video loop."},
            {"id": "z4_5", "title": "Record Live Session", "status": "hold", "xp": 50, "note": "Location: Balcony or iconic spot in Israel. Acoustic setup."}
          ]
        },
        {
          "name": "Launch: Single 'The Face'",
          "tasks": [
            {"id": "z5_1", "title": "Confirm Title", "status": "todo", "xp": 10, "note": "Decide: 'The Face' vs 'Instalaciones Térmicas'."},
            {"id": "z5_2", "title": "Generate Cover Art", "status": "todo", "xp": 30, "note": "Consistent style with Dinosaurio."},
            {"id": "z5_3", "title": "Create Visualizer", "status": "todo", "xp": 30, "note": "Concept: Thermal/Heatmap aesthetics?"}
          ]
        },
        {
          "name": "Project Abbey Road (The Holy Grail)",
          "tasks": [
            {"id": "z6_1", "title": "Edit Video: Track 1", "status": "todo", "xp": 50, "note": "Raw footage from Abbey Road 2018 (Feli Colina session)."},
            {"id": "z6_2", "title": "Edit Video: Track 2", "status": "todo", "xp": 50, "note": "Raw footage available. Needs assembly."},
            {"id": "z6_3", "title": "Design EP Artwork", "status": "todo", "xp": 40, "note": "High-end aesthetic. Commemorative style."},
            {"id": "z6_4", "title": "Unlock Milestone", "status": "hold", "xp": 100, "note": "LOCKED until Zevah reaches 1,000 Monthly Listeners on Spotify."}
          ]
        }
      ]
    }

    updated = False
    if 'areas' in data:
        for i, area in enumerate(data['areas']):
            if area['id'] == 'zevah':
                data['areas'][i] = new_zevah_data
                updated = True
                print("✅ Found and updated 'zevah' area.")
                break
    
    if not updated:
        # Append if not found? Or warn?
        # Assuming it exists based on context.
        print("⚠️ 'zevah' area not found. Appending...")
        if 'areas' not in data: data['areas'] = []
        data['areas'].append(new_zevah_data)

    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print("✅ Database saved successfully.")

if __name__ == "__main__":
    update_zevah()
