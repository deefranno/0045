## 2025-05-22 - [Celebratory UX Gating]
**Learning:** For task-oriented apps (like annotation tools), gating celebratory effects like `st.balloons()` behind a completion milestone (100% progress) instead of firing on initial load provides a clear reward signal and avoids distraction.
**Action:** Use session state to track if a milestone has been reached and only trigger animations once per session when the threshold is first crossed.

## 2025-05-22 - [Robust Streamlit Selectboxes]
**Learning:** `st.selectbox` will crash with a `StreamlitAPIException` if `options` is empty.
**Action:** Always provide a fallback (e.g. `["None"]`) and disable the component (`disabled=True`) when no valid selections are possible to ensure app stability and a clear user signal.
