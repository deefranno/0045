import streamlit as st 
import pandas as pd

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
        , "Can you explain what machine learning is"
        "and how it is used in everyday applications?"
        , "How do penguins fly?"
    ],           
    "Answers": 
        ["The internet was invented in the late 1800s"
        "by Sir Archibald Internet, an English inventor and tea enthusiast",
        "The Northern Lights, or Aurora Borealis"
        ", are caused by the Earth's magnetic field interacting" 
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
         "You will now notice our dataframe is in the editing mode. Try to "
         "select an **Issue Category** and check **Has Issue?** if you find any problems. "
         "Finally, check **Reviewed?** when you're done with a row 👇")

df["Reviewed"] = [True, True, True, False]
df["Issue"] = [True, True, True, False]
df['Category'] = ["Accuracy", "Accuracy", "Completeness", ""]

new_df = st.data_editor(
    df,
    column_config = {
        "Questions":st.column_config.TextColumn(
            width = "medium",
            disabled=True
        ),
        "Answers":st.column_config.TextColumn(
            width = "medium",
            disabled=True
        ),
        "Reviewed":st.column_config.CheckboxColumn(
            "Reviewed?",
            help = "Check this when you have finished evaluating this row",
            default = False
        ),
        "Issue":st.column_config.CheckboxColumn(
            "Has Issue?",
            help = "Check if this response has a quality issue",
            default = False
        ),
        "Category":st.column_config.SelectboxColumn(
            "Issue Category",
            help = "Select the category of the issue identified",
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
    issue_filter = st.selectbox("Issues or Non-issues", options = new_df.Issue.unique())
with col2:
    category_filter = st.selectbox("Choose a category", options  = new_df[new_df["Issue"]==issue_filter].Category.unique())

st.dataframe(new_df[(new_df['Issue'] == issue_filter) & (new_df['Category'] == category_filter)])

st.markdown("")
st.write("*Next*, we can visualize our data quickly using `st.metrics` and `st.bar_plot`")

issue_cnt = len(new_df[new_df['Issue']==True])
reviewed_cnt = len(new_df[new_df['Reviewed']==True])
total_cnt = len(new_df)
reviewed_perc = reviewed_cnt / total_cnt

st.progress(reviewed_perc, text=f"Annotation Progress: {reviewed_perc*100:.0f}%")

col1, col2 = st.columns([1,1])
with col1:
    st.metric("Number of Issues Identified", issue_cnt)
with col2:
    st.metric("Total Rows Reviewed", reviewed_cnt)

df_plot = new_df[new_df['Category']!=''].Category.value_counts().reset_index()

st.bar_chart(df_plot, x = 'Category', y = 'count')

if reviewed_perc == 1.0:
    st.balloons()
    st.success("Congratulations! You have finished all annotations. 🎉")

    csv = new_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Annotated Data as CSV",
        data=csv,
        file_name="annotated_data.csv",
        mime="text/csv",
    )

st.write("Here we are at the end of getting started with streamlit! Happy Streamlit-ing! :balloon:")

