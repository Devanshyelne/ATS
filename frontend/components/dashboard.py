from typing import Any, Dict

import streamlit as st
from frontend.components._helpers import render_html

from frontend.components.action_items import display_action_items
from frontend.components.detailed_feedback import display_detailed_feedback
from frontend.components.jd_comparison import display_jd_comparison
from frontend.components.recommendations import display_recommendations
from frontend.components.score_display import display_overall_score, display_score_breakdown
from frontend.components.skill_validation import display_skill_validation
from frontend.components.strengths_issues import display_critical_issues, display_strengths
from frontend.components._helpers import safe_html


def display_results_dashboard(analysis: Dict[str, Any]) -> None:
    """Render the structured backend response as a polished results dashboard."""
    render_html(
        """
        <div class="results-intro">
            <div>
                <div class="eyebrow">Analysis complete</div>
                <h2>Your resume snapshot</h2>
                <p>Review the score, then work through the highest-impact improvements first.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([0.8, 1.55])
    with left:
        display_overall_score(analysis)
    with right:
        interpretation = safe_html(analysis.get("interpretation", ""))
        strengths_count = len(analysis.get("strengths") or [])
        issue_count = len(analysis.get("critical_issues") or analysis.get("issues_summary") or [])
        render_html(
            f"""
            <section class="surface result-summary-card">
                <div class="eyebrow">Executive readout</div>
                <h3>What to focus on next</h3>
                <p>{interpretation or 'Use the score breakdown and feedback below to prioritize your next revision.'}</p>
                <div class="result-summary-stats">
                    <div><strong>{strengths_count}</strong><span>strengths found</span></div>
                    <div><strong>{issue_count}</strong><span>priority issues</span></div>
                </div>
            </section>
            """
        )

    render_html('<div style="height:0.5rem"></div>', unsafe_allow_html=True)
    display_score_breakdown(analysis)

    strengths, issues = st.columns(2)
    with strengths:
        display_strengths(analysis.get("strengths") or [])
    with issues:
        display_critical_issues(analysis)

    display_skill_validation(analysis)

    jd_comparison = analysis.get("jd_comparison") or analysis.get("jd_match_analysis")
    if jd_comparison:
        display_jd_comparison(jd_comparison)

    display_detailed_feedback(analysis)
    display_action_items(analysis)
    display_recommendations(analysis)
