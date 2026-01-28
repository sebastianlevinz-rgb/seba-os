# Findings

## Research Log
- **Knowledge Item**: Reviewed `Shabtai XP Dashboard` (data_model.md). The existing model was Area/Project/Task. New requirement adds `XP Value`.
- **Tech Stack**: User selected **Streamlit** for speed. It has native support for `st.dataframe` and data caching, which fits the "Self-Healing" rule.

## Constraints
- **Offline Resilience**: Must cache data locally to handle API flickers.
- **Mobile Usage**: User wants to update from phone via Google Sheets app. This means our app must handle *read* syncs efficiently, and potentially *write* syncs if we add buttons.
- **Complexity**: Keep it "Minimal Actionable Tasks".
