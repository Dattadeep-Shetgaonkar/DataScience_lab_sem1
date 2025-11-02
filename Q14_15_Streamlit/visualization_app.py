import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Course Data Visualization (Streamlit)")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("coursera_courses.csv")

df = load_data()

st.write("## Data Preview")
st.dataframe(df)

# Bar chart: Number of courses by duration
st.write("## Number of Courses by Duration")
dur_counts = df['Duration'].value_counts()
fig, ax = plt.subplots()
dur_counts.plot(kind='bar', ax=ax)
plt.xlabel('Duration')
plt.ylabel('Number of Courses')
st.pyplot(fig)

# Pie chart: Top 5 skills
st.write("## Top 5 Skills (by frequency)")
skills = df['Skills'].dropna().str.split(',').explode().str.strip()
skill_counts = skills.value_counts().head(5)
st.bar_chart(skill_counts)
