# SOP: Data (Logic)

**Goal**: standardized CRUD for `database.json`.

## 1. Load Data
- **Input**: None (reads `database.json`).
- **Output**: Pandas DataFrame.
- **Logic**: 
    1. Read JSON. 
    2. Convert to DataFrame. 
    3. Ensure `xp_value` is numeric.

## 2. Save Data
- **Input**: Pandas DataFrame.
- **Output**: Success Boolean.
- **Logic**:
    1. Convert DataFrame to `records` dict.
    2. Wrap in `{"tasks": [...]}` envelope.
    3. Write to `database.json`.

## 3. Calculate XP
- **Input**: DataFrame.
- **Output**: Dict `{ "Health": 120, "AI Projects": 50 ... }`.
- **Logic**:
    - Filter `Status == "Complete"`.
    - Group By `Area`.
    - Sum `xp_value`.
