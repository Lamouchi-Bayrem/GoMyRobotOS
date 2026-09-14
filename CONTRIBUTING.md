# Contributing to GoMyRobotOS

Thank you for contributing to GoMyRobotOS. This project is an early-stage,
documentation-first system: the architecture and the Partition Contract are frozen
as a specification (milestone **M0**), and no target system has been implemented yet.

## Development flow

1. Fork the repository and create a feature branch from `main`.
2. Keep changes scoped: one architecture concern per pull request.
3. Update the documentation in the same pull request that changes an ADR, a
   milestone definition, or the shape of the Partition Contract.
4. The documentation build (`docs/`) must pass:

   ```bash
   python3 -m venv .venv
   . .venv/bin/activate
   pip install -r docs/requirements.txt
   python -m sphinx -b html docs docs/_build/html
   ```

5. Open a pull request against `main`.

## Non-negotiable documentation rules

These rules apply to every contribution, including prose, schemas, and
examples:

1. **Single source of truth.** The documentation sources in this
   repository (under `docs/`) are the primary source of truth. Do not
   invent architecture.
2. **Never invent.** Never introduce APIs, command-line tools, hardware support,
   hypervisor support, RTEMS/ROS 2 support claims, certification claims, safety
   properties, benchmark results, or timing results that the repository does not
   actually demonstrate.
3. **Use explicit maturity labels everywhere:**

   ```text
   Stable | Experimental | Research | Planned | Not implemented
   ```

4. **No silent elevation.** An *architecture proposal* must never be written as an
   *implemented feature*, and a *research target* must never be written as a
   *supported platform*.
5. **ROS 2 Rolling is the external authority** for all ROS 2 concepts
   (<https://docs.ros.org/en/rolling/>). Link to Rolling; never duplicate ROS 2
   documentation; never invent GoMyRobot-flavored replacements for standard
   ROS 2 concepts (`GoMyRobotNode`, `GoMyRobotPublisher`, `GoMyRobotExecutor`…).
6. **Do not create documentation pages merely to fill the tree.** Pages must
   contain meaningful content, and the content must be traceable to the Final
   Architecture or to a recorded Architecture Decision.
7. **Milestones are M0-M6.** Do not create M7 unless a future architecture
   decision establishes a separate milestone.

## Architecture decisions

Architectural changes are made through Architecture Decision Records (ADRs) in
`docs/development/architecture-decisions.md`:

* New decisions get the next free `ADR-NNNN` number.
* An accepted ADR is never rewritten silently; supersede it with a new ADR that
  references it.
* A PR that changes architecture without an ADR should be sent back.

## Code conventions

The first implementations land at **M1** (x86-64 reference partition: parser,
validator, IR, Xen backend, boot/deployment, basic partition monitoring).
Code-style conventions will be added to this document as the first code lands.
Until then, keep tool names, CLI flags, and version claims out of the
documentation.

## Reporting problems

* Architecture inconsistencies: file an issue referencing the conflicting
  documentation pages.
* Documentation build failures: issues are detected automatically by the
  `docs` GitHub Action (`.github/workflows/docs.yml`).

## License

Contributions are licensed under the Apache License 2.0, the same as the rest
of the repository.
