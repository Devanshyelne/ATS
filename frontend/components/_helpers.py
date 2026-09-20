from datetime import datetime
from html import escape
from textwrap import dedent
from typing import Any, Iterable, Tuple

import streamlit as st


def render_html(markup: str, **_: Any) -> None:
    """Render an HTML fragment without letting indentation create code blocks."""
    normalized = dedent(str(markup)).strip()
    normalized = "\n".join(
        line.lstrip() for line in normalized.splitlines() if line.strip()
    )
    st.markdown(normalized, unsafe_allow_html=True)


def get_score_color(score: float) -> Tuple[str, str]:
    """Return the semantic text/background colors for a 0–100 score."""
    if score >= 80:
        return "#15803d", "#ecfdf3"
    if score >= 60:
        return "#b45309", "#fff7ed"
    return "#b91c1c", "#fef2f2"


def get_score_emoji(score: float) -> str:
    """Legacy compatibility helper; the redesigned UI uses semantic labels."""
    if score >= 80:
        return "Strong"
    if score >= 60:
        return "Developing"
    return "Needs attention"


def get_severity_style(severity: str) -> Tuple[str, str, str]:
    """Return (label, text color, background color) for an issue severity."""
    level = (severity or "").lower()
    if level in ("critical", "high"):
        return "High priority", "#b91c1c", "#fef2f2"
    if level == "medium":
        return "Medium priority", "#b45309", "#fff7ed"
    return "Low priority", "#15803d", "#ecfdf3"


def safe_html(value: Any) -> str:
    """Escape backend-provided text before placing it in an HTML card."""
    # These values are inserted into element text, not HTML attributes. Avoid
    # encoding apostrophes so they cannot surface as visible HTML entity text if
    # a browser or Markdown renderer displays the fragment verbatim.
    return escape(str(value or ""), quote=False)


def to_float(value: Any, default: float = 0.0) -> float:
    """Coerce optional API values for display without crashing the UI."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def score_status(score: float) -> Tuple[str, str]:
    """Return a concise score label and CSS tone name."""
    if score >= 80:
        return "Strong foundation", "success"
    if score >= 60:
        return "On the right track", "warning"
    return "Needs attention", "danger"


def clamp(value: Any, minimum: float = 0.0, maximum: float = 100.0) -> float:
    """Clamp a display-only number without changing business calculations."""
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        numeric = minimum
    return max(minimum, min(maximum, numeric))


def format_date(value: Any) -> str:
    """Format API timestamps for the history view, with a safe fallback."""
    if not value:
        return "Date unavailable"
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return parsed.strftime("%b %-d, %Y")
    except (TypeError, ValueError):
        return str(value)


def render_chips(values: Iterable[Any], tone: str = "neutral", limit: int | None = None) -> str:
    """Build lightweight HTML chips for keyword and skill collections."""
    values = list(values or [])
    if limit is not None:
        values = values[:limit]
    if not values:
        return '<span class="empty-note">None detected</span>'
    return "".join(
        f'<span class="chip chip-{tone}">{safe_html(value)}</span>'
        for value in values
    )
