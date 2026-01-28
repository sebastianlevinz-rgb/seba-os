# SOP: Link (Connectivity)

**Goal**: Manage Data Consistency using Local JSON (Primary for v1).

## 1. Source of Truth
- **File**: `database.json` (Root directory).
- **Format**: JSON Schema defined in `gemini.md`.

## 2. Protocol
1.  **Init**: Check if `database.json` exists. If not, create with Seed Data.
2.  **Read**: Load JSON into Pandas DataFrame.
3.  **Write**: Save DataFrame back to JSON.
4.  **Backup**: (Optional) Copy to `.tmp/backup_database.json` before write.

## 3. Error Handling
- **JSONDecodeError**: If file is corrupted, load `database.json.bak` (if exists) or re-init empty schema.
