# SOP: Streamlit (Frontend)

**Goal**: Build a "Glaido-styled" gamified dashboard using Streamlit.

## 1. Page Config
- **Layout**: Wide mode (`layout="wide"`).
- **Theme**: Dark Mode forced via `config.toml` (managed by user settings usually, but we will style components to match Black/Lime).

## 2. Components
### A. Progress Bars (The "Pulse")
- Use `st.progress` for standard bars.
- calculate `value` = (Completed XP / Target XP).
- **Style**: Standard Streamlit bars are hard to color without CSS injection. We will use **Custom CSS** to force Lime Green (`#BFF549`).

### B. MAT List (The "Action")
- Use `st.data_editor` for the Task List.
- **Columns**: `Task`, `Project`, `Status`, `XP Value`.
- **Interactivity**: 
  - `Status` should be a Dropdown (`status` column config).
  - Editing `Status` to "Complete" triggers a re-run and XP update.

### C. Metrics (The "Score")
- Use `st.metric` for "Total XP" per Area.
- Label: "HEALTH XP", "AI XP", "ZEVAH XP".

## 3. Custom CSS (Styling)
- Inject `<style>` via `st.markdown(unsafe_allow_html=True)`.
- **Target**: `.stProgress > div > div > div > div` { background-color: #BFF549; }
- **Font**: Import 'Inter' if possible, or use system sans-serif.

## 4. State Management
- `st.session_state['data']`: Holds the current DataFrame.
- `st.session_state['last_updated']`: Timestamp to force refresh.
