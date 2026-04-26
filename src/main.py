"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    pop_happy = {
        "name": "Pop Happy",
        "genre": "pop",
        "mood": "happy",
        "energy": 0.70,
        "valence": 0.90,
        "danceability": 0.80,
        "acousticness": 0.50
    }

    energetic_pop = {
        "name": "Energetic Pop",
        "genre": "pop",
        "mood": "intense",
        "energy": 1.00,
        "valence": 0.50,
        "danceability": 0.80,
        "acousticness": 0.50
    }

    chill_lofi = {
        "name": "Chill Lofi",
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.20,
        "valence": 0.50,
        "danceability": 0.20,
        "acousticness": 0.50
    }

    deep_intense_rock = {
        "name": "Deep Intense Rock",
        "genre": "rock",
        "mood": "intense",
        "energy": 1.00,
        "valence": 0.50,
        "danceability": 0.80,
        "acousticness": 0.50
    }

    undecided_listener = {
        "name": "Undecided Listener",
        "genre": "pop",
        "mood": "relaxed",
        "energy": 0.5,
        "valence": 0.5,
        "danceability": 0.5,
        "acousticness": 0.5
    }

    classical_intense = {
        "name": "Classical Intense",
        "genre": "classical",
        "mood": "intense",
        "energy": 0.9,
        "valence": 0.4,
        "danceability": 0.2,
        "acousticness": 0.95
    }

    all_maximums = {
        "name": "All Maximums",
        "genre": "hip hop",
        "mood": "spirited",
        "energy": 1.0,
        "valence": 1.0,
        "danceability": 1.0,
        "acousticness": 0.0
    }

    all_minimums = {
        "name": "All Minimums",
        "genre": "classical",
        "mood": "yearning",
        "energy": 0.0,
        "valence": 0.0,
        "danceability": 0.0,
        "acousticness": 1.0
    }

    high_energy_melancholic = {
        "name": "High Energy Melancholic",
        "genre": "metal",
        "mood": "melancholic",
        "energy": 0.95,
        "valence": 0.1,
        "danceability": 0.8,
        "acousticness": 0.02
    }

    low_energy_celebratory = {
        "name": "Low Energy Celebratory",
        "genre": "ambient",
        "mood": "celebratory",
        "energy": 0.1,
        "valence": 0.95,
        "danceability": 0.05,
        "acousticness": 0.95
    }

    profiles = [
        pop_happy,
        energetic_pop,
        chill_lofi,
        deep_intense_rock,
        undecided_listener,
        classical_intense,
        all_maximums,
        all_minimums,
        high_energy_melancholic,
        low_energy_celebratory
    ]

    for profile in profiles:
        recommendations = recommend_songs(profile, songs, k=5)

        print(f"\nTop recommendations for {profile["name"]}:\n")
        for rec in recommendations:
            # You decide the structure of each returned item.
            # A common pattern is: (song, score, explanation)
            song, score, explanation = rec
            print(f"{song['title']} - Score: {score:.2f}")
            print(f"Because: {explanation}")
            print()


if __name__ == "__main__":
    main()
