import requests
import streamlit as st
from frontend.components._helpers import render_html

from frontend.components._helpers import format_date, safe_html, to_float
from frontend.services import api_client


def _show_backend_error(exc: Exception) -> None:
    if isinstance(exc, requests.ConnectionError):
        st.error("Could not reach the history service. Check that the backend is running on port 8000.")
    elif isinstance(exc, requests.Timeout):
        st.error("The history service took too long to respond. Try again in a moment.")
    elif isinstance(exc, requests.HTTPError) and exc.response is not None:
        st.error(f"The history service returned {exc.response.status_code}: {exc.response.text}")
    else:
        st.error(f"Unexpected error: {exc}")


def _open_analysis(analysis: dict) -> None:
    st.session_state["scorer_analysis"] = analysis
    st.session_state.current_view = "scorer"
    st.rerun()


def render() -> None:
    render_html(
        """
        <div class="page-header">
            <div class="eyebrow">Your workspace</div>
            <h1 class="page-title">Analysis history</h1>
            <p class="page-lede">Review previous resume analyses and return to a detailed result whenever you need it.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    access_token = st.session_state.get("access_token")
    if not access_token:
        render_html(
            '<div class="auth-gate"><h3>Sign in to view your history</h3><p>Your saved analyses are available after authentication through the existing account flow.</p></div>',
            unsafe_allow_html=True,
        )
        return

    try:
        history = api_client.get_history(access_token)
    except requests.RequestException as exc:
        _show_backend_error(exc)
        return

    if not history:
        render_html(
            '<div class="empty-state"><h3>No analyses yet</h3><p>Your resume insights will appear here after your first analysis.</p></div>',
            unsafe_allow_html=True,
        )
        _, center, _ = st.columns([1, 1.2, 1])
        with center:
            if st.button("Analyze your resume  →", use_container_width=True, type="primary", key="history_empty_scorer"):
                st.session_state.current_view = "scorer"
                st.rerun()
        return

    scores = [to_float(entry.get("ats_score"), 0.0) for entry in history]
    latest_score = scores[0] if scores else 0.0
    best_score = max(scores) if scores else 0.0
    render_html(
        f"""
        <div class="history-summary-grid">
            <div class="history-summary-item"><span>Total analyses</span><strong>{len(history)}</strong></div>
            <div class="history-summary-item"><span>Best score</span><strong>{best_score:.0f}<small> / 100</small></strong></div>
            <div class="history-summary-item"><span>Latest score</span><strong>{latest_score:.0f}<small> / 100</small></strong></div>
        </div>
        """
    )

    for index, entry in enumerate(history):
        filename = entry.get("filename", "resume")
        ats_score = to_float(entry.get("ats_score"), 0.0)
        created_at = format_date(entry.get("created_at", ""))
        analysis = entry.get("analysis_result", {}) or {}
        component_scores = analysis.get("component_scores", {}) or {}
        jd_comparison = analysis.get("jd_comparison") or analysis.get("jd_match_analysis")
        entry_id = str(entry.get("id") or index)
        pdf_key = f"history_pdf_{entry_id}"

        jd_value = f"{float(jd_comparison.get('match_percentage', 0)):.0f}%" if jd_comparison else "—"
        render_html(
            f"""
            <article class="history-card">
                <div class="history-main">
                    <div class="history-file"><strong>{safe_html(filename)}</strong><span>Analyzed {safe_html(created_at)}</span></div>
                    <div class="history-score">{ats_score:.0f}<span style="font-size:0.72rem;color:#64748b;font-weight:600;"> / 100</span></div>
                </div>
                <div class="history-metrics">
                    <div class="history-metric"><span>Formatting</span><strong>{to_float(component_scores.get('formatting'), 0):.0f}/20</strong></div>
                    <div class="history-metric"><span>Keywords & Skills</span><strong>{to_float(component_scores.get('keywords'), 0):.0f}/25</strong></div>
                    <div class="history-metric"><span>Content Quality</span><strong>{to_float(component_scores.get('content'), 0):.0f}/25</strong></div>
                    <div class="history-metric"><span>Skill Validation</span><strong>{to_float(component_scores.get('skill_validation'), 0):.0f}/15</strong></div>
                    <div class="history-metric"><span>ATS Compatibility</span><strong>{to_float(component_scores.get('ats_compatibility'), 0):.0f}/15</strong></div>
                </div>
            </article>
            """,
            unsafe_allow_html=True,
        )

        view_col, pdf_col, delete_col = st.columns([1.1, 1.1, 0.8])
        with view_col:
            if st.button("View analysis", use_container_width=True, key=f"view_{entry_id}"):
                _open_analysis(analysis)
        with pdf_col:
            if st.button("Prepare PDF", use_container_width=True, key=f"pdf_{entry_id}"):
                try:
                    with st.spinner("Preparing PDF..."):
                        st.session_state[pdf_key] = api_client.get_history_pdf(entry_id, access_token)
                except requests.RequestException as exc:
                    _show_backend_error(exc)
        with delete_col:
            if st.button("Delete", use_container_width=True, key=f"delete_{index}"):
                try:
                    api_client.delete_history_entry(entry_id, access_token)
                    st.rerun()
                except requests.RequestException as exc:
                    _show_backend_error(exc)

        if pdf_key in st.session_state:
            st.download_button(
                "Download PDF",
                data=st.session_state[pdf_key],
                file_name=f"ats_report_{entry_id}.pdf",
                mime="application/pdf",
                use_container_width=True,
                key=f"download_history_pdf_{entry_id}",
            )
