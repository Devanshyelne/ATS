from frontend.components._helpers import render_html


def render_footer() -> None:
    """Render the shared product credit at the end of every main view."""
    render_html(
        """
        <footer class="app-footer">
            <span>Created by Devansh Yelne</span>
            <span class="footer-separator">·</span>
            <span>© 2026</span>
            <a href="https://github.com/Devanshyelne" target="_blank" rel="noreferrer">GitHub</a>
        </footer>
        """
    )
