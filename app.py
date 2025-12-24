import pickle
import streamlit as st
import random
import time

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="CineSense",
    page_icon="🎬",
    layout="wide"
)

# ================= DYNAMIC THEME COLORS =================
ACCENTS = ["#ff4b4b", "#7c7cff", "#00c896", "#ff9f1c", "#e056fd"]
ACCENT = random.choice(ACCENTS)

# ================= CSS =================
st.markdown(f"""
<style>
body {{
    background-color: #0b0e14;
}}

.hero-title {{
    font-size: 46px;
    font-weight: 900;
}}

.hero-sub {{
    color: #9aa0a6;
    font-size: 17px;
    max-width: 720px;
}}

.stButton > button {{
    background: linear-gradient(135deg, {ACCENT}, #ffffff);
    color: black;
    border-radius: 16px;
    padding: 12px 30px;
    font-weight: 800;
    border: none;
}}

.movie-card {{
    background: rgba(30, 34, 48, 0.85);
    border-radius: 22px;
    padding: 26px;
    text-align: center;
    box-shadow: 0 20px 45px rgba(0,0,0,0.6);
    transition: all 0.3s ease;
    height: 170px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}}

.movie-card:hover {{
    transform: translateY(-10px) scale(1.05);
}}

.movie-title {{
    font-size: 20px;
    font-weight: 800;
}}

.movie-meta {{
    font-size: 13px;
    color: #b5b8c0;
}}

.fade-in {{
    animation: fadeIn 0.6s ease-in-out;
}}

@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(10px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown("""
<div class="hero-title">🎬 CineSense: AI-Powered Movie Recommender</div>
<div class="hero-sub">
Experience intelligent movie suggestions driven by content-based machine learning.
</div>
""", unsafe_allow_html=True)

# ================= LOAD DATA =================
@st.cache_resource
def load_data():
    movies = pickle.load(open("movie_list.pkl", "rb"))
    similarity = pickle.load(open("similarity.pkl", "rb"))
    return movies, similarity

movies, similarity = load_data()

# ================= RECOMMEND FUNCTION =================
def recommend(movie_title):
    index = movies[movies["title"] == movie_title].index[0]
    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )
    return [movies.iloc[i[0]].title for i in distances[1:6]]

# ================= INPUT (FIXED – NEVER BLANK) =================
st.markdown("### 🎥 Pick a movie you like")

selected_movie = st.selectbox(
    label="Movie selection",
    options=movies["title"].values,
    key="movie_select"
)

# ================= ACTION =================
if st.button("🚀 Generate Smart Recommendations"):
    with st.spinner("Analyzing your taste…"):
        time.sleep(0.8)  # makes it feel dynamic

    recommendations = recommend(selected_movie)

    st.markdown("### 🔥 Recommended for You")

    cols = st.columns(5)
    for col, movie in zip(cols, recommendations):
        with col:
            st.markdown(f"""
            <div class="movie-card fade-in">
                <div class="movie-title">{movie}</div>
                <div class="movie-meta">High content similarity</div>
            </div>
            """, unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown("""
<br>
<p style="text-align:center;color:#6f7380;font-size:13px;">
CineSense • Intelligent Content-Based Recommendation Engine
</p>
""", unsafe_allow_html=True)
