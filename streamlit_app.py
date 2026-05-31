import streamlit as st 
import pandas as pd

st.set_page_config(page_title="Data Evaluation App", page_icon="🎨")
st.markdown("# Data Evaluation App")

st.write("We are so glad to see you here. ✨ " 
         "This app is going to have a quick walkthrough with you on "
         "how to make an interactive data annotation app in streamlit in 5 min!")

st.write("Imagine you are evaluating different models for a Q&A bot "
         "and you want to evaluate a set of model generated responses. "
        "You have collected some user data. "
         "Here is a sample question and response set.")

data = {
    "Questions": 
        ["Who invented the internet?"
        , "What causes the Northern Lights?"
        , "Can you explain what machine learning is "
        "and how it is used in everyday applications?"
        , "How do penguins fly?"
    ],           
    "Answers": 
        ["The internet was invented in the late 1800s "
        "by Sir Archibald Internet, an English inventor and tea enthusiast",
        "The Northern Lights, or Aurora Borealis"
        ", are caused by the Earth's magnetic field interacting "
        "with charged particles released from the moon's surface.",
        "Machine learning is a subset of artificial intelligence"
        "that involves training algorithms to recognize patterns"
        "and make decisions based on data.",
        " Penguins are unique among birds because they can fly underwater. "
        "Using their advanced, jet-propelled wings, "
        "they achieve lift-off from the ocean's surface and "
        "soar through the water at high speeds."
    ]
}

df = pd.DataFrame(data)

st.write(df)

st.write("Now I want to evaluate the responses from my model. "
         "One way to achieve this is to use the very powerful `st.data_editor` feature. "
         "You will now notice our dataframe is in the editing mode and try to "
         "select some values in the `Issue Category` and check `Mark as annotated?` once finished 👇")

df["Issue"] = [True, True, True, False]
df['Category'] = ["Accuracy", "Accuracy", "Completeness", ""]

new_df = st.data_editor(
    df,
    width='stretch',
    column_config = {
        "Questions":st.column_config.TextColumn(
            "Question",
            help = "The original question from the dataset",
            width = "medium",
            disabled=True
        ),
        "Answers":st.column_config.TextColumn(
            "Model Answer",
            help = "The model-generated response to be evaluated",
            width = "medium",
            disabled=True
        ),
        "Issue":st.column_config.CheckboxColumn(
            "Annotated?",
            help = "Check this box to mark the response as reviewed",
            default = False
        ),
        "Category":st.column_config.SelectboxColumn
        (
        "Issue Category",
        help = "Assign a classification to the response quality",
        options = ['Accuracy', 'Relevance', 'Coherence', 'Bias', 'Completeness'],
        required = False
        )
    }
)

st.write("You will notice that we changed our dataframe and added new data. "
         "Now it is time to visualize what we have annotated!")

st.divider()

st.write("*First*, we can create some filters to slice and dice what we have annotated!")

col1, col2 = st.columns([1,1])
with col1:
    issue_filter = st.selectbox(
        "Filter by Annotation Status",
        options=[True, False],
        format_func=lambda x: "✅ Annotated" if x else "⏳ Pending"
    )
with col2:
    available_categories = new_df[new_df["Issue"]==issue_filter].Category.unique()
    category_filter = st.selectbox(
        "Choose a category",
        options=available_categories,
        disabled=len(available_categories) == 0
    )

st.dataframe(
    new_df[(new_df['Issue'] == issue_filter) & (new_df['Category'] == category_filter)],
    width='stretch'
)

st.markdown("")
st.write("*Next*, we can visualize our data quickly using `st.metrics` and `st.bar_plot`")

issue_cnt = len(new_df[new_df['Issue']])
total_cnt = len(new_df)
progress_value = issue_cnt / total_cnt if total_cnt > 0 else 0
issue_perc = f"{progress_value*100:.0f}%"

col1, col2 = st.columns([1,1])
with col1:
    st.metric("Annotated Responses", issue_cnt, help="Total number of items marked as annotated")
with col2:
    st.metric("Annotation Progress", issue_perc, help="Percentage of total items completed")

st.progress(progress_value)

df_plot = new_df[new_df['Category']!=''].Category.value_counts().reset_index()

st.bar_chart(df_plot, x = 'Category', y = 'count')

st.write("Here we are at the end of getting started with streamlit! Happy Streamlit-ing! :balloon:")

# Micro-UX: Trigger balloons only on 100% completion
if issue_cnt == total_cnt and total_cnt > 0:
    if not st.session_state.get('celebrated', False):
        st.balloons()
        st.session_state.celebrated = True
else:
    # Reset celebration state if they uncheck something
    st.session_state.celebrated = False
