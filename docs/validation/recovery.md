# Validation: Recovery

Recovery validation answers one question: **does the contractual recovery
semantics produce a *measurable* recovery model rather than a statement
that "recovery exists"?**

## The pipeline under test

Every validation run follows the standard fault model:

```text
fault
  ↓
detect
  ↓
contain
  ↓
recover
  ↓
resume / safe state
```

with the four measured intervals:

```text
T_detect  T_contain  T_recover  T_resume
```

| Interval   | Measured between                                        |
| ---------- | --------------------------------------------------------|
| `T_detect`  | fault occurrence → detection mechanism reports failure    |
| `T_contain` | fault occurrence → other partitions provably unaffected  |
| `T_recover` | detection → partition reaches its contractual action      |
| `T_resume`  | recovery action start → partition back to service         |

## The fault classes exercised

From Research Problem 3's list: application crash, illegal memory access,
illegal MMIO, DMA violation, interrupt abuse, CPU starvation, resource
exhaustion, service-domain crash, management-domain failure, watchdog
timeout, corrupted image.

The last three - *service-domain crash*, *management-domain failure*,
and *corrupted image* - are where the GoMyRobotGuard independence rule
(ADR-0011) gets exercised hardest: the recovery action must be taken by
something that does **not** depend on the failed domain
([GoMyRobotGuard](../components/gomyrobotguard)).

## What "passing" means

A recovery validation run passes when, for a given
(partition, fault class, backend):

1. fault was detected within a logged `T_detect`,
2. containment held (no cross-partition effect beyond declared channels),
3. the *contractual* action executed (restart / safe state / escalation
   as declared),
4. `T_recover` and `T_resume` are logged,
5. the metadata flows to the
   [evidence graph](../assurance/evidence-graph)
   without manual rework (the M5 integration goal).

## Status

```text
recovery semantics (contract):        specified (M0)
recovery timing measurements:         none exist yet
timing model (T_* table):             Status: Planned (M3+; automated into
                                      assurance at M5)
```

```{warning}
No GoMyRobotOS documentation page states a recovery time ("recovers in
< N ms") until such a measurement exists. A recovery plan being *declared*
in a contract is not a recovery time being *achieved* - the anti-hallucination
rules treat these as different facts.
```
