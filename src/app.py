import os
import streamlit as st
from dotenv import load_dotenv

from agent import Agent
from llm_client import GeminiClient
from recommender import load_songs
from similarity_matrices import GENRE_SIMILARITY, MOOD_SIMILARITY

load_dotenv()

st.set_page_config(page_title="AI Music Recommender", page_icon="🎵", layout="wide")
st.title("AI Music Recommender")
st.caption("Generates music recommendations based on your preferences and self-iterates if results fall below the quality threshold.")

# ----------------------------
# Sidebar
# ----------------------------
st.sidebar.header("Settings")

model_name = st.sidebar.selectbox(
    "Gemini model",
    ["gemini-2.5-flash", "gemini-2.5-pro"],
)

temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.2,
    step=0.1,
    help="Lower = more consistent. Higher = more creative.",
)

show_debug = st.sidebar.checkbox("Show agent trace", value=False)

st.sidebar.divider()

api_key = os.getenv("GEMINI_API_KEY", "").strip()
if not api_key:
    st.sidebar.warning("No GEMINI_API_KEY found. Agent will run without Gemini.")
    client = None
else:
    client = GeminiClient(model_name=model_name, temperature=temperature)
    st.sidebar.success("Gemini client ready.")

# ----------------------------
# Song catalog (cached)
# ----------------------------
@st.cache_data
def get_songs():
    csv_path = os.path.join(os.path.dirname(__file__), "../data/songs.csv")
    return load_songs(csv_path)

songs = get_songs()

GENRES = sorted(GENRE_SIMILARITY.keys())
MOODS  = sorted(MOOD_SIMILARITY.keys())

# ----------------------------
# User profile inputs
# ----------------------------
st.subheader("Your Profile")

col_a, col_b = st.columns(2)

with col_a:
    genre = st.selectbox("Preferred genre", GENRES, index=GENRES.index("pop"))
    mood  = st.selectbox("Preferred mood",  MOODS,  index=MOODS.index("happy"))

with col_b:
    energy       = st.slider("Energy",       0.0, 1.0, 0.7, 0.05)
    valence      = st.slider("Valence",      0.0, 1.0, 0.7, 0.05)
    danceability = st.slider("Danceability", 0.0, 1.0, 0.6, 0.05)
    acousticness = st.slider("Acousticness", 0.0, 1.0, 0.3, 0.05)

user_prefs = {
    "genre":        genre,
    "mood":         mood,
    "energy":       energy,
    "valence":      valence,
    "danceability": danceability,
    "acousticness": acousticness,
}

run_button = st.button("Get Recommendations", type="primary", use_container_width=True)

# ----------------------------
# Results
# ----------------------------
if run_button:
    agent = Agent(client=client)

    with st.spinner("Running recommendation workflow..."):
        result = agent.run(user_prefs, songs, k=5)

    recommendations = result["recommendations"]
    passed           = result["passed_threshold"]
    logs             = result["logs"]

    st.divider()

    if passed:
        st.success("Recommendations passed the quality threshold.")
    else:
        st.warning("Recommendations fell below the quality threshold — Gemini was consulted.")

    st.subheader("Top Recommendations")
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        with st.expander(f"{rank}. {song['title']} — {song['artist']}  |  Score: {score:.2f}"):
            meta_col, score_col = st.columns([3, 1])
            with meta_col:
                st.write(f"**Genre:** {song['genre']}  |  **Mood:** {song['mood']}")
                st.write(f"**Why:** {explanation}")
            with score_col:
                st.metric("Score", f"{score:.2f}")

    if show_debug:
        st.divider()
        st.subheader("Agent Trace")
        for entry in logs:
            step, message = entry["step"], entry["message"]
            code_start = message.find("def ")
            if code_start != -1:
                st.write(f"**[{step}]** {message[:code_start].strip()}")
                st.code(message[code_start:], language="python")
            else:
                st.write(f"**[{step}]** {message}")
