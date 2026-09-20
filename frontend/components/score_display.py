from typing import Any, Dict

import streamlit as st
from frontend.components._helpers import render_html

from frontend.components._helpers import clamp, safe_html, score_status


COMPONENTS = [
    ("Formatting", "formatting", 20),
    ("Keywords & Skills", "keywords", 25),
    ("Content Quality", "content", 25),
    ("Skill Validation", "skill_validation", 15),
    ("ATS Compatibility", "ats_compatibility", 15),
]


def display_overall_score(analysis: Dict[str, Any]) -> None:
    score = clamp(analysis.get("ATS_score", analysis.get("ats_score", 0)))
    interpretation = safe_html(analysis.get("interpretation", ""))
    status, tone = score_status(score)
    angle = score * 3.6

    render_html(
        f"""
        <section class="score-card">
            <div class="score-card-label">Overall ATS score</div>
            <div class="score-ring-wrap">
                <div class="score-ring" style="--score-angle:{angle:.1f}deg;">
                    <div class="score-ring-content">
                        <div class="score-number">{score:.0f}</div>
                        <div class="score-denom">out of 100</div>
                    </div>
                </div>
            </div>
            <div class="score-status tone-{tone}">{safe_html(status)}</div>
            <p class="score-interpretation">{interpretation or 'Review the breakdown below to see where your resume can improve.'}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def display_score_breakdown(analysis: Dict[str, Any]) -> None:
    component_scores = analysis.get("component_scores") or {}
    cards = []
    for label, key, maximum in COMPONENTS:
        value = clamp(component_scores.get(key, 0), 0, maximum)
        percentage = (value / maximum * 100) if maximum else 0
        tone = "success" if percentage >= 80 else "warning" if percentage >= 60 else "danger"
        cards.append(
            f"""
            <div class="metric-card">
                <div class="score-grid-label">{safe_html(label)}</div>
                <div class="score-grid-value">{value:.0f}<span class="score-grid-label"> / {maximum}</span></div>
                <div class="progress-track"><div class="progress-fill {tone}" style="width:{percentage:.1f}%"></div></div>
            </div>
            """
        )

    render_html(
        """
        <div class="section-heading">
            <h3>Score breakdown</h3>
            <p>Five signals contribute to the score returned by the analysis engine.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_html(f'<div class="score-grid">{"".join(cards)}</div>', unsafe_allow_html=True)
