import math
import os
import re
from typing import Any, Callable, Dict, List, Optional, Tuple

from similarity_matrices import GENRE_SIMILARITY, MOOD_SIMILARITY
from llm_client import GeminiClient

DEFAULT_WEIGHTS: Dict[str, float] = {
    "genre":        0.15,
    "mood":         0.20,
    "energy":       0.20,
    "valence":      0.15,
    "danceability": 0.15,
    "acousticness": 0.15,
}

SCORE_THRESHOLD = 0.8


class Agent:
    """
    Agentic recommendation workflow (single pass):

    1. PLAN  — log scoring weights
    2. ACT   — score and rank the song catalog
    3. CHECK — accept if top score >= threshold; otherwise call Gemini once
               to suggest improvements to score_song() and log its response.
    """

    def __init__(self, client: Optional[GeminiClient] = None) -> None:
        self.logs: List[Dict[str, str]] = []
        self._gemini = client

    def run(
        self,
        user_prefs: Dict[str, Any],
        songs: List[Dict[str, Any]],
        k: int = 5,
        threshold: float = SCORE_THRESHOLD,
    ) -> Dict[str, Any]:
        self.logs = []

        # --- PLAN ---
        self._log("PLAN", f"Weights: {self._fmt_weights(DEFAULT_WEIGHTS)}")

        # --- ACT ---
        recommendations = self._score_and_rank(user_prefs, songs, k)
        top_score = recommendations[0][1] if recommendations else 0.0
        self._log("ACT", f"Top score: {top_score:.3f}  threshold: {threshold}")

        # --- CHECK ---
        if top_score >= threshold:
            self._log("CHECK", f"Accepted — {top_score:.3f} >= {threshold}.")
        else:
            self._log("CHECK", f"Score {top_score:.3f} < {threshold}. Asking Gemini for improvements.")
            if self._gemini:
                new_fn = self._ask_gemini(user_prefs, recommendations, threshold)
                if new_fn:
                    recommendations = self._score_and_rank(user_prefs, songs, k, score_fn=new_fn)
                    top_score = recommendations[0][1] if recommendations else 0.0
                    self._log("CHECK", f"Revised top score after applying Gemini's scorer: {top_score:.3f}")
            else:
                self._log("CHECK", "No Gemini client available.")

        return {
            "recommendations": recommendations,
            "passed_threshold": top_score >= threshold,
            "logs": self.logs,
        }

    # -------------------------
    # Gemini integration
    # -------------------------

    def _ask_gemini(
        self,
        user_prefs: Dict,
        recommendations: List[Tuple],
        threshold: float,
    ) -> Optional[Callable]:
        """Ask Gemini for an improved score_song(), compile it, and return it as a callable."""
        recommender_path = os.path.join(os.path.dirname(__file__), "recommender.py")
        with open(recommender_path) as f:
            current_code = f.read()

        top_recs = "\n".join(
            f"  {i+1}. {song['title']} (score={score:.3f}, genre={song['genre']}, "
            f"energy={song['energy']}, valence={song['valence']})"
            for i, (song, score, _) in enumerate(recommendations[:3])
        )

        prompt = (
            f"USER PROFILE:\n{user_prefs}\n\n"
            f"CURRENT SCORING WEIGHTS: {DEFAULT_WEIGHTS}\n\n"
            f"TOP RECOMMENDATIONS (all scored below the {threshold} threshold):\n{top_recs}\n\n"
            "CURRENT RECOMMENDER CODE:\n"
            f"```python\n{current_code}\n```\n\n"
            f"The top recommendation score ({recommendations[0][1]:.3f}) is below the required "
            f"threshold ({threshold}). Rewrite score_song(user_prefs, song) to better match this "
            "user profile. Rules:\n"
            "- Signature must stay: score_song(user_prefs: Dict, song: Dict) -> Tuple[float, str]\n"
            "- You may use `math`, `GENRE_SIMILARITY`, and `MOOD_SIMILARITY` (all already in scope).\n"
            "- Return ONLY the complete Python function definition. "
            "No markdown fences, no imports, no explanation."
        )

        self._log("CHECK", "Asking Gemini for an improved score_song()...")
        raw = self._gemini.complete(  # type: ignore[union-attr]
            system_prompt="You are improving a music recommendation engine written in Python.",
            user_prompt=prompt,
        )

        if not raw:
            self._log("CHECK", "Gemini returned an empty response.")
            return None

        fn_code = self._extract_function(raw, "score_song")
        if not fn_code:
            self._log("CHECK", f"Gemini responded but no function found. Raw:\n{raw}")
            return None

        self._log("CHECK", f"Gemini suggested:\n{fn_code}")
        namespace: Dict[str, Any] = {
            "math": math,
            "GENRE_SIMILARITY": GENRE_SIMILARITY,
            "MOOD_SIMILARITY": MOOD_SIMILARITY,
            # typing symbols Gemini may use in annotations
            "Dict": Dict, "List": List, "Tuple": Tuple,
            "Any": Any, "Optional": Optional,
        }
        try:
            exec(fn_code, namespace)  # noqa: S102
            fn = namespace.get("score_song")
            if callable(fn):
                self._log("CHECK", "Compiled successfully. Applying to scorer.")
                return fn
        except Exception as e:
            self._log("CHECK", f"Failed to compile Gemini's function: {e}")
        return None

    def _extract_function(self, text: str, fn_name: str) -> Optional[str]:
        text = re.sub(r"```(?:python)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"```", "", text)
        match = re.search(rf"(def {fn_name}\b[\s\S]+?)(?=\ndef |\Z)", text)
        if match:
            return match.group(1).rstrip()
        return None

    # -------------------------
    # Scoring
    # -------------------------

    def _score_and_rank(
        self,
        user_prefs: Dict[str, Any],
        songs: List[Dict[str, Any]],
        k: int,
        score_fn: Optional[Callable] = None,
    ) -> List[Tuple]:
        scored = []
        for song in songs:
            if score_fn:
                try:
                    scored.append((song, *score_fn(user_prefs, song)))
                except Exception:
                    scored.append((song, 0.0, "scoring error"))
            else:
                scored.append((song, *self._score_song(user_prefs, song)))
        return sorted(scored, key=lambda x: x[1], reverse=True)[:k]

    def _score_song(
        self,
        user_prefs: Dict[str, Any],
        song: Dict[str, Any],
    ) -> Tuple[float, str]:
        genre_score    = GENRE_SIMILARITY.get(user_prefs["genre"], {}).get(song["genre"], 0.0)
        energy_score   = math.exp(-5 * (song["energy"]       - user_prefs["energy"])       ** 2)
        valence_score  = math.exp(-5 * (song["valence"]      - user_prefs["valence"])      ** 2)
        dance_score    = math.exp(-5 * (song["danceability"] - user_prefs["danceability"]) ** 2)
        acoustic_score = math.exp(-5 * (song["acousticness"] - user_prefs["acousticness"]) ** 2)

        overall = (
            DEFAULT_WEIGHTS["genre"]        * genre_score   +
            DEFAULT_WEIGHTS["energy"]       * energy_score  +
            DEFAULT_WEIGHTS["valence"]      * valence_score +
            DEFAULT_WEIGHTS["danceability"] * dance_score   +
            DEFAULT_WEIGHTS["acousticness"] * acoustic_score
        )
        explanation = (
            f"genre={genre_score:.2f}, energy={energy_score:.2f}, "
            f"valence={valence_score:.2f}, danceability={dance_score:.2f}, "
            f"acousticness={acoustic_score:.2f}"
        )
        return overall, explanation

    # -------------------------
    # Utilities
    # -------------------------

    def _fmt_weights(self, weights: Dict[str, float]) -> str:
        return ", ".join(f"{k}={v:.2f}" for k, v in weights.items())

    def _log(self, step: str, message: str) -> None:
        self.logs.append({"step": step, "message": message})
