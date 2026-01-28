import json
import pymongo
import os

# Tu conexión directa a la nube
MONGO_URI = "mongodb+srv://sebastianlevinz_db_user:d1lopjAMe9CaURCj@cluster0.wkhuwqg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

def migrate():
    # 1. Leer datos locales
    local_path = 'database.json'
    if not os.path.exists(local_path):
        print("❌ ERROR: No encuentro el archivo 'tools/database.json'")
        return

    with open(local_path, 'r', encoding='utf-8') as f:
        local_data = json.load(f)
        # Aseguramos que tenga el ID correcto para la nube
        local_data["_id"] = "main_data"

    # 2. Conectar a la nube
    print("⏳ Conectando a MongoDB Atlas...")
    client = pymongo.MongoClient(MONGO_URI)
    db = client["seba_os_db"]
    collection = db["user_data"]

    # 3. Subir datos
    print("🚀 Subiendo tus datos...")
    collection.replace_one({"_id": "main_data"}, local_data, upsert=True)
    
    print("\n✅ ¡LISTO! Tus datos han sido clonados a la nube.")
    print("👉 Ahora ve a tu Web App (la url de Streamlit) y recarga la página (F5).")

if __name__ == "__main__":
    migrate()