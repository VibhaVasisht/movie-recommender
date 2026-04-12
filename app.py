import streamlit as st
from recommender import load_and_process_data, recommend, get_movie_list

# Page config
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
        background-color: #0a0e27;
    }
    
    .title-container {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #1a1f3a 0%, #0f1419 100%);
        border-radius: 10px;
        color: #e0e0e0;
        margin-bottom: 2rem;
        border: 1px solid #2a3f5f;
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #a0a0a0;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .recommendation-card {
        background: linear-gradient(135deg, #1a2332 0%, #0f1620 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: #e0e0e0;
        margin: 1rem 0;
        font-size: 1.1rem;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        border-left: 3px solid #00bfff;
        transition: transform 0.3s ease;
    }
    
    .recommendation-card:hover {
        transform: translateX(5px);
        border-left-color: #0099cc;
    }
    
    .input-section {
        background-color: #121829;
        padding: 2rem;
        border-radius: 10px;
        margin: 2rem 0;
        border: 1px solid #2a3f5f;
    }
    
    .results-header {
        border-left: 5px solid #00bfff;
        padding-left: 1rem;
        margin: 2rem 0 1rem 0;
        color: #e0e0e0;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("""
    <div class="title-container">
        <h1>Movie Recommender System</h1>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <p class="subtitle">Discover movies similar to your favourites</p>
""", unsafe_allow_html=True)

try:
    # Sidebar info
    with st.sidebar:
        st.markdown("### About This App")
        st.info("""
        This recommender system uses content-based filtering to find movies similar to the one you choose.
        
        It analyzes:
        - Genres
        - Cast & Crew
        - Overview & Keywords
        """)
        
        st.markdown("---")
        st.markdown("### Dataset Info")
        st.write("Data: TMDB 5000 Movies & Credits")
    
    # Load data (this might take a moment)
    with st.spinner("Loading movie database..."):
        new_df, similarity = load_and_process_data()

    movie_list = get_movie_list(new_df)

    # Input section
    st.markdown("""
        <div class="input-section">
            <h3 style="color: #e0e0e0;">Find Similar Movies</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        selected_movie = st.selectbox(
            "Choose your movie:",
            movie_list,
            index=None,
            placeholder="Type or select a movie...",
            help="Select a movie from the database"
        )
    
    with col2:
        search_button = st.button("Search", use_container_width=True)

    # Results section
    if search_button:
        with st.spinner("Finding similar movies..."):
            recommendations = recommend(selected_movie, new_df, similarity)

        st.markdown("""
            <div class="results-header">
                <h2 style="color: #e0e0e0;">Movies Similar to: <span style="color: #00bfff;">{}</span></h2>
            </div>
        """.format(selected_movie), unsafe_allow_html=True)
        
        st.write("")  # Spacing
        
        if recommendations[0] != "Movie not found in database":
            for i, movie in enumerate(recommendations, 1):
                st.markdown(
                    f'<div class="recommendation-card">#{i} {movie}</div>',
                    unsafe_allow_html=True
                )
        else:
            st.warning("Movie not found in the database. Please select another movie.")

except FileNotFoundError as e:
    st.error("Error: " + str(e))
    st.info("Please download the TMDB 5000 Movies and Credits datasets and place them in the project directory.")
except Exception as e:
    st.error(f"An error occurred: {str(e)}")