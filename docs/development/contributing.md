# Contributing (documentation version)

The root `CONTRIBUTING.md` file (repository root) is the process
reference. This page is the *documentation-authoring* contract everyone
contributing to `docs/` must honor - it is the enforceable extraction of
the [documentation policy]
(https://github.com/gomyrobot/GoMyRobotOS/blob/main/docs).

## Status labels - the vocabulary

Every non-trivial claim uses exactly one:

```text
Stable | Experimental | Research | Planned | Not implemented
```

+ composite forms allowed in contexts: `Development / Reference`,
`Flight Reference / Development` (platform roles). Ad-hoc synthesis of
maturity states is forbidden.

## Forbidden conversions (anti-hallucination)

* *architecture proposal* → *implemented feature*
* *research target* → *supported platform*
* *documented contract* → *demonstrated behavior*
* *QEMU fault model* → *radiation evidence*

If a change requires any of these, it must carry an ADR change with a
milestone gate number attached (e.g., "effective in M3"), or it must not
happen.

## ROS 2 rules

* Single external authority:
  [ROS 2 Rolling](https://docs.ros.org/en/rolling/).
* No reproduction of ROS 2 docs; no second conceptual model for ROS 2.
* No GoMyRobot rebranding of ROS 2 concepts.
* Distinguish "documentation reference" from "implemented support"
  ([compatibility/ros2]
  (../compatibility/ros2) is the living example).

## ADRs

* New ADR = next free `ADR-NNNN` in
  [architecture-decisions]
  (architecture-decisions), with context / decision / consequence /
  status.
* No silent editing of an Accepted ADR - supersede with a new number.
* No renumbering of existing ADRs.

## Milestones

* Milestones are **M0-M6** in the [overview]
  (../milestones/overview). M7 does not exist; editors must not add
  it, rename it, or rescope a milestone page outside of the ADR process.

## Page discipline

* No page is created "to fill out the tree". Every page must carry content
  traceable to (a) the final architecture, (b) an ADR, or (c) a recorded
  milestone gate.
* Build hygiene: the doc build must pass with zero warnings
  (CI `docs` job; Read the Docs `fail_on_warning: true`).
* The toctree in [index.md](../index) reflects the structure - new
  pages must be added to a toctree or they are not part of the site.
