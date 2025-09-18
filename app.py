#kevon dawkins
#Cuny Tech Prep
#Data Science Bootcamp
#Week 3 Exercise - MovieLens Dashboard


import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="MovieLens Dashboard", layout="wide")


# Load Dataset

def load_data():
    return pd.read_csv("data/movie_ratings.csv")

df = load_data()
st.title("🎬 MovieLens Dashboard - Week 3 Exercise")

st.write("Dataset preview:")
st.dataframe(df.head())


# Sidebar Filters

st.sidebar.header("Filters")

# Age filter
min_age = int(df["age"].min())
max_age = int(df["age"].max())
age_range = st.sidebar.slider("Select Age Range", min_age, max_age, (20, 40))

# Genre filter
all_genres = df["genres"].unique().tolist()
selected_genres = st.sidebar.multiselect("Select Genres", all_genres)

# Apply filters
filtered_df = df[(df["age"] >= age_range[0]) & (df["age"] <= age_range[1])]

if selected_genres:
    filtered_df = filtered_df[filtered_df["genres"].isin(selected_genres)]

st.write(f"Filtered dataset: {filtered_df.shape[0]} rows")
st.dataframe(filtered_df.head())


# Q1: Breakdown of Genres

st.header("1. Breakdown of Genres")
genre_counts = filtered_df['genres'].value_counts()
fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(y=genre_counts.index[:15], x=genre_counts.values[:15], ax=ax, palette="viridis")
ax.set_xlabel("Number of Ratings")
ax.set_ylabel("Genre")
st.pyplot(fig)


# Q2: Highest Satisfaction Genres

st.header("2. Genres with Highest Viewer Satisfaction")
avg_ratings = filtered_df.groupby("genres")["rating"].mean().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(x=avg_ratings.values, y=avg_ratings.index, ax=ax, palette="coolwarm")
ax.set_xlabel("Average Rating")
ax.set_ylabel("Genre")
st.pyplot(fig)


# Q3: Mean Rating by Release Year

st.header("3. Mean Rating Across Movie Release Years")
ratings_by_year = filtered_df.groupby("year")["rating"].mean().dropna()
fig, ax = plt.subplots(figsize=(12,6))
sns.lineplot(x=ratings_by_year.index, y=ratings_by_year.values, marker="o", ax=ax)
ax.set_xlabel("Release Year")
ax.set_ylabel("Mean Rating")
st.pyplot(fig)


# Q4: Best Rated Movies

st.header("4. Top 5 Best-Rated Movies")
movie_stats = filtered_df.groupby("title")["rating"].agg(["mean","count"])

best50 = movie_stats[movie_stats["count"] >= 50].sort_values("mean", ascending=False).head(5)
best150 = movie_stats[movie_stats["count"] >= 150].sort_values("mean", ascending=False).head(5)

st.subheader("Top 5 Movies (≥50 ratings)")
st.table(best50)

st.subheader("Top 5 Movies (≥150 ratings)")
st.table(best150)


# Insights

st.header("📊 Insights & Conclusions")
st.markdown("""
- **Drama & Comedy** dominate ratings volume.
- **Film-Noir & War** movies receive the highest average ratings.
- **Older movies (1930s–50s)** trend higher in ratings; **1990s movies** average lower.
- **Best-rated films** include *A Close Shave (1995)*, *Schindler’s List (1993)*, *The Wrong Trousers (1993)*, *Casablanca (1942)*, and *The Shawshank Redemption (1994)*.
""")

# end 
#had little time for doing extra credit