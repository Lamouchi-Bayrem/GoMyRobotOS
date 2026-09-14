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

extensions = [
    "myst_parser",
]

html_theme = "sphinx_rtd_theme"
html_title = "GoMyRobotOS Documentation"
html_logo = "_static/gomyrobotos-logo.svg"

# Content-width overlay, kept identical to the ROS 2 documentation
# site (docs.ros.org/_static/custom.css).
html_css_files = ["custom.css"]

exclude_patterns = ["Thumbs.db", ".DS_Store", "**/.DS_Store", "_build"]
