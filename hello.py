import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the movies dataset
movies_data = pd.read_csv("https://raw.githubusercontent.com/nv-thang/Data-Visualization-Course/main/movies.csv")

# Convert 'year' to string for better compatibility with Streamlit widgets
movies_data['year'] = movies_data['year'].astype(str)

# Sidebar: Movie Score Filter
st.sidebar.write("Select a range on the slider (it represents movie score) to view the total number of movies in a genre that falls within that range")
score_range = st.sidebar.slider("Choose a score range:", 1.0, 10.0, (3.0, 4.0), 0.01)

# Sidebar: Genre and Year Filter
st.sidebar.write("Select your preferred genre(s) and year to view the movies released that year and in that genre")
selected_genres = st.sidebar.multiselect("Choose genre:", movies_data['genre'].unique(), ["Animation", "Horror", "Fantasy", "Romance"])
selected_year = st.sidebar.selectbox("Choose a Year", movies_data['year'].unique())

# Filtering data based on the slider range
filtered_by_score = movies_data[(movies_data['score'] >= score_range[0]) & (movies_data['score'] <= score_range[1])]

# Filtering data based on selected genre and year
filtered_data = movies_data[(movies_data['genre'].isin(selected_genres)) & (movies_data['year'] == selected_year)]

# Content
st.markdown("<h2>Interactive Dashboard</h2>", unsafe_allow_html=True)
st.markdown("<h3>Interact with this dashboard using the widgets on the sidebar</h3>", unsafe_allow_html=True)

# Column layout for movie list and line chart
cols = st.columns(2)

# Display the filtered data in the first column
with cols[0]:
    if not filtered_data.empty:
        st.markdown("<h4>Lists of movies filtered by year and Genre</h4>", unsafe_allow_html=True)
        filtered_data_sorted = filtered_data.sort_values(by='name')
        st.dataframe(filtered_data_sorted[['name', 'genre', 'year']].reset_index(drop=True))
    else:
        st.write("No movies found for the selected filters.")

# Calculate total score by genre
total_score_by_genre = filtered_by_score.groupby('genre')['score'].count()

# Display the line chart in the second column
with cols[1]:
    st.markdown("<h4>User score of movies and their genre</h4>", unsafe_allow_html=True)
    st.line_chart(total_score_by_genre, use_container_width=True)

# Display the average movie budget by genre below the columns
st.write("Average Movie Budget, Grouped by Genre")
avg_budget = movies_data.groupby('genre')['budget'].mean().round()
avg_budget = avg_budget.reset_index()
genre = avg_budget['genre']
avg_bud = avg_budget['budget']

fig = plt.figure(figsize=(19, 10))
plt.bar(genre, avg_bud, color='maroon')
plt.xlabel('genre')
plt.ylabel('budget')
plt.title('Matplotlib Bar Chart Showing the Average Budget of Movies in Each Genre')
st.pyplot(fig)
