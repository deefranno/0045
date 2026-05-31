## 2025-05-22 - [Completion Gating for Delight]
**Learning:** For task-oriented apps like data annotation tools, firing celebratory effects like 'st.balloons()' on initial load is distracting. Gating them behind a 100% completion milestone via 'st.session_state' provides a clear reward signal and avoids repetition on every app rerun.
**Action:** Always gate celebratory effects behind a logical completion state and use session state to ensure they fire exactly once per milestone reached.

## 2025-05-22 - [Python 3.12 & Streamlit Compatibility]
**Learning:** Python 3.12 requires Streamlit 1.57.0+ to ensure a pre-compiled 'Pillow' wheel is available, avoiding build failures due to missing local 'jpeg' headers for source compilation.
**Action:** When working in Python 3.12 environments, prefer 'streamlit>=1.57.0' in requirements.txt.
