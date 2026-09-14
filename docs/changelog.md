# Changelog

All notable changes to GoMyRobotOS are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
GoMyRobotOS has not produced software releases yet, it is at milestone **M0**
(Architecture and Contract Freeze). This changelog therefore tracks
documentation and specification changes.

## [Unreleased]

### Added

* **M0 documentation baseline**: Sphinx + MyST documentation site
  (`docs/`) published to GitHub Pages and built by GitHub Actions.
* **Partition Contract v1**: conceptual field specification
  (`docs/contract/`), JSON Schema
  (`schemas/partition-contract.schema.json`), and illustrative examples per
  target (`examples/x86-64`, `examples/ng-ultra`, `examples/hpsc`).
* Milestone plan **M0-M6** and acceptance gates
  (`docs/milestones/`).
* ROS 2 Rolling compatibility reference
  (`docs/compatibility/ros2.md`).
* Root `README.md` (repository entry point) and all documentation
  sources under `docs/` (contributing guide and changelog included
  as site pages).
* **Contract v1 amendment** (ADR-0014, ADR-0015, ADR-0016, ADR-0017):
  IPC channel classes (`sampling` / `queuing`) with channel properties,
  `timing.wcet_bound_us` + `wcet_evidence_class`,
  `recovery.guard_independence_stage`, and
  `partition.capabilities_required`, all additive; the three
  illustrative examples stay in lockstep.
* Five architecture items selected from the reviewed v2 draft
  (ADR-0014 through ADR-0018): backend capability manifest and the
  no-silent-downgrade rule, IPC channel semantics, Guard independence
  staging, WCET evidence classification, and the space-fault
  responsibility split.
* `docs/architecture/frozen-baseline.md`: scope notes for the frozen
  baseline (naming rule, v1 exclusions, platform position).
* `docs/development/architecture-v2.md`: superseded-v2 pointer page
  recording what was taken from the draft and what was explicitly
  excluded.
* External product-page links (gomyrobot.com) for GoMyRobotRT,
  GoMyRobotGuard, GoMyRobotBSP, GoMyRobotAssure, GoMyRobotFault,
  GoMyRobotVerify, GoMyRobotBench, and GoMyRobotSecure references in the
  docs.

### Changed

* Visual parity with the ROS 2 documentation: `sphinx_rtd_theme`,
  64rem content width, copyable code buttons, `sphinx` Pygments style,
  `language="en"`.
* ASCII dash normalization: every en/em dash replaced by a plain ASCII
  hyphen across docs, examples, and schemas.
* The documentation site becomes the architecture source of truth: root
  `GoMyRobotOS.md` and `docs.md` removed, baseline scope notes folded
  into `docs/` (ADR-0018).
* ADR list extended: ADR-0001 through ADR-0018
  (`docs/development/architecture-decisions.md`).
* Documentation consolidated under a single folder: root
  `CONTRIBUTING.md` merged into `docs/development/contributing.md`
  (now the single contributing reference) and root `CHANGELOG.md`
  moved to `docs/changelog.md`; both are published in the
  `docs/index.md` toctree. Root `README.md` remains the GitHub
  entry point.
* GitHub Actions runners: `.github/workflows/gh-pages.yml` pinned to
  Ubuntu 24.04 LTS; `.github/workflows/docs.yml` pinned to Ubuntu
  26.04 LTS (still published as preview on GitHub-hosted runners;
  Ubuntu 24.04 LTS is the stable fallback).
* GitHub Pages moved to the official Actions deployment model
  (`actions/upload-pages-artifact` + `actions/deploy-pages`) in
  `.github/workflows/gh-pages.yml`: the site is now deployed through
  the Pages infrastructure (Settings → Pages → Source: GitHub
  Actions) and no longer pushed to a `gh-pages` branch.
* Every documentation page now carries a GitHub link in the breadcrumb
  that opens the edit screen of exactly that page's source file
  (`html_context` + `vcs_pageview_mode: edit`, repo
  `gomyrobot/GoMyRobotOS`, branch `main`, sources under `docs/`).
* Documentation home is the GitHub Pages site
  (<https://gomyrobot.github.io/GoMyRobotOS/>), the single published
  location (README and
  `docs/getting-started/installation.md` point at it).
* Read the Docs hosting has been retired for the documentation: `.readthedocs.yaml`
  is deleted, every "mirror" reference is removed (development
  environment table, project testing table, contributing and M0
  milestone checklists), and the host clause in ADR-0013 now names the
  GitHub Pages site. The GitHub Actions deployment
  (`.github/workflows/gh-pages.yml`) is the single published site.
* Sidebar navigation now behaves like the ROS 2 documentation: all
  sections are listed at once, and clicking a section (Getting
  started, Concepts, etc.) selects it and expands what is under it;
  sections not containing the page you are reading start collapsed
  and stay under user control. Implemented in the site's own
  `docs/_static/toc-tree.js` (+ `custom.css`), without touching the
  theme.
* Shipping fix: `html_static_path` is now declared in `docs/conf.py`.
  Without it, the project's `_static/` assets (the ROS 2
  content-width overlay and the new navigation script) were never
  copied into the build, even though the pages referenced them.
* Double-dash cleanup in `docs/architecture/backend-model.md`: the
  capability-check figure now uses the single-hyphen arrow style the
  rest of the diagram already uses (the 5-character left arrow became
  the 2-character one, and the double-segment fork frame became the
  single-segment form). No double-hyphen sequences remain in
  documentation prose, only structural markdown table-divider lines
  and section rules, plus the logo SVG's XML comment, are untouched.
* Browser tab titles now show exactly the page name: `html_title` is
  left empty in `docs/conf.py`, so the ", GoMyRobotOS Documentation"
  suffix (and its dash) no longer follows every page title in the tab
  bar; the sidebar brand still comes from `project` and is
  unaffected.

### Fixed

* Architecture doc fixes: Guard/Sim restored in the stack diagram,
  target-matrix status label, section 1 heading level, WorldGuard
  spelling, watchdog classification (fault indicator, not an
  environmental fault class), legacy `nano-ros` naming note.
* M0 milestone page deliverable count ("seven" to "five").
* One remaining em dash in `docs/_static/custom.css`.
