from typing import Any, Dict, List, Tuple

import streamlit as st
from frontend.components._helpers import render_html

from frontend.components._helpers import safe_html


SEVERITY_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def _collect_action_items(analysis: Dict[str, Any]) -> List[Tuple[str, str, str]]:
    items: List[Tuple[str, str, str]] = []
    for issue in analysis.get("detailed_feedback") or []:
        level = (issue.get("severity_level") or "low").lower()
        title = issue.get("issue_title", "")
        for action in issue.get("action_items") or []:
            items.append((level, title, action))
    if not items:
        items.extend(("medium", "General improvement", item) for item in analysis.get("suggestions") or [])
    items.sort(key=lambda row: SEVERITY_RANK.get(row[0], 99))
    return items


def display_action_items(analysis: Dict[str, Any]) -> None:
    items = _collect_action_items(analysis)
    if not items:
        return

    rendered = []
    for index, (level, source, action) in enumerate(items, start=1):
        priority = "Urgent" if level in ("critical", "high") else "Next step"
        rendered.append(
            f"""
            <div class="action-item">
                <div class="action-number">{index:02d}</div>
                <div><strong>{safe_html(action)}</strong><p>{safe_html(source)}</p></div>
                <span class="priority">{priority}</span>
            </div>
            """
        )

    render_html(
        f"""
        <div class="section-heading">
            <h3>Your improvement plan</h3>
            <p>Concrete next steps, sorted by the urgency returned by the analysis.</p>
        </div>
        <div class="action-plan">{''.join(rendered)}</div>
        """,
        unsafe_allow_html=True,
    )
