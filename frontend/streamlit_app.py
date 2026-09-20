import sys
from pathlib import Path

import streamlit as st


sys.path.insert(0, str(Path(__file__).parent.parent))
from frontend.components._helpers import render_html
from frontend.components.layout import render_footer

st.set_page_config(
    page_title="ATS Resume Scorer",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


for key, default in [
    ("access_token", None),
    ("refresh_token", None),
    ("user_id", None),
    ("user_email", None),
    ("auth_error", None),
    ("auth_info", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default


if not st.session_state.access_token and "code" in st.query_params:
    from frontend.services import supabase_client

    result = supabase_client.exchange_code_for_session(st.query_params["code"])
    st.query_params.clear()
    if "error" in result:
        st.session_state.auth_error = f"Google sign-in failed: {result['error']}"
    else:
        st.session_state.access_token = result["access_token"]
        st.session_state.refresh_token = result["refresh_token"]
        st.session_state.user_id = result["user_id"]
        st.session_state.user_email = result["email"]
        st.rerun()


def load_css() -> str:
    css_path = Path(__file__).parent / "assets" / "styles.css"
    try:
        return f"<style>{css_path.read_text()}</style>"
    except FileNotFoundError:
        return ""


render_html(load_css(), unsafe_allow_html=True)

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

if st.session_state.dark_mode:
    render_html(
        """
        <style>
            :root {
                --ink: #f8fafc; --ink-soft: #cbd5e1; --muted: #94a3b8; --muted-light: #64748b;
                --canvas: #0b1120; --surface: #111827; --surface-soft: #172033;
                --line: #263449; --line-strong: #3b4a62; --brand-soft: #202653;
                --success-soft: #0d2d1b; --warning-soft: #35220d; --danger-soft: #351517; --info-soft: #13264a;
            }
            .stApp, [data-testid="stSidebar"] { background: var(--canvas) !important; color: var(--ink); }
            [data-testid="stSidebar"] { border-color: var(--line); }
            .hero-shell { border-color: #303b64; background: linear-gradient(135deg, #111827 0%, #171c3b 68%, #102c38 100%); }
            .hero-panel, .hero-meta span, .value-item { border-color: var(--line); background: rgba(17, 24, 39, 0.8); }
            .score-ring::after { background: var(--surface); }
            .stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] > div { background: var(--surface); color: var(--ink); }
            [data-testid="stFileUploader"] section { border-color: var(--line-strong); background: var(--surface-soft); }
            .stButton > button, .stLinkButton > a, .stDownloadButton > button { background: var(--surface); color: var(--ink-soft); }
            .stButton > button:hover, .stLinkButton > a:hover, .stDownloadButton > button:hover { background: var(--brand-soft); color: #c7d2fe; }
            .stApp p, .stApp li, .stApp label { color: var(--ink-soft); }
            .chip { background: var(--surface-soft); color: var(--ink-soft); }
            .chip-success { border-color: #166534; background: var(--success-soft); color: #bbf7d0; }
            .chip-warning { border-color: #92400e; background: var(--warning-soft); color: #fed7aa; }
            .chip-danger { border-color: #991b1b; background: var(--danger-soft); color: #fecaca; }
            .file-ready { border-color: #166534; background: var(--success-soft); color: #bbf7d0; }
            .priority { background: var(--warning-soft); color: #fed7aa; }
            .preview-shell, .closing-cta { border-color: #303b64; background: linear-gradient(135deg, #111827 0%, #171c3b 100%); }
            .preview-card { border-color: var(--line); background: var(--surface); }
            .preview-ring { border-right-color: #334155; }
        </style>
        """,
        unsafe_allow_html=True,
    )

if "current_view" not in st.session_state:
    st.session_state.current_view = "landing"


def _navigate(view: str) -> None:
    st.session_state.current_view = view
    st.rerun()


with st.sidebar:
    render_html(
        """
        <div class="sidebar-brand">
            <div class="brand-mark">A</div>
            <div><div class="brand-name">ATS Resume Scorer</div><div class="brand-caption">Career intelligence workspace</div></div>
        </div>
        <div class="sidebar-section-label">Workspace</div>
        """,
        unsafe_allow_html=True,
    )

    nav_items = [("landing", "⌂  Home"), ("scorer", "◈  ATS Scorer"), ("history", "◷  History"), ("resources", "▤  Resources")]
    for view, label in nav_items:
        active_label = f"●  {label.split('  ', 1)[-1]}" if st.session_state.current_view == view else label
        if st.button(active_label, use_container_width=True, key=f"nav_{view}"):
            _navigate(view)

    st.toggle("Dark mode", key="dark_mode", help="Switch between the light and dark product themes.")

    render_html('<div class="sidebar-section-label">Account</div>', unsafe_allow_html=True)
    from frontend.services import supabase_client

    if st.session_state.access_token:
        render_html(
            f'<div class="sidebar-account"><div class="sidebar-label" style="margin-bottom:0.35rem;">Signed in</div><div class="sidebar-account-email">{st.session_state.user_email}</div></div>',
            unsafe_allow_html=True,
        )
        if st.button("Sign out", use_container_width=True, key="sign_out"):
            supabase_client.sign_out()
            for key in ("access_token", "refresh_token", "user_id", "user_email"):
                st.session_state[key] = None
            st.rerun()
    else:
        render_html(
            '<div class="auth-intro"><h3>Welcome back</h3><p>Sign in to analyze resumes and access your saved history.</p></div>',
            unsafe_allow_html=True,
        )
        if st.session_state.auth_error:
            st.error(st.session_state.auth_error)
            st.session_state.auth_error = None
        if st.session_state.auth_info:
            st.info(st.session_state.auth_info)
            st.session_state.auth_info = None

        tab_in, tab_up = st.tabs(["Sign in", "Create account"])
        with tab_in:
            with st.form("signin_form", clear_on_submit=False):
                email = st.text_input("Email", key="signin_email")
                password = st.text_input("Password", type="password", key="signin_pw")
                submitted = st.form_submit_button("Sign in", use_container_width=True)
            if submitted:
                result = supabase_client.sign_in_with_password(email, password)
                if "error" in result:
                    st.session_state.auth_error = result["error"]
                else:
                    st.session_state.access_token = result["access_token"]
                    st.session_state.refresh_token = result["refresh_token"]
                    st.session_state.user_id = result["user_id"]
                    st.session_state.user_email = result["email"]
                st.rerun()

        with tab_up:
            with st.form("signup_form", clear_on_submit=False):
                email_up = st.text_input("Email", key="signup_email")
                password_up = st.text_input("Password (min 6 chars)", type="password", key="signup_pw")
                submitted_up = st.form_submit_button("Create account", use_container_width=True)
            if submitted_up:
                result = supabase_client.sign_up_with_password(email_up, password_up)
                if "error" in result:
                    st.session_state.auth_error = result["error"]
                elif result.get("pending_confirmation"):
                    st.session_state.auth_info = f"Check your inbox — confirmation email sent to {result['email']}."
                else:
                    st.session_state.access_token = result["access_token"]
                    st.session_state.refresh_token = result["refresh_token"]
                    st.session_state.user_id = result["user_id"]
                    st.session_state.user_email = result["email"]
                st.rerun()

        render_html('<div style="text-align:center;margin:0.8rem 0;color:#94a3b8;font-size:0.75rem;">or</div>', unsafe_allow_html=True)
        oauth = supabase_client.google_oauth_url()
        if "error" in oauth:
            st.caption(f"Google sign-in unavailable: {oauth['error']}")
        else:
            st.link_button("Continue with Google", url=oauth["url"], use_container_width=True)


if st.session_state.current_view == "landing":
    from frontend.views import landing
    landing.render()
elif st.session_state.current_view == "scorer":
    from frontend.views import scorer
    scorer.render()
elif st.session_state.current_view == "history":
    from frontend.views import history
    history.render()
elif st.session_state.current_view == "resources":
    from frontend.views import resources
    resources.render()

render_footer()
