import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Data Evaluation Dashboard",
    page_icon="📊",
    layout="wide"
)

st.markdown("# Data Evaluation App")

st.write("We are so glad to see you here. ✨ "
         "This app is a walkthrough on how to make an interactive "
         "data annotation app in Streamlit in 5 min!")

st.write("Imagine you are evaluating model-generated responses for a Q&A bot. "
         "You have collected some user data. Here is a sample question and response set.")

data = {
    "Questions": [
        "Who invented the internet?",
        "What causes the Northern Lights?",
        "Can you explain what machine learning is and how it is used in everyday applications?",
        "How do penguins fly?"
    ],
    "Answers": [
        "The internet was invented in the late 1800s by Sir Archibald Internet, an English inventor and tea enthusiast.",
        "The Northern Lights, or Aurora Borealis, are caused by the Earth's magnetic field interacting with charged particles released from the moon's surface.",
        "Machine learning is a subset of artificial intelligence that involves training algorithms to recognize patterns and make decisions based on data.",
        "Penguins are unique among birds because they can fly underwater. Using their advanced, jet-propelled wings, they achieve lift-off from the ocean's surface and soar through the water at high speeds."
    ]
}

df = pd.DataFrame(data)

# Initializing annotation state
if 'df' not in st.session_state:
    df["Reviewed"] = [True, True, True, False]
    df["Issue"] = [True, True, False, False]
    df['Category'] = ["Accuracy", "Accuracy", "None", "None"]
    st.session_state.df = df

st.write("Use the `st.data_editor` below to evaluate the model responses. "
         "Mark rows as **Reviewed** and specify if an **Issue** was found 👇")

# Configuration for columns
column_config = {
    "Questions": st.column_config.TextColumn(width="medium", disabled=True),
    "Answers": st.column_config.TextColumn(width="medium", disabled=True),
    "Reviewed": st.column_config.CheckboxColumn("Reviewed?", help="Mark if you have finished evaluating this row"),
    "Issue": st.column_config.CheckboxColumn("Issue Found?", help="Check if the response contains an error"),
    "Category": st.column_config.SelectboxColumn(
        "Issue Category",
        help="Select the category of the issue found",
        options=['None', 'Accuracy', 'Relevance', 'Coherence', 'Bias', 'Completeness'],
        required=True,
        default="None"
    )
}

new_df = st.data_editor(
    st.session_state.df,
    column_config=column_config,
    hide_index=True,
    width="stretch"
)

# Save changes to session state
st.session_state.df = new_df

# Progress tracking and completion celebratory animation
total_cnt = len(new_df)
reviewed_cnt = new_df["Reviewed"].sum()
issue_cnt = new_df["Issue"].sum()
is_complete = (reviewed_cnt == total_cnt) and (total_cnt > 0)

if is_complete and not st.session_state.get("celebrated", False):
    st.balloons()
    st.session_state.celebrated = True
elif not is_complete:
    st.session_state.celebrated = False

if is_complete:
    st.success("All responses have been reviewed! 🎉")

st.divider()

st.write("### 🔍 Visualize Annotations")
st.write("Use the filters below to slice and dice your evaluated data.")

col1, col2 = st.columns([1, 1])

with col1:
    status_options = sorted(new_df.Reviewed.unique(), reverse=True)
    status_filter = st.selectbox(
        "Filter by Review Status",
        options=status_options,
        format_func=lambda x: "✅ Reviewed" if x else "⏳ Pending",
        help="Filter the table by whether rows have been reviewed"
    )

with col2:
    # Filter categories based on status, excluding empty/None if we want to focus on issues
    available_categories = sorted(new_df[new_df["Reviewed"] == status_filter].Category.unique())
    category_filter = st.selectbox(
        "Filter by Category",
        options=available_categories,
        help="Filter the table by issue category",
        disabled=len(available_categories) == 0
    )

filtered_df = new_df[(new_df['Reviewed'] == status_filter) & (new_df['Category'] == category_filter)]

if not filtered_df.empty:
    st.dataframe(filtered_df, hide_index=True, width="stretch")
else:
    st.info("No records found for the selected filters.")

st.markdown("")
st.write("### 📈 Analytics Dashboard")

issue_perc = f"{(reviewed_cnt / total_cnt) * 100:.0f}%" if total_cnt > 0 else "0%"

m_col1, m_col2, m_col3 = st.columns(3)
with m_col1:
    st.metric("Total Responses", total_cnt, help="Total number of items to be evaluated")
with m_col2:
    st.metric("Review Progress", issue_perc, help="Percentage of items that have been reviewed")
with m_col3:
    st.metric("Issues Found", int(issue_cnt), help="Total number of items marked with an issue")

# Plot only issues
df_plot = new_df[new_df['Category'] != 'None'].Category.value_counts().reset_index()

if not df_plot.empty:
    st.bar_chart(df_plot, x='Category', y='count')
else:
    st.info("No issues found yet to visualize.")

st.write("Happy Streamlit-ing! :balloon:")
