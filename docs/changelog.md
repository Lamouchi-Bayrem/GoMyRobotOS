# Changelog

All notable changes to GoMyRobotOS are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
GoMyRobotOS has not produced software releases yet - it is at milestone **M0**
(Architecture and Contract Freeze). This changelog therefore tracks
documentation and specification changes.

## [Unreleased]

### Added

* **M0 documentation baseline**: Sphinx + MyST documentation site
  (`docs/`) published to Read the Docs and built by GitHub Actions.
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
  `partition.capabilities_required` - all additive; the three
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
* CI runners pinned to Ubuntu 26.04 LTS in
  `.github/workflows/docs.yml` and `.github/workflows/gh-pages.yml`
  (GitHub-hosted runners still publish `ubuntu-26.04` as preview;
  Ubuntu 24.04 LTS remains the stable fallback). `.readthedocs.yaml`
  keeps `ubuntu-24.04` - the latest LTS currently documented by
  Read the Docs.
* GitHub Pages moved to the official Actions deployment model
  (`actions/upload-pages-artifact` + `actions/deploy-pages`) in
  `.github/workflows/gh-pages.yml`: the site is now deployed through
  the Pages infrastructure (Settings → Pages → Source: GitHub
  Actions) and no longer pushed to a `gh-pages` branch.

### Fixed

* Architecture doc fixes: Guard/Sim restored in the stack diagram,
  target-matrix status label, section 1 heading level, WorldGuard
  spelling, watchdog classification (fault indicator, not an
  environmental fault class), legacy `nano-ros` naming note.
* M0 milestone page deliverable count ("seven" to "five").
* One remaining em dash in `docs/_static/custom.css`.
