from typing import Any, Dict, Optional

import streamlit as st
from frontend.components._helpers import render_html

from frontend.components._helpers import clamp, render_chips, safe_html


def display_jd_comparison(jd_comparison: Optional[Dict[str, Any]]) -> None:
    if not jd_comparison:
        return

    match_pct = clamp(jd_comparison.get("match_percentage", 0))
    semantic = clamp(float(jd_comparison.get("semantic_similarity", 0)) * 100)
    matched = jd_comparison.get("matched_keywords", []) or []
    missing = jd_comparison.get("missing_keywords", []) or []
    gap = jd_comparison.get("skills_gap", []) or []

    render_html(
        """
        <div class="section-heading">
            <h3>Job description match</h3>
            <p>Compare your resume with the target role to see where evidence is strong and where it is missing.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_html(
        f"""
        <div class="jd-stat-grid">
            <div class="skill-stat"><strong>{match_pct:.0f}%</strong><span>Job match</span></div>
            <div class="skill-stat"><strong>{semantic:.0f}%</strong><span>Semantic similarity</span></div>
            <div class="skill-stat"><strong>{len(missing)}</strong><span>Missing keywords</span></div>
        </div>
        <div class="surface" style="margin-bottom:0.95rem;">
            <div class="score-grid-label" style="margin-bottom:0.5rem;">Overall match</div>
            <div class="progress-track"><div class="progress-fill info" style="width:{match_pct:.1f}%"></div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns(2)
    with left:
        render_html(
            f"""
            <section class="surface">
                <h4 class="surface-title">Matched keywords</h4>
                <p class="muted-copy">Terms already represented in the resume.</p>
                <div class="tag-list">{render_chips(matched, "success", 15)}</div>
            </section>
            """,
            unsafe_allow_html=True,
        )
    with right:
        render_html(
            f"""
            <section class="surface">
                <h4 class="surface-title">Missing keywords</h4>
                <p class="muted-copy">Terms to address only when they reflect your real experience.</p>
                <div class="tag-list">{render_chips(missing, "warning", 15)}</div>
            </section>
            """,
            unsafe_allow_html=True,
        )

    render_html(
        f"""
        <section class="surface" style="margin-top:0.95rem;">
            <h4 class="surface-title">Skills gap</h4>
            <p class="muted-copy">Areas where stronger evidence may improve the comparison.</p>
            <div class="tag-list">{render_chips(gap, "danger", 12)}</div>
        </section>
        """,
        unsafe_allow_html=True,
    )
