# Sphinx configuration for the GoMyRobotOS documentation.
#
# Build locally:
#   python3 -m sphinx -b html docs docs/_build/html

project = "GoMyRobotOS"
author = "GoMyRobot"
copyright = "2026, GoMyRobot"

# GoMyRobotOS is at milestone M0 (Architecture and Contract Freeze).
# No software release exists yet, so the version refers to the
# specification/documentation baseline.
version = "0.1.0"
release = "0.1.0 (M0: Architecture and Contract Freeze)"

extensions = [
    "myst_parser",
]

html_theme = "furo"
pygments_dark_style = "monokai"

html_title = "GoMyRobotOS Documentation"

exclude_patterns = ["Thumbs.db", ".DS_Store", "**/.DS_Store", "_build"]

# Deep-ish anchors on headings make cross-referencing ADRs and
# contract fields manageable.
myst_heading_anchors = 3
