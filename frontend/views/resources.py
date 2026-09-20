import streamlit as st
from frontend.components._helpers import render_html


def render() -> None:
    render_html(
        """
        <div class="page-header">
            <div class="eyebrow">Resume playbook</div>
            <h1 class="page-title">Build a clearer, ATS-friendly resume</h1>
            <p class="page-lede">Practical guidance for writing a resume that is easy for screening systems to parse and easy for people to scan.</p>
        </div>
        <div class="section-heading" style="margin-top:0;">
            <h2>ATS essentials</h2>
            <p>Use these principles as a quick review before running another analysis.</p>
        </div>
        <div class="resource-grid">
            <article class="resource-card do-card"><div class="resource-kicker">Do</div><h3>Make the structure obvious</h3><p>Use standard section headings, explicit skills, and a simple layout.</p><ul class="resource-list"><li>Use standard section headings</li><li>List skills explicitly</li><li>Quantify achievements with numbers</li><li>Use readable fonts such as Arial, Calibri, or Times New Roman</li><li>Save as PDF or DOCX</li></ul></article>
            <article class="resource-card dont-card"><div class="resource-kicker">Avoid</div><h3>Reduce parsing friction</h3><p>Keep important content in the main document flow so it is not missed.</p><ul class="resource-list"><li>Avoid tables and text boxes</li><li>Keep important information out of headers and footers</li><li>Avoid images and graphics</li><li>Prefer a single-column layout</li><li>Do not keyword stuff</li></ul></article>
            <article class="resource-card"><div class="resource-kicker">Write with evidence</div><h3>Make every claim useful</h3><p>When you name a skill, connect it to a project, outcome, or responsibility that shows how you used it.</p><ul class="resource-list"><li>Lead bullets with strong action verbs</li><li>Explain the result, not only the task</li><li>Spell out abbreviations the first time</li></ul></article>
        </div>
        <div class="section-heading">
            <h2>Common keywords by industry</h2>
            <p>Use these as prompts while tailoring your resume to a real role.</p>
        </div>
        """
    )

    tech, business, creative = st.tabs(["Technology", "Business", "Creative"])
    with tech:
        render_html(
            """
            <section class="resource-tab-panel">
                <div class="resource-kicker">Technology</div><h3>Software development</h3><p>Programming languages, frameworks, tools, and delivery practices.</p>
                <div class="tag-list"><span class="chip chip-neutral">Python</span><span class="chip chip-neutral">JavaScript</span><span class="chip chip-neutral">React</span><span class="chip chip-neutral">Django</span><span class="chip chip-neutral">Git</span><span class="chip chip-neutral">Docker</span><span class="chip chip-neutral">Agile</span><span class="chip chip-neutral">CI/CD</span></div>
            </section>
            """
        )
    with business:
        render_html(
            """
            <section class="resource-tab-panel">
                <div class="resource-kicker">Business</div><h3>Management and operations</h3><p>Show how you coordinate people, priorities, budgets, and outcomes.</p>
                <div class="tag-list"><span class="chip chip-neutral">Project management</span><span class="chip chip-neutral">Stakeholder engagement</span><span class="chip chip-neutral">Budget management</span><span class="chip chip-neutral">Strategic planning</span><span class="chip chip-neutral">Team leadership</span></div>
            </section>
            """
        )
    with creative:
        render_html(
            """
            <section class="resource-tab-panel">
                <div class="resource-kicker">Creative</div><h3>Design and communication</h3><p>Make both craft and collaboration visible in the language you choose.</p>
                <div class="tag-list"><span class="chip chip-neutral">Adobe Creative Suite</span><span class="chip chip-neutral">UI/UX Design</span><span class="chip chip-neutral">Wireframing</span><span class="chip chip-neutral">Prototyping</span><span class="chip chip-neutral">Brand Identity</span></div>
            </section>
            """
        )

    render_html(
        """
        <div class="section-heading">
            <h2>Template library</h2>
            <p>The current product focuses on analysis and feedback. Downloadable templates can be added here in a future release.</p>
        </div>
        <div class="template-placeholder"><strong>Templates coming soon</strong><span>Use the analysis workflow to improve the resume you already have.</span></div>
        """
    )
