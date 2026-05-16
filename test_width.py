import streamlit as st
import pandas as pd
df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
try:
    st.dataframe(df, width="stretch")
    print("Success: width='stretch' is accepted")
except Exception as e:
    print(f"Error: {e}")
