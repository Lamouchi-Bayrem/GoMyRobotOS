# Assurance: Evidence model

GoMyRobotOS is a **producer of evidence inputs**, not a judge of them
([ADR-0012](../development/architecture-decisions)).
This page defines what it produces, and from where.

## The evidence inputs

Every managed partition supplies, and every deployment publishes:

| Input                | Source (contract/IR/BSP)                                   |
| -------------------- | ------------------------------------------------------------|
| partition configuration   | the contract itself + IR                             |
| hardware profile            | target platform (Hardware Profile)                       |
| backend version             | the backend build realizing the IR                   |
| image hash                  | `security.image_identity` + BSP build metadata         |
| resource allocation         | `execution`, `memory`, `devices`, `interrupts`, `dma`    |
| required tests              | `verification.required_tests`                          |
| deployment identity         | BSP deployment manifest                                  |

plus, generated at runtime by the [recovery
model](../architecture/recovery-model):

| Input                | Meaning                                           |
| -------------------- | --------------------------------------------------|
| recovery actions log    | restart / safe state / escalation taken per partition |
| fault observations      | detections with measured T_* intervals            |

## Requirement → field → test → result chain

The contract's two traceability groups give the chain its first three
links; Verify/Bench/Fault supply the fourth:

```text
requirement            contract field            required test           measured result
GMR-FLIGHT-CPU-001  →  execution.cpu_set    →   cpu_isolation       →   (M3 measurement)
GMR-FLIGHT-MEM-002  →  memory.regions       →   memory_isolation    →   (M3 measurement)
                       interrupts.owned     →   irq_isolation       →   (M3 measurement)
                       timing_budget        →   timing_bound        →   (M3 measurement)
```

## Why this shape

1. **Machine-readable**: every input is YAML/JSON/hashes, not prose - an
   assurance process can consume it without a human in the loop.
2. **Portable by construction**: none of the inputs are backend-specific
   (the backend *version* is a fact about the realization, not about the
   contract) - which is what makes
   [assurance portability](evidence-graph) a researchable question.
3. **Final at the partition boundary**: the inputs are *complete at the
   partition level*; external products decide aggregation and argument
   structure.

## Timing evidence classification

Every timing claim in the evidence graph carries an explicit evidence
class:

* **proven** - backed by a formal / static WCET analysis
* **measured** - validated by benchmarking under a defined stress pattern
* **unbounded** - no bound; only for workload classes explicitly declared
  unbounded

Documentation and artifacts must never present `measured` as `proven`:
"validated under a 2 ms budget" and "WCET proven at 2 ms" are different
claims. The contract carries the class via
`execution.timing_budget.wcet_evidence_class`.

## What this is not

Not a safety case, not a claim of any standard (e.g., DO-178C or similar)
conformance, not a "guarantee". It is a *data plane for assurance*,
used however rigorously the external assurance process chooses. GoMyRobotOS
maps evidence onto existing standards (the ECSS Q ST 80C / ECSS E ST 40C
lineage, and ARINC 653 where useful); it creates no new certification
standard. At M0, it contains no measured values at
all - only the *structure* of what future measurements will take.
