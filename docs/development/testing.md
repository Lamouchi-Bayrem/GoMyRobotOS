# Testing (project)

This page states the *project-level* testing story for the software that
will exist from M1 onward. As of M0, the only things that are tested are
the documentation build and the contract schema (both in CI today).

## What is tested today (M0)

| Check                       | Where                                |
| --------------------------- | ------------------------------------ |
| documentation builds cleanly | GitHub Actions `docs` job + Read the Docs (fail_on_warning) |
| example contracts validate   | GitHub Actions `schema` job (JSON Schema draft 2020-12) |

No software exists yet to be tested; the tables below are the committed
shape of the future, consistent with the
[milestones](../milestones/overview).

## Declared test areas (from the validation section)

A contract's `verification.required_tests` names what the partition must
clear; the project-level program mirrors those names:

* `reproducible_boot`, M1
* `cpu_isolation`, `memory_isolation`, `irq_isolation`, `timing_bound` -
  M1 (basic), M3 (measured)
* communication on declared endpoints, M1
* interference (GMR-INTERF v1), M3
* fault containment + recovery timing, M1 (basic) → M3/M5

Full methodology: [validation/methodology]
(../validation/methodology).

## Ladder

```text
host CI (x86-64)
   → QEMU
   → NG-ULTRA hardware
   → HPSC (research)
```

A result is only published once it reaches the platform it is claimed
about: an x86-64 number is never written as an NG-ULTRA number.

## Tooling policy

* No test tool, CLI flag, framework, or version is referenced anywhere in
  the documentation until the first code lands at M1, the anti-
  hallucination rules extend to tooling.
* Test *names* (slugs) referenced by contracts must be stable once M1
  ships, because contracts pin them.
