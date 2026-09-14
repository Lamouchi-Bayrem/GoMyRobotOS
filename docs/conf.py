# Sphinx configuration for the GoMyRobotOS documentation.
#
# Build locally:
#   python3 -m sphinx -b html docs docs/_build/html
#
# Design note: the theme and layout intentionally match docs.ros.org
# (stock Read-the-Docs theme plus the same content-width overlay), so
# the GoMyRobotOS documentation sits visually inside the same
# documentation ecosystem as ROS 2. This is a documentation-styling
# choice only; ROS 2 remains an external reference, and nothing here
# claims implemented ROS 2 support.

project = "GoMyRobotOS"
author = "The GoMyRobotOS Authors"
copyright = "2026, The GoMyRobotOS Authors"

# GoMyRobotOS is at milestone M0 (Architecture and Contract Freeze).
# No software release exists yet, so the version refers to the
# specification/documentation baseline.
version = "M0"
release = "M0"

language = "en"

extensions = [
    "myst_parser",
    "sphinx_copybutton",
]

# Same sidebar behavior as the control.ros.org documentation site
# (ros-controls/control.ros.org): every section is listed at the root of
# the toctree, the per-section tree collapses to the current branch, and
# only the logo is shown in the sidebar header.
html_theme_options = {
    "collapse_navigation": True,
    "sticky_navigation": True,
    "navigation_depth": -1,
    "logo_only": True,
    # Breadcrumb link target: "edit" -> the GitHub *edit* screen of the
    # exact source file of each page (default "blob" only shows the file).
    "vcs_pageview_mode": "edit",
}
pygments_style = "sphinx"
copybutton_exclude = ".linenos, .gp, .go"

html_theme = "sphinx_rtd_theme"
# Without this, Sphinx 7+ does not copy the project's _static/ directory
# at all - static assets (this site's custom.css and toc-tree.js) must be
# declared explicitly. (html_logo and html_js_files still reference them
# from the page; this makes the files actually ship.)
html_static_path = ["_static"]
# Intentionally empty: with a value set, Sphinx appends
# " - <html_title>" to every page's <title>, which put a dash in
# every browser tab. The empty value makes the tab exactly the
# page name; the site name still appears in the sidebar brand
# via `project`.
html_title = ""
html_logo = "_static/gomyrobotos-logo.svg"

# Content-width overlay, kept identical to the ROS 2 documentation
# site (docs.ros.org/_static/custom.css).
html_css_files = ["custom.css"]

# "View on GitHub" and "Edit on GitHub" links in the theme footer:
# every rendered page links to its own source file in the repository.
html_context = {
    "display_github": True,
    "github_user": "gomyrobot",
    "github_repo": "GoMyRobotOS",
    "github_version": "main",
    "conf_py_path": "/docs/",
}

exclude_patterns = ["Thumbs.db", ".DS_Store", "**/.DS_Store", "_build"]
