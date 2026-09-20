from typing import Optional

import requests
import streamlit as st
from frontend.components._helpers import render_html

from frontend.components.dashboard import display_results_dashboard
from frontend.services import api_client


MAX_RESUME_BYTES = 5 * 1024 * 1024


def _read_jd(jd_file, jd_text: str) -> str:
    """Turn the supported JD inputs into the plain text expected by the API."""
    if jd_text:
        return jd_text.strip()
    if jd_file is None:
        return ""
    if jd_file.name.lower().endswith(".txt"):
        return jd_file.getvalue().decode("utf-8", errors="ignore").strip()
    st.warning("Job description files must be `.txt` for now — paste the JD text instead if you have a PDF or DOCX.")
    return ""


def _show_backend_error(exc: Exception) -> None:
    """Translate request failures into calm, actionable UI copy."""
    if isinstance(exc, requests.ConnectionError):
        st.error("Could not reach the analysis service. Check that the backend is running on port 8000.")
    elif isinstance(exc, requests.Timeout):
        st.error("The analysis service took too long to respond. Try a smaller resume or check the server logs.")
    elif isinstance(exc, requests.HTTPError) and exc.response is not None:
        try:
            detail = exc.response.json().get("detail", exc.response.text)
        except ValueError:
            detail = exc.response.text
        st.error(f"The analysis service returned {exc.response.status_code}: {detail}")
    else:
        st.error(f"Unexpected error: {exc}")


def _summary_text(analysis: dict) -> str:
    """Create the existing plain-text export without changing analysis meaning."""
    score = float(analysis.get("ATS_score", analysis.get("ats_score", 0)))
    lines = [f"ATS Score: {score:.0f}/100", ""]
    if analysis.get("strengths"):
        lines.extend(["STRENGTHS:", *(f"  - {item}" for item in analysis["strengths"]), ""])
    if analysis.get("critical_issues"):
        lines.extend(["PRIORITY ISSUES:", *(f"  - {item}" for item in analysis["critical_issues"]), ""])
    if analysis.get("suggestions"):
        lines.extend(["SUGGESTIONS:", *(f"  - {item}" for item in analysis["suggestions"])])
    return "\n".join(lines)


def _render_upload_area(analysis_mode: str):
    """Render the existing resume/JD widgets with presentation-only guidance."""
    left, right = st.columns(2)

    with left:
        with st.container(border=True):
            render_html(
                """
                <div class="section-heading" style="margin-top:0;">
                    <h3>Upload your resume</h3>
                    <p>PDF, DOC, or DOCX · maximum 5 MB</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            resume_file = st.file_uploader(
                "Drag and drop your file here, or choose a file",
                type=["pdf", "doc", "docx"],
                help="Supported: PDF, DOC, DOCX (max 5 MB)",
                key="resume_upload",
            )
            if resume_file:
                render_html(
                    f'<div class="file-ready"><strong>Ready</strong><span>{resume_file.name} · {resume_file.size / 1024:.1f} KB</span></div>',
                    unsafe_allow_html=True,
                )

    jd_file: Optional[object] = None
    jd_text = ""

    with right:
        with st.container(border=True):
            if analysis_mode == "Job Description Comparison":
                render_html(
                    """
                    <div class="section-heading" style="margin-top:0;">
                        <h3>Compare against a job description</h3>
                        <p>See what matches and which terms need stronger evidence.</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                jd_method = st.radio(
                    "Input method",
                    ["Paste text", "Upload .txt file"],
                    horizontal=True,
                    key="jd_input_method",
                )
                if jd_method == "Upload .txt file":
                    jd_file = st.file_uploader(
                        "Choose a JD file (.txt only)",
                        type=["txt"],
                        key="jd_upload",
                    )
                    if jd_file:
                        render_html(f'<div class="file-ready"><strong>Ready</strong><span>{jd_file.name}</span></div>', unsafe_allow_html=True)
                else:
                    jd_text = st.text_area(
                        "Paste the job description",
                        height=190,
                        placeholder="Paste the role description here...",
                        key="jd_text",
                    )
                    if jd_text:
                        render_html(f'<div class="file-ready"><strong>Ready</strong><span>{len(jd_text):,} characters</span></div>', unsafe_allow_html=True)
            else:
                render_html(
                    """
                    <div class="section-heading" style="margin-top:0;">
                        <h3>General ATS analysis</h3>
                        <p>Start with the resume alone and review its core scoring signals.</p>
                    </div>
                    <div class="surface" style="margin-top:1.2rem;">
                        <div class="surface-title">Want a targeted comparison?</div>
                        <p class="muted-copy">Switch to Job Description Comparison to add a role description.</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    return resume_file, jd_file, jd_text


def _render_export_buttons(analysis: dict) -> None:
    render_html(
        """
        <div class="section-heading">
            <h3>Export your report</h3>
            <p>Keep a shareable copy of the structured analysis.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Generate PDF report", use_container_width=True, type="primary", key="generate_pdf_report"):
            try:
                with st.spinner("Preparing your report..."):
                    pdf_bytes = api_client.generate_pdf(analysis, access_token=st.session_state["access_token"])
                st.session_state["scorer_pdf_bytes"] = pdf_bytes
            except requests.RequestException as exc:
                _show_backend_error(exc)
        if "scorer_pdf_bytes" in st.session_state:
            st.download_button(
                "Download PDF",
                data=st.session_state["scorer_pdf_bytes"],
                file_name="ats_resume_report.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="download_pdf_report",
            )
    with c2:
        st.download_button(
            "Download summary (.txt)",
            data=_summary_text(analysis),
            file_name="ats_summary.txt",
            mime="text/plain",
            use_container_width=True,
            key="download_summary",
        )


def render() -> None:
    render_html(
        """
        <div class="page-header">
            <div class="eyebrow">Career intelligence workspace</div>
            <h1 class="page-title">Resume analysis</h1>
            <p class="page-lede">See exactly where your resume performs well, where it needs evidence, and which improvements are worth making first.</p>
        </div>
        <div class="flow-steps">
            <div class="flow-step"><strong>01</strong><span>Choose mode</span></div>
            <div class="flow-step"><strong>02</strong><span>Upload resume</span></div>
            <div class="flow-step"><strong>03</strong><span>Review insights</span></div>
        </div>
        <div class="mode-shell"><div class="eyebrow" style="margin-bottom:0.4rem;">Choose an analysis mode</div></div>
        """,
        unsafe_allow_html=True,
    )

    analysis_mode = st.radio(
        "Analysis mode",
        ["General ATS Analysis", "Job Description Comparison"],
        horizontal=True,
        key="analysis_mode",
        label_visibility="collapsed",
    )

    resume_file, jd_file, jd_text = _render_upload_area(analysis_mode)

    if not resume_file:
        render_html(
            '<div class="auth-gate"><h3>Upload a resume to begin</h3><p>Your results will appear here after the analysis completes. You can keep this page open while you prepare a file.</p></div>',
            unsafe_allow_html=True,
        )
        if st.session_state.get("scorer_analysis"):
            display_results_dashboard(st.session_state["scorer_analysis"])
        return

    if resume_file.size > MAX_RESUME_BYTES:
        st.error("This file is larger than 5 MB. Choose a smaller resume file to continue.")
        return

    if not st.session_state.get("access_token"):
        render_html(
            '<div class="auth-gate"><h3>Sign in to run your analysis</h3><p>Your account is used to authorize the existing analysis and history endpoints.</p></div>',
            unsafe_allow_html=True,
        )
        return

    _, action_col, _ = st.columns([1, 1.2, 1])
    with action_col:
        analyze = st.button("Analyze resume  →", use_container_width=True, type="primary", key="analyze_resume")

    if not analyze:
        if st.session_state.get("scorer_analysis"):
            display_results_dashboard(st.session_state["scorer_analysis"])
            _render_export_buttons(st.session_state["scorer_analysis"])
        return

    st.session_state.pop("scorer_pdf_bytes", None)
    st.session_state.pop("scorer_analysis", None)
    job_description = _read_jd(jd_file, jd_text) if analysis_mode == "Job Description Comparison" else ""

    try:
        with st.spinner("Analyzing your resume · this may take a moment"):
            analysis = api_client.analyze_resume(
                resume_file=resume_file,
                access_token=st.session_state["access_token"],
                job_description=job_description,
            )
    except requests.RequestException as exc:
        _show_backend_error(exc)
        return

    st.session_state["scorer_analysis"] = analysis
    render_html('<div class="file-ready" style="margin:1.2rem 0;">Analysis complete. Your results are ready below.</div>', unsafe_allow_html=True)
    display_results_dashboard(analysis)
    _render_export_buttons(analysis)
