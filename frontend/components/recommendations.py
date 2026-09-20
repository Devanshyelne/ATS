from typing import Any, Dict

import streamlit as st
from frontend.components._helpers import render_html

from frontend.components._helpers import safe_html


def display_recommendations(analysis: Dict[str, Any]) -> None:
    suggestions = analysis.get("suggestions") or []
    if not suggestions:
        return

    items = "".join(
        f'<li>{safe_html(suggestion)}</li>' for suggestion in suggestions
    )
    render_html(
        f"""
        <div class="section-heading">
            <h3>Recommended next steps</h3>
            <p>Use the feedback to make focused improvements before applying.</p>
        </div>
        <section class="surface">
            <ul class="check-list">{items}</ul>
        </section>
        """,
        unsafe_allow_html=True,
    )
