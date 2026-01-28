# gemini.md - Project Constitution

## 1. Data Schemas

### Core Entity: MAT (Minimal Actionable Task)
The application operates on a flat list of tasks. The "Source of Truth" (Google Sheet) and internal application state must adhere to this shape.

**JSON Representation (Payload):**
```json
{
  "tasks": [
    {
      "id": "string (uuid)",
      "area": "string (Health | AI | Zevah)",
      "project": "string",
      "description": "string (The MAT content)",
      "status": "string (Todo | Process | Hold | Complete)",
      "xp_value": "integer",
      "last_updated": "string (ISO 8601 Timestamp)"
    }
  ]
}
```

**Google Sheet Columns:**
1. `ID` (Hidden/System)
2. `Area`
3. `Project`
4. `Task` (Description)
5. `Status`
6. `XP Value`
7. `Last Updated`

## 2. Behavioral Rules

- **Gamification Logic**: 
  - `Total XP` = Sum of `xp_value` for all tasks where `status` == "Complete".
  - Progress Bars per Area = (`Current XP` / `Target XP`) * 100. (Target XP defaults to Total XP of all tasks in that Area, or a fixed milestone).
- **Visual Feedback**: 
  - Status changes triggers immediate UI reflecting.
  - Progress bars animate on update.
- **Fail-Safe / Self-Healing**:
  - If Google Sheets API fails (`5xx` or Timeout), the system MUST load from a local `backup_data.json` and display a "Offline Mode" warning.
  - No app crashes allowed on API failures.
- **Simplicity**:
  - UI must focus on *doing*. Minimize inputs. Single-click status toggles.

## 3. Architectural Invariants
- **Data-First Rule**: Coding only begins once "Payload" shaped is confirmed.
- **3-Layer Architecture**: Layer 1 (SOPs), Layer 2 (Navigation), Layer 3 (Tools).
- **Self-Healing**: Analyze -> Patch -> Test -> Update Architecture.

## 4. Design System (Glaido)
- **Primary**: Lime Green `#BFF549`
- **Base**: Black `#000000`, White `#ffffff`
- **Font**: Inter / Inter Display

## 5. Maintenance Log
- [Init] Project structure created.
- [Phase 1] Data Schema defined. Streamlit selected for Frontend.
- [Phase 1.5] Design Guidelines ingested (Glaido).
- [Phase 4] System Deployed locally (localhost:8501).
- [Phase 4.5] "Interactive Upgrade": Refactored `app.py` and `data_engine.py` to support JSON Hierarchy, Expanders, and full CRUD (Add/Delete/Complete).
- [Phase 4.6] "Dashboard 2.0": Injected "Travel Affiliate Blog". Implemented Visual Gamification (Badges, Dynamic Bars) and Focus Filters.
- [Phase 4.7] "Full Edit Control": Added `edit_task` logic. Implemented in-line Update Forms for Title, XP, and Due Dates.
- [Phase 4.8] "Outputs & Links": Added `comment` field to schema. Tasks can now store notes/links, which render as Info blocks.
- [Phase 4.9] "Quest Log": Implemented 2-Step Completion Flow (Output Capture) and a separate History view for completed tasks.
- [Phase 4.9] "Quest Log": Implemented 2-Step Completion Flow (Output Capture) and a separate History view for completed tasks.
- [Phase 5.0] [REVERTED] Voice Command Module.
- [Phase 6.0] "UI Cleanup": Set default view to Collapsed (Compact).
- [Phase 6.5] "Project Creator": Added capability to create new projects directly from the UI. Corrected Zevah naming.
- [Phase 7.0] "Master-Detail UI": Refactored navigation. Home Screen now shows Pillar Cards. Clicking an area drills down into specific projects.
- [Phase 9.0] "Clickable Cards": Implemented High-Fidelity UI styling. Areas are now large, interactive cards (Primary Buttons) with hover effects.
- [Phase 9.5] "Integrity Fix": Added Quest Log/Restore section to Area View. Verified unique keys for all interactive elements.
- [Phase 10.0] "Global Hierarchy": Updated Global Quest Log to show "Area > Project" structure and enabled dashboard-wide restoration.
- [Phase 11.0] "Seba OS v2.0": Implemented 'Aero Glass' UI overhaul. Added Global Navigation, Focus Week/Quick Wins views, and Insights Dashboard. Live on Port 8502.
- [Phase 11.5] "Minimalist Refinement": Cleaned up Dashboard cards (Card-only, no progress bars). Added local avatar support.
- [Phase 12.0] "Self-Diagnostic": Created `system_check.py`. Automated integrity check passed (CRUD + State Logic).
- [Phase 13.0] "Seba OS v3.0": Applied "Cyber-Glow" Theme. Restored per-area XP progress bars with visual percentage indicators.
- [Phase 14.0] "Cloud Ready": Implemented Hybrid Storage (Local JSON + MongoDB). Added `requirements.txt` for deployment.
- [Phase 14.5] "Cloud Sync": Executed `upload_data.py`. Local database successfully replicated to MongoDB Atlas (Cluster0).
- [Phase 15.0] "Turbo Mode": Optimized `data_engine.py` using `st.cache_resource` for persistent MongoDB connections.

