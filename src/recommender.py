from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

from similarity_matrices import GENRE_SIMILARITY, MOOD_SIMILARITY

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    genre: str
    mood: str
    energy: float
    valence: float
    danceability: float
    acousticness: float

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        """Initialize the recommender with a list of songs."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs ranked by score for the given user profile."""
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song was recommended."""
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv
    songs = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            song = {
                'id': int(row['id']),
                'title': row['title'],
                'artist': row['artist'],
                'genre': row['genre'],
                'mood': row['mood'],
                'energy': float(row['energy']),
                'tempo_bpm': float(row['tempo_bpm']),
                'valence': float(row['valence']),
                'danceability': float(row['danceability']),
                'acousticness': float(row['acousticness']),
            }
            songs.append(song)
    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """
    Implements "Algorithm Recipe" from Phase 2.
    Calculates overall score for individual song based on weighted-sum
    Weights are: genre=0.15, mood=0.20, energy=0.20, valence=0.15, danceability=0.15, accousticness=0.15
    - Song features acquired from load_songs()
    - Genre similarity value taken from GENRE_SIMILARITY
    - Mood similarity value taken from MOOD_SIMILARITY
    - Scores for numerical values are generated with
        - exp(-5 * (song_value - preference_value)^2) function e^x
    Returns an overall score float and a string reason for score.
    """
    import math

    genre_score = GENRE_SIMILARITY.get(user_prefs["genre"], {}).get(song["genre"], 0.0)
    mood_score = MOOD_SIMILARITY.get(user_prefs["mood"], {}).get(song["mood"], 0.0)

    energy_score = math.exp(-5 * (song["energy"] - user_prefs["energy"]) ** 2)
    valence_score = math.exp(-5 * (song["valence"] - user_prefs["valence"]) ** 2)
    danceability_score = math.exp(-5 * (song["danceability"] - user_prefs["danceability"]) ** 2)
    acousticness_score = math.exp(-5 * (song["acousticness"] - user_prefs["acousticness"]) ** 2)

    overall_score = (
        0.15 * genre_score +
        0.20 * mood_score +
        0.20 * energy_score +
        0.15 * valence_score +
        0.15 * danceability_score +
        0.15 * acousticness_score
    )

    explanation = (
        f"genre={genre_score:.2f}, mood={mood_score:.2f}, "
        f"energy={energy_score:.2f}, valence={valence_score:.2f}, "
        f"danceability={danceability_score:.2f}, acousticness={acousticness_score:.2f}"
    )

    return overall_score, explanation