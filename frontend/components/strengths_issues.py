from typing import Any, Dict, List

import streamlit as st
from frontend.components._helpers import render_html

from frontend.components._helpers import safe_html


def _items(items: List[str], issue: bool = False) -> str:
    if not items:
        return '<p class="empty-note">No items were returned for this section.</p>'
    css = "check-list issue-list" if issue else "check-list"
    return f'<ul class="{css}">' + "".join(
        f"<li>{safe_html(item)}</li>" for item in items
    ) + "</ul>"


def display_strengths(strengths: List[str]) -> None:
    render_html(
        f"""
        <section class="list-card">
            <h3>What is working</h3>
            <p>Signals that are already helping your resume perform well.</p>
            {_items(strengths)}
        </section>
        """,
        unsafe_allow_html=True,
    )


def display_critical_issues(analysis: Dict[str, Any]) -> None:
    critical = analysis.get("critical_issues") or []
    summary = analysis.get("issues_summary") or []
    extra = [item for item in summary if item not in critical]
    all_issues = list(critical) + extra

    if not all_issues:
        render_html(
            """
            <section class="list-card">
                <h3>No priority issues found</h3>
                <p>Your analysis did not return any urgent issues for this resume.</p>
                <div class="file-ready">Review the detailed feedback below for further opportunities.</div>
            </section>
            """,
            unsafe_allow_html=True,
        )
        return

    render_html(
        f"""
        <section class="list-card">
            <h3>Priority issues</h3>
            <p>{len(all_issues)} item(s) need attention before your next application.</p>
            {_items(all_issues, issue=True)}
        </section>
        """,
        unsafe_allow_html=True,
    )
