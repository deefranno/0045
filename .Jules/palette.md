## 2024-04-29 - Enhancing Semantic Filtering in Streamlit
**Learning:** Using `format_func` in Streamlit selectboxes allows transforming raw data (like booleans or short codes) into user-friendly, semantic labels with emojis. This significantly reduces cognitive load and makes the interface more accessible by providing clear status indicators (e.g., "⚠️ Issues Found" vs "✅ No Issues") instead of generic "True/False" values.
**Action:** Always prefer `format_func` for boolean or categorical filters to provide immediate visual context and clearer meaning to users.
