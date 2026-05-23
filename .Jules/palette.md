## 2025-05-23 - [Streamlit Balloon Gating]
**Learning:** Gating celebratory effects like `st.balloons()` behind a progress milestone (100% completion) provides a meaningful reward signal, whereas firing on initial load is distracting and lacks context. Use `st.session_state` to ensure it only fires once upon reaching the goal.
**Action:** Always gate one-time celebratory animations behind specific user-driven milestones and use session state to manage trigger state.

## 2025-05-23 - [Data Editor State Persistence]
**Learning:** `st.data_editor` without an explicit `key` may lose state or behave inconsistently during reruns in complex apps. Providing a unique `key` ensures reliable state management.
**Action:** Assign a unique `key` to all `st.data_editor` components by default.
