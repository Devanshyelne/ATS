import streamlit as st
from frontend.components._helpers import render_html


def _go_to_scorer() -> None:
    st.session_state.current_view = "scorer"
    st.rerun()


def render() -> None:
    render_html(
        """
        <section class="hero-shell">
            <div class="hero-copy">
                <div class="eyebrow">AI-powered resume intelligence</div>
                <h1>Make your resume easier to <span>match</span> and easier to understand.</h1>
                <p>Analyze your resume across ATS compatibility, content quality, keywords, skills, and job-description fit — then turn the results into practical next steps.</p>
                <div class="hero-actions">
                    <span class="hero-action-note">Built for job seekers, students, and growing professionals</span>
                    <a class="hero-secondary" href="#how-it-works">See how it works</a>
                </div>
            </div>
            <div class="hero-panel">
                <div class="mini-score">
                    <div class="mini-score-mark">01</div>
                    <div><strong>Start with a clearer signal</strong><small>Upload a resume and see what recruiters and screening systems can find.</small></div>
                </div>
            </div>
        </section>
        """
    )

    _, center, _ = st.columns([1, 1.3, 1])
    with center:
        if st.button("Analyze my resume  →", use_container_width=True, type="primary", key="landing_analyze"):
            _go_to_scorer()

    render_html(
        """
        <div class="value-strip">
            <div class="value-item"><strong>Five scoring dimensions</strong><span>Formatting /20 · Keywords & Skills /25 · Content Quality /25</span></div>
            <div class="value-item"><strong>Evidence-led analysis</strong><span>Skill validation, JD comparison, and prioritized feedback</span></div>
            <div class="value-item"><strong>Secure account workflow</strong><span>Review saved analyses and remove them from History when needed</span></div>
        </div>
        <div class="section-heading">
            <h2>Everything you need to improve with confidence</h2>
            <p>A calm, structured view of the signals that shape resume performance.</p>
        </div>
        <div class="feature-grid">
            <article class="feature-card"><div class="feature-icon">A</div><h3>ATS Compatibility</h3><p>Evaluate structure and formatting signals that help automated systems parse your resume.</p></article>
            <article class="feature-card"><div class="feature-icon">K</div><h3>Keyword Match</h3><p>Understand the skills and terms your resume already communicates clearly.</p></article>
            <article class="feature-card"><div class="feature-icon">C</div><h3>Content Quality</h3><p>Surface content signals such as action verbs, achievements, and clarity.</p></article>
            <article class="feature-card"><div class="feature-icon">S</div><h3>Skill Validation</h3><p>Connect listed skills to projects and experience so your claims have context.</p></article>
            <article class="feature-card"><div class="feature-icon">J</div><h3>Job Description Match</h3><p>Compare your resume with a target role and identify meaningful gaps.</p></article>
            <article class="feature-card"><div class="feature-icon">→</div><h3>Actionable Feedback</h3><p>Move from a score to concrete improvements organized by priority.</p></article>
        </div>
        <section class="preview-shell">
            <div class="preview-copy"><div class="eyebrow">Sample result preview</div><h2>Know what to fix before you apply.</h2><p>A clear score is only the beginning. See the signals, evidence gaps, and next actions in one focused workspace.</p></div>
            <div class="preview-card">
                <div class="preview-card-top"><span>Overall ATS score</span><span class="preview-chip">Strong foundation</span></div>
                <div class="preview-score-row"><div class="preview-ring"><strong>84</strong><span>/ 100</span></div><div><strong class="preview-verdict">Ready to refine</strong><p>Strong structure with a few high-impact improvements.</p></div></div>
                <div class="preview-breakdown">
                    <div><span>Formatting</span><strong>17 / 20</strong></div>
                    <div><span>Keywords & Skills</span><strong>21 / 25</strong></div>
                    <div><span>Content Quality</span><strong>22 / 25</strong></div>
                    <div><span>Skill Validation</span><strong>13 / 15</strong></div>
                    <div><span>ATS Compatibility</span><strong>12 / 15</strong></div>
                </div>
            </div>
        </section>
        <div class="section-heading" id="how-it-works">
            <h2>A simple path to a stronger resume</h2>
            <p>Keep the process focused and easy to repeat as your resume evolves.</p>
        </div>
        <div class="steps-grid">
            <article class="step-card"><div class="step-number">01 / UPLOAD</div><h3>Choose your resume</h3><p>Upload a PDF, DOC, or DOCX file from the scorer page.</p></article>
            <article class="step-card"><div class="step-number">02 / ANALYZE</div><h3>Review the signals</h3><p>Let the existing analysis engine evaluate the resume and optional job description.</p></article>
            <article class="step-card"><div class="step-number">03 / IMPROVE</div><h3>Take the next step</h3><p>Use the score breakdown, evidence gaps, and recommendations to revise with intent.</p></article>
        </div>
        <section class="closing-cta"><div><div class="eyebrow">Ready when you are</div><h2>Turn your next application into a better signal.</h2><p>Upload your resume and start with a focused, evidence-led review.</p></div></section>
        """
    )

    _, cta, _ = st.columns([1, 1.3, 1])
    with cta:
        if st.button("Start an analysis  →", use_container_width=True, type="primary", key="landing_analyze_bottom"):
            _go_to_scorer()
