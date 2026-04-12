from typing import Dict

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

# Genre similarity matrix — binary match values (0.0–1.0).
# Based on production style, instrumentation, tempo, and emotional tone.
# Expanded from the genre table in documentation.md to cover all 17 genres in the dataset.
GENRE_SIMILARITY: Dict[str, Dict[str, float]] = {
    "ambient":    {"ambient":1.0, "blues":0.1, "classical":0.6, "country":0.0, "folk":0.2, "hip hop":0.0, "indie pop":0.1, "jazz":0.5, "latin":0.1, "lofi":0.7, "metal":0.0, "pop":0.0, "r&b":0.0, "reggae":0.2, "rock":0.0, "synthwave":0.2, "world":0.4},
    "blues":      {"ambient":0.1, "blues":1.0, "classical":0.2, "country":0.5, "folk":0.3, "hip hop":0.2, "indie pop":0.2, "jazz":0.5, "latin":0.1, "lofi":0.2, "metal":0.2, "pop":0.2, "r&b":0.6, "reggae":0.1, "rock":0.4, "synthwave":0.0, "world":0.1},
    "classical":  {"ambient":0.6, "blues":0.2, "classical":1.0, "country":0.1, "folk":0.3, "hip hop":0.0, "indie pop":0.1, "jazz":0.4, "latin":0.2, "lofi":0.5, "metal":0.1, "pop":0.0, "r&b":0.0, "reggae":0.0, "rock":0.0, "synthwave":0.0, "world":0.3},
    "country":    {"ambient":0.0, "blues":0.5, "classical":0.1, "country":1.0, "folk":0.7, "hip hop":0.0, "indie pop":0.2, "jazz":0.1, "latin":0.1, "lofi":0.2, "metal":0.0, "pop":0.2, "r&b":0.1, "reggae":0.2, "rock":0.2, "synthwave":0.0, "world":0.3},
    "folk":       {"ambient":0.2, "blues":0.3, "classical":0.3, "country":0.7, "folk":1.0, "hip hop":0.0, "indie pop":0.3, "jazz":0.2, "latin":0.2, "lofi":0.4, "metal":0.0, "pop":0.1, "r&b":0.0, "reggae":0.1, "rock":0.1, "synthwave":0.0, "world":0.4},
    "hip hop":    {"ambient":0.0, "blues":0.2, "classical":0.0, "country":0.0, "folk":0.0, "hip hop":1.0, "indie pop":0.2, "jazz":0.1, "latin":0.3, "lofi":0.1, "metal":0.0, "pop":0.4, "r&b":0.7, "reggae":0.2, "rock":0.0, "synthwave":0.1, "world":0.1},
    "indie pop":  {"ambient":0.1, "blues":0.2, "classical":0.1, "country":0.2, "folk":0.3, "hip hop":0.2, "indie pop":1.0, "jazz":0.4, "latin":0.1, "lofi":0.3, "metal":0.0, "pop":0.8, "r&b":0.2, "reggae":0.0, "rock":0.2, "synthwave":0.3, "world":0.1},
    "jazz":       {"ambient":0.5, "blues":0.5, "classical":0.4, "country":0.1, "folk":0.2, "hip hop":0.1, "indie pop":0.4, "jazz":1.0, "latin":0.3, "lofi":0.6, "metal":0.0, "pop":0.2, "r&b":0.3, "reggae":0.1, "rock":0.1, "synthwave":0.1, "world":0.3},
    "latin":      {"ambient":0.1, "blues":0.1, "classical":0.2, "country":0.1, "folk":0.2, "hip hop":0.3, "indie pop":0.1, "jazz":0.3, "latin":1.0, "lofi":0.0, "metal":0.0, "pop":0.3, "r&b":0.3, "reggae":0.5, "rock":0.0, "synthwave":0.1, "world":0.5},
    "lofi":       {"ambient":0.7, "blues":0.2, "classical":0.5, "country":0.2, "folk":0.4, "hip hop":0.1, "indie pop":0.3, "jazz":0.6, "latin":0.0, "lofi":1.0, "metal":0.0, "pop":0.1, "r&b":0.0, "reggae":0.0, "rock":0.0, "synthwave":0.3, "world":0.1},
    "metal":      {"ambient":0.0, "blues":0.2, "classical":0.1, "country":0.0, "folk":0.0, "hip hop":0.0, "indie pop":0.0, "jazz":0.0, "latin":0.0, "lofi":0.0, "metal":1.0, "pop":0.0, "r&b":0.0, "reggae":0.0, "rock":0.6, "synthwave":0.1, "world":0.0},
    "pop":        {"ambient":0.0, "blues":0.2, "classical":0.0, "country":0.2, "folk":0.1, "hip hop":0.4, "indie pop":0.8, "jazz":0.2, "latin":0.3, "lofi":0.1, "metal":0.0, "pop":1.0, "r&b":0.5, "reggae":0.1, "rock":0.3, "synthwave":0.6, "world":0.1},
    "r&b":        {"ambient":0.0, "blues":0.6, "classical":0.0, "country":0.1, "folk":0.0, "hip hop":0.7, "indie pop":0.2, "jazz":0.3, "latin":0.3, "lofi":0.0, "metal":0.0, "pop":0.5, "r&b":1.0, "reggae":0.2, "rock":0.1, "synthwave":0.1, "world":0.1},
    "reggae":     {"ambient":0.2, "blues":0.1, "classical":0.0, "country":0.2, "folk":0.1, "hip hop":0.2, "indie pop":0.0, "jazz":0.1, "latin":0.5, "lofi":0.0, "metal":0.0, "pop":0.1, "r&b":0.2, "reggae":1.0, "rock":0.1, "synthwave":0.0, "world":0.5},
    "rock":       {"ambient":0.0, "blues":0.4, "classical":0.0, "country":0.2, "folk":0.1, "hip hop":0.0, "indie pop":0.2, "jazz":0.1, "latin":0.0, "lofi":0.0, "metal":0.6, "pop":0.3, "r&b":0.1, "reggae":0.1, "rock":1.0, "synthwave":0.4, "world":0.0},
    "synthwave":  {"ambient":0.2, "blues":0.0, "classical":0.0, "country":0.0, "folk":0.0, "hip hop":0.1, "indie pop":0.3, "jazz":0.1, "latin":0.1, "lofi":0.3, "metal":0.1, "pop":0.6, "r&b":0.1, "reggae":0.0, "rock":0.4, "synthwave":1.0, "world":0.0},
    "world":      {"ambient":0.4, "blues":0.1, "classical":0.3, "country":0.3, "folk":0.4, "hip hop":0.1, "indie pop":0.1, "jazz":0.3, "latin":0.5, "lofi":0.1, "metal":0.0, "pop":0.1, "r&b":0.1, "reggae":0.5, "rock":0.0, "synthwave":0.0, "world":1.0},
}