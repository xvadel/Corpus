"""
Corpus — User Skill Model
===========================
Persists concept-level mastery scores per user in SQLite.

Schema
------
concept_mastery(user_id TEXT, concept_id TEXT, score REAL, attempts INT,
                last_seen TEXT, PRIMARY KEY (user_id, concept_id))

Score semantics
---------------
0.0 – 0.39  : unseen / no exposure
0.4 – 0.59  : introduced
0.6 – 0.79  : practiced
0.8 – 1.0   : mastered

Score updates use an exponential moving average so recent interactions
weigh more than distant ones without fully discarding past performance.
"""

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DB_PATH = PROJECT_ROOT / "corpus_data" / "user_skills.db"

EMA_ALPHA = 0.4   # weight of new score vs. existing score
MASTERY_THRESHOLD = 0.80


def _conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(DB_PATH))
    con.row_factory = sqlite3.Row
    con.execute("""
        CREATE TABLE IF NOT EXISTS concept_mastery (
            user_id    TEXT NOT NULL,
            concept_id TEXT NOT NULL,
            score      REAL NOT NULL DEFAULT 0.0,
            attempts   INTEGER NOT NULL DEFAULT 0,
            last_seen  TEXT NOT NULL,
            PRIMARY KEY (user_id, concept_id)
        )
    """)
    con.commit()
    return con


class UserSkillModel:
    """
    Persistent per-user concept mastery store.

    All score values are in [0.0, 1.0]. Scores are updated via an exponential
    moving average so recency matters but history is not discarded.
    """

    # ──────────────────────────────────────────────────────────────────────
    # Reads
    # ──────────────────────────────────────────────────────────────────────

    def get_score(self, user_id: str, concept_id: str) -> float:
        """Return mastery score for a single concept (0.0 if never seen)."""
        with _conn() as con:
            row = con.execute(
                "SELECT score FROM concept_mastery WHERE user_id=? AND concept_id=?",
                (user_id, concept_id)
            ).fetchone()
        return float(row["score"]) if row else 0.0

    def get_all_scores(self, user_id: str) -> Dict[str, float]:
        """Return {concept_id: score} for every concept the user has interacted with."""
        with _conn() as con:
            rows = con.execute(
                "SELECT concept_id, score FROM concept_mastery WHERE user_id=?",
                (user_id,)
            ).fetchall()
        return {r["concept_id"]: float(r["score"]) for r in rows}

    def get_mastered_concepts(self, user_id: str) -> List[str]:
        """Return concept IDs where score >= MASTERY_THRESHOLD."""
        with _conn() as con:
            rows = con.execute(
                "SELECT concept_id FROM concept_mastery WHERE user_id=? AND score>=?",
                (user_id, MASTERY_THRESHOLD)
            ).fetchall()
        return [r["concept_id"] for r in rows]

    def get_known_concept_ids(self, user_id: str, threshold: float = 0.4) -> List[str]:
        """Return concept IDs where the user has at least minimal exposure."""
        with _conn() as con:
            rows = con.execute(
                "SELECT concept_id FROM concept_mastery WHERE user_id=? AND score>=?",
                (user_id, threshold)
            ).fetchall()
        return [r["concept_id"] for r in rows]

    # ──────────────────────────────────────────────────────────────────────
    # Writes
    # ──────────────────────────────────────────────────────────────────────

    def record_interaction(
        self,
        user_id: str,
        concept_id: str,
        performance: float
    ) -> float:
        """
        Update mastery for a concept after an interaction.

        Args:
            user_id:     Authenticated user identifier.
            concept_id:  The concept interacted with.
            performance: Interaction quality in [0.0, 1.0].
                         - 1.0 for a correct answer / quiz pass
                         - 0.5 for partial understanding / reading
                         - 0.0 for incorrect / skipped

        Returns:
            New mastery score after update.
        """
        if not (0.0 <= performance <= 1.0):
            raise ValueError(f"performance must be in [0.0, 1.0], got {performance!r}")

        now = datetime.now(timezone.utc).isoformat()
        with _conn() as con:
            row = con.execute(
                "SELECT score, attempts FROM concept_mastery WHERE user_id=? AND concept_id=?",
                (user_id, concept_id)
            ).fetchone()

            if row:
                old_score = float(row["score"])
                new_score = EMA_ALPHA * performance + (1 - EMA_ALPHA) * old_score
                new_attempts = row["attempts"] + 1
                con.execute(
                    """UPDATE concept_mastery
                       SET score=?, attempts=?, last_seen=?
                       WHERE user_id=? AND concept_id=?""",
                    (new_score, new_attempts, now, user_id, concept_id)
                )
            else:
                # First interaction — seed with performance directly
                new_score = performance
                con.execute(
                    """INSERT INTO concept_mastery (user_id, concept_id, score, attempts, last_seen)
                       VALUES (?, ?, ?, 1, ?)""",
                    (user_id, concept_id, new_score, now)
                )
        return new_score

    def bulk_record(
        self,
        user_id: str,
        interactions: List[Dict]
    ) -> Dict[str, float]:
        """
        Record multiple interactions at once.

        interactions: [{"concept_id": str, "performance": float}, ...]
        Returns:      {concept_id: new_score}
        """
        results = {}
        for item in interactions:
            results[item["concept_id"]] = self.record_interaction(
                user_id, item["concept_id"], item["performance"]
            )
        return results

    def reset_user(self, user_id: str) -> None:
        """Delete all mastery records for a user (useful for testing / account reset)."""
        with _conn() as con:
            con.execute("DELETE FROM concept_mastery WHERE user_id=?", (user_id,))

    # ──────────────────────────────────────────────────────────────────────
    # Summaries
    # ──────────────────────────────────────────────────────────────────────

    def get_profile_summary(self, user_id: str) -> Dict:
        """Return a structured summary of the user's overall skill profile."""
        all_scores = self.get_all_scores(user_id)
        mastered   = [cid for cid, s in all_scores.items() if s >= MASTERY_THRESHOLD]
        practiced  = [cid for cid, s in all_scores.items() if 0.6 <= s < MASTERY_THRESHOLD]
        introduced = [cid for cid, s in all_scores.items() if 0.4 <= s < 0.6]

        return {
            "user_id":         user_id,
            "total_concepts":  len(all_scores),
            "mastered_count":  len(mastered),
            "practiced_count": len(practiced),
            "introduced_count":len(introduced),
            "mastered":        mastered,
            "practiced":       practiced,
            "introduced":      introduced,
            "average_score":   (sum(all_scores.values()) / len(all_scores)) if all_scores else 0.0
        }
