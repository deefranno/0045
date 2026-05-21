## 2026-05-21 - Accessible Boolean Selectboxes in Streamlit
**Learning:** Streamlit's 'st.selectbox' uses the raw values of the 'options' list as labels by default. For boolean filters, this results in 'True/False' which is not user-friendly. Using 'format_func' allows mapping these technical values to semantic, accessible labels with visual cues (like emojis).
**Action:** Always use 'format_func' with 'st.selectbox' when the underlying data values are technical or boolean to provide better context and accessibility.
