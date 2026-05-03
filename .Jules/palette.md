# Palette's Journal - Data Evaluation App

## 2024-05-15 - Streamlit UX Fundamentals
**Learning:** Initial unconditional animations (like st.balloons()) can be distracting and lose their impact if they fire on every page load. Gating them behind a terminal success state (100% completion) and using st.session_state to ensure they only trigger once provides a much more rewarding user experience. Additionally, using 'wide' layout in Streamlit is essential for data-heavy applications to avoid horizontal scrolling and cramped components.
**Action:** Always gate celebratory animations behind specific achievements and prefer 'wide' layout for data dashboards.

## 2024-05-15 - Semantic Labels and Progress Tracking
**Learning:** Using 'format_func' in selectboxes allows for semantic labels (e.g., '✅ Annotated' vs '⏳ Pending') that improve accessibility and speed of comprehension. Pairing this with a 'st.progress' bar provides immediate visual feedback on the task status.
**Action:** Use emojis and semantic labels in filters to bridge the gap between technical data states and user-facing concepts.
