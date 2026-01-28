import os
import sys
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def check_link():
    """
    Verifies connection to Google Sheets.
    Required ENV: SHABTAI_XP_SHEET_ID
    Required File: service_account.json
    """
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    
    creds_path = "service_account.json"
    sheet_id = os.getenv("SHABTAI_XP_SHEET_ID")
    
    print("--- B.L.A.S.T. Link Verification ---")
    
    # 1. Check Credentials File
    if not os.path.exists(creds_path):
        print(f"❌ FAILED: '{creds_path}' not found.")
        print("   -> Please place your Google Service Account JSON file in the root.")
        return False

    # 2. Check Sheet ID
    if not sheet_id:
        print("❌ FAILED: 'SHABTAI_XP_SHEET_ID' not found in environment.")
        return False

    try:
        # 3. Connect
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
        client = gspread.authorize(creds)
        
        # 4. Handshake
        print(f"📡 Connecting to Sheet ID: {sheet_id}...")
        sheet = client.open_by_key(sheet_id).sheet1
        headers = sheet.row_values(1)
        
        print(f"✅ SUCCESS: Connected! Headers found: {headers}")
        return True

    except Exception as e:
        print(f"❌ ERROR: Connection failed. \n   {e}")
        return False

if __name__ == "__main__":
    success = check_link()
    if not success:
        sys.exit(1)
