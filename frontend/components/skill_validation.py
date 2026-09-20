from typing import Any, Dict

import streamlit as st
from frontend.components._helpers import render_html

from frontend.components._helpers import clamp, safe_html


def display_skill_validation(analysis: Dict[str, Any]) -> None:
    details = analysis.get("skill_validation_details") or {}
    validated = details.get("validated", []) or []
    unvalidated = details.get("unvalidated", []) or []
    total = details.get("total", len(validated) + len(unvalidated))
    validated_count = details.get("validated_count", len(validated))
    pct = clamp(details.get("validation_pct", 0))

    render_html(
        """
        <div class="section-heading">
            <h3>Skill validation</h3>
            <p>See which listed skills are supported by evidence in the resume.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not total:
        render_html('<div class="surface empty-note">No skills were detected on the resume.</div>', unsafe_allow_html=True)
        return

    render_html(
        f"""
        <div class="skill-stat-grid">
            <div class="skill-stat"><strong>{int(total)}</strong><span>Total skills</span></div>
            <div class="skill-stat"><strong>{int(validated_count)}</strong><span>Validated</span></div>
            <div class="skill-stat"><strong>{pct:.0f}%</strong><span>Validation rate</span></div>
        </div>
        <div class="surface" style="margin-bottom:0.95rem;">
            <div class="score-grid-label" style="margin-bottom:0.5rem;">Evidence coverage</div>
            <div class="progress-track"><div class="progress-fill success" style="width:{pct:.1f}%"></div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    validated_html = []
    for entry in validated:
        skill = safe_html(entry.get("skill", "Unknown skill"))
        projects = entry.get("projects", []) or []
        supporting_text = ", ".join(str(item) for item in projects[:3]) if projects else "experience section"
        similarity = entry.get("similarity")
        if isinstance(similarity, (int, float)):
            supporting_text += f" · {float(similarity) * 100:.0f}% match"
        validated_html.append(
            f'<div class="skill-item"><strong>{skill}</strong><span>Validated in {safe_html(supporting_text)}</span></div>'
        )

    unvalidated_html = [
        f'<div class="skill-item"><strong>{safe_html(skill)}</strong><span>Needs supporting evidence</span></div>'
        for skill in unvalidated
    ]

    left, right = st.columns(2)
    with left:
        render_html(
            f"""
            <section class="surface">
                <h4 class="surface-title">Validated skills</h4>
                <p class="muted-copy">Skills connected to projects or experience.</p>
                <div class="skill-list">{''.join(validated_html) or '<p class="empty-note">None detected</p>'}</div>
            </section>
            """,
            unsafe_allow_html=True,
        )
    with right:
        render_html(
            f"""
            <section class="surface">
                <h4 class="surface-title">Skills needing evidence</h4>
                <p class="muted-copy">Listed skills without clear supporting evidence.</p>
                <div class="skill-list">{''.join(unvalidated_html) or '<p class="empty-note">All listed skills have evidence.</p>'}</div>
            </section>
            """,
            unsafe_allow_html=True,
        )
