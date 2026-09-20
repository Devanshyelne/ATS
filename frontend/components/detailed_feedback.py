from typing import Any, Dict, List

import streamlit as st
from frontend.components._helpers import render_html

from frontend.components._helpers import get_severity_style, safe_html


SEVERITY_ORDER = ["critical", "high", "medium", "low"]


def _group_by_severity(issues: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    grouped: Dict[str, List[Dict[str, Any]]] = {level: [] for level in SEVERITY_ORDER}
    for issue in issues:
        level = (issue.get("severity_level") or "low").lower()
        grouped.setdefault(level, []).append(issue)
    return grouped


def _render_issue(issue: Dict[str, Any], index: int) -> None:
    severity = (issue.get("severity_level") or "low").lower()
    severity_label, text_color, _ = get_severity_style(severity)
    title = safe_html(issue.get("issue_title", "Untitled issue"))
    impact = safe_html(issue.get("ats_impact", ""))
    render_html(
        f"""
        <article class="feedback-card severity-{safe_html(severity)}">
            <div class="feedback-head">
                <h4>{title}</h4>
                <span class="severity-label" style="color:{text_color};">{safe_html(severity_label)}</span>
            </div>
            <div class="muted-copy">ATS impact: {impact or 'Not specified'}</div>
        </article>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("View details", expanded=False):
        explanation = issue.get("explanation", "")
        where = issue.get("where_it_appears", "")
        how_to_fix = issue.get("how_to_fix", "")
        actions = issue.get("action_items") or []
        example = issue.get("example_improvement", "")
        if explanation:
            render_html(f'<div class="detail-label">What is happening</div><p class="detail-copy">{safe_html(explanation)}</p>', unsafe_allow_html=True)
        if where:
            render_html(f'<div class="detail-label">Where it appears</div><p class="detail-copy">{safe_html(where)}</p>', unsafe_allow_html=True)
        if how_to_fix:
            render_html(f'<div class="detail-label">How to fix it</div><p class="detail-copy">{safe_html(how_to_fix)}</p>', unsafe_allow_html=True)
        if actions:
            render_html('<div class="detail-label">Action items</div>', unsafe_allow_html=True)
            render_html('<ul class="check-list">' + "".join(f"<li>{safe_html(item)}</li>" for item in actions) + '</ul>', unsafe_allow_html=True)
        if example:
            render_html(f'<div class="detail-label">Example improvement</div><pre class="detail-copy">{safe_html(example)}</pre>', unsafe_allow_html=True)


def display_detailed_feedback(analysis: Dict[str, Any]) -> None:
    issues = analysis.get("detailed_feedback") or []
    if not issues:
        return

    render_html(
        f"""
        <div class="section-heading">
            <h3>Detailed feedback</h3>
            <p>{len(issues)} item(s) grouped by severity. Open an item to see context and a concrete fix.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    grouped = _group_by_severity(issues)
    index = 0
    for level in SEVERITY_ORDER:
        items = grouped.get(level, [])
        if not items:
            continue
        render_html(f'<div class="eyebrow" style="margin:1rem 0 0.55rem;">{level.title()} · {len(items)}</div>', unsafe_allow_html=True)
        for issue in items:
            _render_issue(issue, index)
            index += 1
