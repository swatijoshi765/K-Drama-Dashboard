import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

#Load data
df = pd.read_csv(r"C:\Users\swati\Desktop\kdrama dashboard\kdrama.csv")


# Rename columns if needed
df.rename(columns={
    'Name': 'Title',
    'Year of release': 'Year',
    'Original Network': 'Platform',
    'Genres': 'Genre',
    'Cast': 'Cast'
}, inplace=True)

# Clean data
df.dropna(subset=['Title', 'Genre', 'Rating', 'Cast'], inplace=True)

st.set_page_config(page_icon="k-drama dashboard",layout="wide")

st.title("🎬 K-Drama Dashboard")

#stats summary 

st.markdown("### 🔢 Summary Stats")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total K-dramas",len(df))

with col2:
    avg_rating = round(df['Rating'].mean(),2)
    st.metric("Average Rating ⭐", avg_rating)

with col3:
    platforms = df['Platform'].nunique()
    st.metric("Platforms Available", platforms)

# REPLACE THE OLD CODE WITH THIS


import os
import base64
from PIL import Image

# --- CSS to create the image container ---
st.markdown("""
<style>
.image-container-3-1 {
    width: 200px; /* You can adjust this width */
    height: 250px; /* 3:1 ratio to the width */
    overflow: hidden; /* This hides the parts of the image that are outside the frame */
    border-radius: 8px; /* Optional: adds rounded corners */
    box-shadow: 0 4px 8px rgba(0,0,0,0.1); /* Optional: adds a subtle shadow */
}

.image-container-3-1 img {
    width: 100%;
    height: 100%;
    object-fit: cover; /* This makes the image cover the whole container without stretching */
    object-position: center; /* This ensures the center of the image is shown */
}
</style>
""", unsafe_allow_html=True)


# --- Your existing app logic ---
st.markdown("## 🔍 Search Cast to View Image")

# Get cast list from dataset (Assuming 'df' is your DataFrame)
all_cast_names = set()
for cast in df['Cast'].dropna():
    names = [n.strip() for n in cast.split(',')]
    all_cast_names.update(names[:2])

all_cast_names = sorted(list(all_cast_names))

# Streamlit selectbox
selected_name = st.selectbox("Select an Actor/Actress", ["-- Select --"] + all_cast_names)

# Show image if selected
if selected_name != "-- Select --":
    image_path = f"images/cast_pics/{selected_name}.jpg"
    if os.path.exists(image_path):
        # We need to encode the local image to display it in HTML
        with open(image_path, "rb") as f:
            data = f.read()
        encoded_image = base64.b64encode(data).decode()

        # Use markdown to display the image inside our styled container
        st.markdown(
            f"""
            <div class="image-container-3-1">
                <img src="data:image/jpeg;base64,{encoded_image}" alt="{selected_name}">
            </div>
            """,
            unsafe_allow_html=True
        )
        st.caption(selected_name) # You can still have a caption below
    else:
        st.markdown(
            f"""<div class='cast-image-warning'>
                <span>❌ No image found for <strong>{selected_name}</strong>.</span>
            </div>""",
            unsafe_allow_html=True
        )

from PIL import Image
import os

filtered_df = df.copy()

top_dramas = filtered_df.sort_values(by="Rating", ascending=False).head(10)

# (Your code to get the 'top_dramas' DataFrame goes here)
# top_dramas = df.sort_values(by="Rating", ascending=False).head(10)

# --- REPLACEMENT CODE STARTS HERE ---

st.markdown("## ⭐ Top 10 Highest Rated K-Dramas")

# Define how many dramas you want per row
DRAMAS_PER_ROW = 2

# Calculate how many rows you'll need
num_rows = -(-len(top_dramas) // DRAMAS_PER_ROW) # A trick for ceiling division

# Loop through the rows
for i in range(num_rows):
    # Create a new set of columns for each row
    cols = st.columns(DRAMAS_PER_ROW)
    
    # Get the slice of dramas for the current row
    row_dramas = top_dramas.iloc[i*DRAMAS_PER_ROW : (i+1)*DRAMAS_PER_ROW]
    
    # Loop through the columns and the dramas for this row
    for col, (index, drama_info) in zip(cols, row_dramas.iterrows()):
        with col:
            # This is your exact card-rendering code from before
            st.markdown(f"#### {drama_info['Title']}")
            
            poster_path = f"images/drama_posters/{drama_info['Title']}.jpg"
            if os.path.exists(poster_path):
                st.image(poster_path, width= 200)
                
            st.markdown(f"**Rating:** ⭐ {drama_info['Rating']}")
            st.markdown(f"**Genre:** {drama_info['Genre']} | **Year:** {drama_info['Year']}")
            
            with st.expander("More Info"):
                st.markdown(f"**Platform:** {drama_info['Platform']}")
                st.markdown(f"**Cast:** {drama_info['Cast']}")
            
            # This adds a bit of space at the bottom of a card, which also helps alignment
            st.write("")
st.markdown("### 📅 Explore Highly Rated K-Dramas by Year")

# Let user choose a year from available ones
available_years = sorted(df['Year'].dropna().unique())
selected_year = st.selectbox("Select a Year", available_years, index=len(available_years)-1)

# Filter the dataframe
filtered_df = df[df['Year'] == selected_year].sort_values(by='Rating', ascending=False)

# Display the results
st.write(f"### 📌 Highly Rated K-Dramas from {selected_year}")
st.dataframe(filtered_df[['Title', 'Rating', 'Genre']].reset_index(drop=True), use_container_width=True)

# --------------------------------------------
# 📂 Sidebar Filters 
# --------------------------------------------

st.sidebar.header("📂 Filter K-Dramas")

# Genre filter
all_genres = set(g.strip() for sublist in df['Genre'].dropna().str.split(',') for g in sublist)
selected_genres = st.sidebar.multiselect("Select Genre(s)", sorted(all_genres))

# Year filter
all_years = sorted(df['Year'].dropna().unique())
selected_years = st.sidebar.multiselect("Select Year(s)", all_years)

# Platform filter
all_platforms = sorted(df['Platform'].dropna().unique())
selected_platforms = st.sidebar.multiselect("Select Platform(s)", all_platforms)

# --------------------------------------------
# Apply Filters to DataFrame
# --------------------------------------------

filtered_df = df.copy()

# Genre filter logic
if selected_genres:
    filtered_df = filtered_df[filtered_df['Genre'].apply(
        lambda g: any(genre.strip() in g for genre in selected_genres) if pd.notna(g) else False
    )]

# Year filter logic
if selected_years:
    filtered_df = filtered_df[filtered_df['Year'].isin(selected_years)]

# Platform filter logic
if selected_platforms:
    filtered_df = filtered_df[filtered_df['Platform'].isin(selected_platforms)]



st.subheader("🎬 Filtered K-Drama Results")
st.write(f"Total results: {len(filtered_df)}")
st.dataframe(filtered_df)







st.markdown("### 📊 K-Drama Visual Insights")

col1, col2 = st.columns(2)

# --- Genre Bar Chart ---
with col1:
    st.markdown("#### 🎭 Genre Distribution")
    genre_counts = df['Genre'].dropna().str.split(', ').explode().value_counts().head(10)
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.barplot(x=genre_counts.values, y=genre_counts.index, palette='pastel', ax=ax)
    ax.set_xlabel("Count")
    st.pyplot(fig)

# --- Platform Pie Chart ---
with col2:
    st.markdown("#### 📺 Platform Distribution")
    platform_series = df['Platform'].dropna().str.split(', ').explode()
    platform_counts = platform_series.value_counts()

    top7 = platform_counts[:7]
    others = platform_counts[7:].sum()
    final = pd.concat([top7, pd.Series({'Others': others})])

    fig2, ax2 = plt.subplots(figsize=(5, 3))
    ax2.pie(final.values, labels=final.index, autopct='%1.1f%%', startangle=140)
    ax2.axis('equal')
    st.pyplot(fig2)



# Tabs inside columns to reduce vertical scroll
st.markdown("### 📈 Data Insights")
top_row = st.columns(2)

# --- ⭐ Rating Distribution ---
with top_row[0]:
    st.markdown("#### ⭐ Rating Distribution")
    fig3, ax3 = plt.subplots(figsize=(4.5, 3))
    sns.histplot(df['Rating'], bins=10, kde=True, ax=ax3, color="skyblue")
    ax3.set_xlabel("Rating")
    ax3.set_ylabel("Number of Dramas")
    st.pyplot(fig3)

# --- 📊 Top Platforms ---
with top_row[1]:
    st.markdown("#### 📊 Top 10 Platforms")
    top_platforms = df['Platform'].dropna().str.split(', ').explode().value_counts().head(10)
    fig4, ax4 = plt.subplots(figsize=(4.5, 3))
    sns.barplot(x=top_platforms.index, y=top_platforms.values, ax=ax4, palette="mako")
    ax4.set_ylabel("Drama Count")
    ax4.set_xlabel("")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig4)

# Bottom row
bottom_row = st.columns(2)

# --- 🕒 Timeline ---
with bottom_row[0]:
    st.markdown("#### 🕒 Yearly Release Trend")
    year_counts = df['Year'].value_counts().sort_index()
    fig5, ax5 = plt.subplots(figsize=(4.5, 3))
    sns.lineplot(x=year_counts.index, y=year_counts.values, marker="o", ax=ax5, color="green")
    ax5.set_xlabel("Year")
    ax5.set_ylabel("Number of Dramas")
    st.pyplot(fig5)

# --- 🔍 Search ---
with bottom_row[1]:
    st.markdown("#### 🔍 Search & Explore")
    search_input = st.text_input("Search by Title, Platform, Genre, or Lead Actor")
    if search_input:
        search_df = df[
            df['Title'].str.contains(search_input, case=False, na=False) |
            df['Platform'].str.contains(search_input, case=False, na=False) |
            df['Genre'].str.contains(search_input, case=False, na=False) |
            df['Cast'].str.contains(search_input, case=False, na=False)
        ]
    else:
        search_df = df
    st.dataframe(search_df.reset_index(drop=True), use_container_width=True)