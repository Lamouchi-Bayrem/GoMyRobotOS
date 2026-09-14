# Architecture v2 (working draft) - superseded for the M0 baseline

```{attention}
This document is **not** the current baseline.
```

The v2 architecture draft (`gomyrobotos-architecture-v2.md` at the
repository root) is a richer, heavier specification that the team has
reviewed but **not adopted** as the architecture baseline. The frozen M0
architecture remains `GoMyRobotOS.md` (repository root): its 6
milestones, its three targets (x86-64 / NG-ULTRA / PIC64-HPSC), and the
abstractions defined there.

Five ideas from the v2 draft were selected for integration into the M0
baseline; their normative text now lives in the pages this site points
to:

| v2 idea | Where it is now defined |
| --- | --- |
| Backend Capability Manifest + no-silent-downgrade rule | [Backend model](../architecture/backend-model) |
| IPC channel semantics (sampling / queuing, channel properties) | [Contract overview](../contract/overview), [Contract specification](../contract/specification) |
| Guard independence staging (0 / 1 / 2) | [GoMyRobotGuard](../components/gomyrobotguard) |
| WCET evidence classes (proven / measured / unbounded) | [Evidence model](../assurance/evidence-model) |
| Space-fault responsibility split (semantics vs. hardware mechanisms) | [Fault injection](../validation/fault-injection) |

Explicitly **not** pulled into the core v1 baseline (and the M0
architecture must not imply them): `power` as an active contract concept,
`fleet` as an abstraction, transport-mechanism requirements in the
contract, clause-level certification mapping as a hard dependency, and
hardware-specific assumptions in the core architecture. See section 33
("Scope notes for the frozen baseline") of `GoMyRobotOS.md` in the
repository root.

The v2 file is kept at the repository root as a record of the design
space discussed; do not edit it to follow the baseline (nor the reverse)
- future intake happens by ADR against the M0 baseline.