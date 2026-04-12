from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# Mood similarity matrix — binary match values (0.0–1.0).
# Grouped by emotional character:
#   Positive/high-energy: happy, playful, celebratory, spirited, triumphant
#   Positive/low-energy:  chill, relaxed, focused, dreamy, romantic
#   Dark/high-energy:     intense, moody
#   Dark/low-energy:      melancholic, yearning, wistful, nostalgic
MOOD_SIMILARITY: Dict[str, Dict[str, float]] = {
    #              hap   chil  int   relx  mood  focu  melan play  nost  drmy  trmp  wist  yearn spir  celb  rom
    "happy":       {"happy":1.0, "chill":0.2, "intense":0.2, "relaxed":0.2, "moody":0.1, "focused":0.2, "melancholic":0.0, "playful":0.8, "nostalgic":0.2, "dreamy":0.5, "triumphant":0.4, "wistful":0.1, "yearning":0.1, "spirited":0.7, "celebratory":0.8, "romantic":0.5},
    "chill":       {"happy":0.2, "chill":1.0, "intense":0.0, "relaxed":0.9, "moody":0.3, "focused":0.7, "melancholic":0.3, "playful":0.1, "nostalgic":0.4, "dreamy":0.5, "triumphant":0.0, "wistful":0.5, "yearning":0.3, "spirited":0.1, "celebratory":0.0, "romantic":0.3},
    "intense":     {"happy":0.2, "chill":0.0, "intense":1.0, "relaxed":0.0, "moody":0.4, "focused":0.1, "melancholic":0.0, "playful":0.2, "nostalgic":0.1, "dreamy":0.1, "triumphant":0.7, "wistful":0.0, "yearning":0.0, "spirited":0.5, "celebratory":0.4, "romantic":0.0},
    "relaxed":     {"happy":0.2, "chill":0.9, "intense":0.0, "relaxed":1.0, "moody":0.2, "focused":0.5, "melancholic":0.3, "playful":0.1, "nostalgic":0.4, "dreamy":0.5, "triumphant":0.0, "wistful":0.5, "yearning":0.3, "spirited":0.1, "celebratory":0.0, "romantic":0.4},
    "moody":       {"happy":0.1, "chill":0.3, "intense":0.4, "relaxed":0.2, "moody":1.0, "focused":0.2, "melancholic":0.5, "playful":0.1, "nostalgic":0.4, "dreamy":0.3, "triumphant":0.2, "wistful":0.5, "yearning":0.6, "spirited":0.1, "celebratory":0.0, "romantic":0.3},
    "focused":     {"happy":0.2, "chill":0.7, "intense":0.1, "relaxed":0.5, "moody":0.2, "focused":1.0, "melancholic":0.1, "playful":0.1, "nostalgic":0.3, "dreamy":0.3, "triumphant":0.0, "wistful":0.3, "yearning":0.2, "spirited":0.2, "celebratory":0.0, "romantic":0.2},
    "melancholic": {"happy":0.0, "chill":0.3, "intense":0.0, "relaxed":0.3, "moody":0.5, "focused":0.1, "melancholic":1.0, "playful":0.0, "nostalgic":0.5, "dreamy":0.2, "triumphant":0.0, "wistful":0.7, "yearning":0.8, "spirited":0.0, "celebratory":0.0, "romantic":0.2},
    "playful":     {"happy":0.8, "chill":0.1, "intense":0.2, "relaxed":0.1, "moody":0.1, "focused":0.1, "melancholic":0.0, "playful":1.0, "nostalgic":0.1, "dreamy":0.3, "triumphant":0.1, "wistful":0.0, "yearning":0.0, "spirited":0.6, "celebratory":0.7, "romantic":0.3},
    "nostalgic":   {"happy":0.2, "chill":0.4, "intense":0.1, "relaxed":0.4, "moody":0.4, "focused":0.3, "melancholic":0.5, "playful":0.1, "nostalgic":1.0, "dreamy":0.4, "triumphant":0.0, "wistful":0.8, "yearning":0.6, "spirited":0.1, "celebratory":0.0, "romantic":0.3},
    "dreamy":      {"happy":0.5, "chill":0.5, "intense":0.1, "relaxed":0.5, "moody":0.3, "focused":0.3, "melancholic":0.2, "playful":0.3, "nostalgic":0.4, "dreamy":1.0, "triumphant":0.0, "wistful":0.4, "yearning":0.2, "spirited":0.3, "celebratory":0.2, "romantic":0.7},
    "triumphant":  {"happy":0.4, "chill":0.0, "intense":0.7, "relaxed":0.0, "moody":0.2, "focused":0.0, "melancholic":0.0, "playful":0.1, "nostalgic":0.0, "dreamy":0.0, "triumphant":1.0, "wistful":0.0, "yearning":0.0, "spirited":0.6, "celebratory":0.5, "romantic":0.0},
    "wistful":     {"happy":0.1, "chill":0.5, "intense":0.0, "relaxed":0.5, "moody":0.5, "focused":0.3, "melancholic":0.7, "playful":0.0, "nostalgic":0.8, "dreamy":0.4, "triumphant":0.0, "wistful":1.0, "yearning":0.7, "spirited":0.0, "celebratory":0.0, "romantic":0.3},
    "yearning":    {"happy":0.1, "chill":0.3, "intense":0.0, "relaxed":0.3, "moody":0.6, "focused":0.2, "melancholic":0.8, "playful":0.0, "nostalgic":0.6, "dreamy":0.2, "triumphant":0.0, "wistful":0.7, "yearning":1.0, "spirited":0.0, "celebratory":0.0, "romantic":0.4},
    "spirited":    {"happy":0.7, "chill":0.1, "intense":0.5, "relaxed":0.1, "moody":0.1, "focused":0.2, "melancholic":0.0, "playful":0.6, "nostalgic":0.1, "dreamy":0.3, "triumphant":0.6, "wistful":0.0, "yearning":0.0, "spirited":1.0, "celebratory":0.8, "romantic":0.3},
    "celebratory": {"happy":0.8, "chill":0.0, "intense":0.4, "relaxed":0.0, "moody":0.0, "focused":0.0, "melancholic":0.0, "playful":0.7, "nostalgic":0.0, "dreamy":0.2, "triumphant":0.5, "wistful":0.0, "yearning":0.0, "spirited":0.8, "celebratory":1.0, "romantic":0.2},
    "romantic":    {"happy":0.5, "chill":0.3, "intense":0.0, "relaxed":0.4, "moody":0.3, "focused":0.2, "melancholic":0.2, "playful":0.3, "nostalgic":0.3, "dreamy":0.7, "triumphant":0.0, "wistful":0.3, "yearning":0.4, "spirited":0.3, "celebratory":0.2, "romantic":1.0},
}

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
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
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
    # TODO: Implement scoring and ranking logic
    # Expected return format: (song_dict, score, explanation)
    return []
