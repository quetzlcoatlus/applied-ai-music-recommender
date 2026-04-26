import math
from typing import Any, Dict, List, Tuple

from similarity_matrices import GENRE_SIMILARITY

DEFAULT_WEIGHTS: Dict[str, float] = {
    "genre":        0.19,
    "energy":       0.24,
    "valence":      0.19,
    "danceability": 0.19,
    "acousticness": 0.19,
}

SCORE_THRESHOLD = 0.5
MAX_RETRIES = 3
# How much genre weight to shed per retry, redistributed equally to numeric features.
GENRE_WEIGHT_STEP = 0.05


class Agent:
    """
    Agentic recommendation workflow:

    1. PLAN  — set (or adjust) scoring weights
    2. ACT   — score and rank the song catalog
    3. CHECK — accept if top score >= threshold; otherwise shed genre weight and retry
    """

    def __init__(self) -> None:
        self.logs: List[Dict[str, str]] = []

    def run(
        self,
        user_prefs: Dict[str, Any],
        songs: List[Dict[str, Any]],
        k: int = 5,
        threshold: float = SCORE_THRESHOLD,
        max_retries: int = MAX_RETRIES,
    ) -> Dict[str, Any]:
        self.logs = []
        weights = dict(DEFAULT_WEIGHTS)
        recommendations: List[Tuple[Dict, float, str]] = []
        top_score = 0.0

        for attempt in range(1, max_retries + 2):
            # --- PLAN ---
            self._log("PLAN", f"Attempt {attempt}: {self._fmt_weights(weights)}")

            # --- ACT ---
            recommendations = self._score_and_rank(user_prefs, songs, weights, k)
            top_score = recommendations[0][1] if recommendations else 0.0
            self._log("ACT", f"Top score: {top_score:.3f}  threshold: {threshold}")

            # --- CHECK ---
            if top_score >= threshold:
                self._log("CHECK", f"Accepted — {top_score:.3f} >= {threshold}.")
                break

            if attempt > max_retries:
                self._log("CHECK", f"Returning best available after {max_retries} retries ({top_score:.3f} < {threshold}).")
                break

            # Refine: reduce genre weight, spread the difference across numeric features.
            reduction = min(GENRE_WEIGHT_STEP, weights["genre"])
            weights["genre"] -= reduction
            per_feature = reduction / 4
            for key in ("energy", "valence", "danceability", "acousticness"):
                weights[key] += per_feature
            self._log(
                "CHECK",
                f"Score {top_score:.3f} < {threshold}. Reducing genre weight by {reduction:.2f} and retrying.",
            )

        return {
            "recommendations": recommendations,
            "passed_threshold": top_score >= threshold,
            "logs": self.logs,
        }

    # -------------------------
    # Scoring
    # -------------------------

    def _score_and_rank(
        self,
        user_prefs: Dict[str, Any],
        songs: List[Dict[str, Any]],
        weights: Dict[str, float],
        k: int,
    ) -> List[Tuple[Dict, float, str]]:
        scored = [(song, *self._score_song(user_prefs, song, weights)) for song in songs]
        return sorted(scored, key=lambda x: x[1], reverse=True)[:k]

    def _score_song(
        self,
        user_prefs: Dict[str, Any],
        song: Dict[str, Any],
        weights: Dict[str, float],
    ) -> Tuple[float, str]:
        genre_score = GENRE_SIMILARITY.get(user_prefs["genre"], {}).get(song["genre"], 0.0)
        energy_score       = math.exp(-5 * (song["energy"]       - user_prefs["energy"])       ** 2)
        valence_score      = math.exp(-5 * (song["valence"]      - user_prefs["valence"])      ** 2)
        danceability_score = math.exp(-5 * (song["danceability"] - user_prefs["danceability"]) ** 2)
        acousticness_score = math.exp(-5 * (song["acousticness"] - user_prefs["acousticness"]) ** 2)

        overall = (
            weights["genre"]        * genre_score +
            weights["energy"]       * energy_score +
            weights["valence"]      * valence_score +
            weights["danceability"] * danceability_score +
            weights["acousticness"] * acousticness_score
        )
        explanation = (
            f"genre={genre_score:.2f}, energy={energy_score:.2f}, "
            f"valence={valence_score:.2f}, danceability={danceability_score:.2f}, "
            f"acousticness={acousticness_score:.2f}"
        )
        return overall, explanation

    # -------------------------
    # Utilities
    # -------------------------

    def _fmt_weights(self, weights: Dict[str, float]) -> str:
        return ", ".join(f"{k}={v:.2f}" for k, v in weights.items())

    def _log(self, step: str, message: str) -> None:
        self.logs.append({"step": step, "message": message})
