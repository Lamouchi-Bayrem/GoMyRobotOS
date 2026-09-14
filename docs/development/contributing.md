# Contributing to GoMyRobotOS

GoMyRobotOS is an early-stage, documentation-first system: the
architecture and the Partition Contract are frozen as a specification
(milestone **M0**), and no target system has been implemented yet.

This page is the single contributing reference, the process, plus the
documentation-authoring contract every contribution to `docs/` must
honor (the enforceable extraction of the documentation policy).

## Development flow

1. Fork the repository and create a feature branch from `main`.
2. Keep changes scoped: one architecture concern per pull request.
3. Update the documentation in the same pull request that changes an
   ADR, a milestone definition, or the shape of the Partition Contract.
4. The documentation build (`docs/`) must pass with zero warnings:

   ```bash
   python3 -m venv .venv
   . .venv/bin/activate
   pip install -r docs/requirements.txt
   python -m sphinx -b html docs docs/_build/html
   ```

5. Open a pull request against `main`.

## Non-negotiable documentation rules

1. **Single source of truth.** The documentation sources under `docs/`
   are the primary source of truth. Do not invent architecture.
2. **Never invent.** Never introduce APIs, command-line tools,
   hardware support, hypervisor support, RTEMS/ROS 2 support claims,
   certification claims, safety properties, benchmark results, or
   timing results that the repository does not actually demonstrate.
3. **Use explicit maturity labels everywhere** (see *Status labels*
   below).
4. **No silent elevation.** An *architecture proposal* must never be
   written as an *implemented feature*, and a *research target* must
   never be written as a *supported platform* (see *Forbidden
   conversions* below).
5. **ROS 2 Rolling is the external authority** for all ROS 2 concepts
   (<https://docs.ros.org/en/rolling/>) (see *ROS 2 rules* below).
6. **Do not create documentation pages merely to fill the tree** (see
   *Page discipline* below).
7. **Milestones are M0-M6** (see *Milestones* below).

## Status labels: the vocabulary

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
* No GoMyRobot rebranding of ROS 2 concepts; never invent
  `GoMyRobotNode`, `GoMyRobotPublisher`, `GoMyRobotExecutor`-style
  substitutes for standard ROS 2 concepts.
* Distinguish "documentation reference" from "implemented support"
  ([compatibility/ros2]
  (../compatibility/ros2) is the living example).

## Architecture decisions (ADRs)

* New ADR = next free `ADR-NNNN` in
  [architecture-decisions]
  (architecture-decisions), with context / decision / consequence /
  status.
* No silent editing of an Accepted ADR, supersede it with a new ADR
  that references it.
* No renumbering of existing ADRs.
* A PR that changes architecture without an ADR should be sent back.

## Milestones

* Milestones are **M0-M6** in the [overview]
  (../milestones/overview). M7 does not exist; editors must not add
  it, rename it, or rescope a milestone page outside of the ADR process.

## Page discipline

* No page is created "to fill out the tree". Every page must carry content
  traceable to (a) the final architecture, (b) an ADR, or (c) a recorded
  milestone gate.
* Build hygiene: the doc build must pass with zero warnings
  (CI `docs` job, built with `-W` so any warning fails it).
* The toctree in [index.md](../index) reflects the structure, new
  pages must be added to a toctree or they are not part of the site.

## Code conventions

The first implementations land at **M1** (x86-64 reference partition:
parser, validator, IR, Xen backend, boot/deployment, basic partition
monitoring). Code-style conventions will be added to this document as
the first code lands. Until then, keep tool names, CLI flags, and
version claims out of the documentation.

## Reporting problems

* Architecture inconsistencies: file an issue referencing the
  conflicting documentation pages.
* Documentation build failures: detected automatically by the `docs`
  GitHub Action (`.github/workflows/docs.yml`), whose build runs with
  `-W`: any warning fails the workflow.

## License

Contributions are licensed under the Apache License 2.0, the same as
the rest of the repository.
