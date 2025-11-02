import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os

# ------------------ Database Connection ------------------ #
# Build absolute path dynamically
db_path = os.path.join(os.path.dirname(__file__), 'movies.sqlite')
print("Using database:", db_path)  # For debugging
engine = create_engine(f"sqlite:///{db_path}")

st.title("🎬 Movies Dataset — Search & Filter Dashboard")

# ------------------ Dropdown Options ------------------ #
directors = pd.read_sql("SELECT id, name FROM directors", engine)
director_options = ["All"] + sorted(directors['name'].dropna().unique().tolist())

movie_titles = pd.read_sql(
    "SELECT original_title FROM movies ORDER BY original_title", engine
)['original_title'].tolist()

# ------------------ Filters UI ------------------ #
selected_title = st.selectbox("🔍 Search Movie Title", [""] + movie_titles)
selected_director = st.selectbox("🎥 Choose Director", director_options)

min_year, max_year = pd.read_sql(
    "SELECT MIN(strftime('%Y', release_date)), MAX(strftime('%Y', release_date)) FROM movies", engine
).iloc[0]
year_range = st.slider("📅 Release Year", int(min_year), int(max_year), (int(min_year), int(max_year)))

min_budget, max_budget = pd.read_sql(
    "SELECT MIN(budget), MAX(budget) FROM movies", engine
).iloc[0]
budget_range = st.slider("💰 Budget Range", int(min_budget), int(max_budget), (int(min_budget), int(max_budget)))

ratings = pd.read_sql(
    "SELECT DISTINCT ROUND(vote_average, 0) AS r FROM movies ORDER BY r", engine
)['r'].tolist()
selected_ratings = st.multiselect("⭐ Rating", ratings)

# ------------------ Build Query ------------------ #
query = """
SELECT m.id, m.original_title, m.release_date,
       m.budget, m.revenue, m.vote_average, m.tagline, d.name AS director_name
FROM movies m
LEFT JOIN directors d ON m.director_id = d.id
WHERE 1=1
"""

params = {}
if selected_title:
    query += " AND m.original_title = :title"
    params["title"] = selected_title
if selected_director != "All":
    query += " AND d.name = :director"
    params["director"] = selected_director
query += " AND CAST(strftime('%Y', m.release_date) AS INTEGER) BETWEEN :start_year AND :end_year"
params["start_year"], params["end_year"] = year_range
query += " AND m.budget BETWEEN :min_budget AND :max_budget"
params["min_budget"], params["max_budget"] = budget_range
if selected_ratings:
    rating_list = ",".join([str(int(r)) for r in selected_ratings])
    query += f" AND ROUND(m.vote_average, 0) IN ({rating_list})"

filtered_data = pd.read_sql(query, engine, params=params)
st.write(f"🎯 **{len(filtered_data)} movies found:**")
st.dataframe(filtered_data)
