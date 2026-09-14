# Architecture v2 (working draft), superseded for the M0 baseline

```{attention}
This document is **not** the current baseline.
```

The v2 architecture draft is a richer, heavier specification that the team
has reviewed but **not adopted** as the architecture baseline. It has been
removed from the repository after its selected sections were integrated;
the frozen M0 architecture is documented in this site, its 6 milestones,
its three targets (x86-64 / NG-ULTRA / PIC64-HPSC), and the abstractions
defined here.

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
hardware-specific assumptions in the core architecture. The full
exclusion list is normative in the
[frozen baseline scope notes](../architecture/frozen-baseline).

Future intake of v2-class ideas happens by ADR against the documented
baseline.