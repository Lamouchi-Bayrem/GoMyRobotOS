# Assurance: Evidence graph

The **Evidence Graph** is the artifact that completes the assurance chain:
it is the representation of *why a property holds* — which requirement,
which contract field, which test, which measurement, on which deployment
identity, with which image hash.

```text
GoMyRobotOS
      │
      ├── partition definition
      ├── configuration
      ├── hashes
      ├── required properties
      └── evidence references
             │
             ▼
     GoMyRobotVerify
     GoMyRobotFault
     GoMyRobotBench
             │
             ▼
    test / evidence artifacts
             │
             ▼
     GoMyRobotAssure
             │
             ▼
       Evidence Graph
```

The graph is *owned and structured by GoMyRobotAssure*. This page
documents GoMyRobotOS's obligations as a **producer of graph inputs**:

## Graph inputs GoMyRobotOS emits

| Node-kind on the graph     | GoMyRobotOS's contribution                         |
| -------------------------- | ----------------------------------------------------- |
| requirement                | contract `requirements` (GMR-… ids)                    |
| property / contract field  | the contract field the requirement constrains          |
| test requirement           | `verification.required_tests`                          |
| test execution             | results handed to Verify (per run, deployment-pinned)  |
| fault event                | recovery actions + T_* measurements                    |
| deployment identity        | manifest + hashes (with BSP)                           |
| environment                | hardware profile + backend version                     |

## Graph nodes vs. edges (blank at M0)

The intended edges — *requirement → field → test → result* — are exactly
the [requirement chain]
(evidence-model.md#requirement-field-test-result-chain) from the
evidence-model page. **No edge on this graph is yet backed by a measured
result**: every "result" node is `Status: Planned` (M1/M3/M5). This is
kept explicit so that a future reader never mistakes the *schema* of the
graph for the *contents* of the graph.

## The portability question

When the same conceptual partitioned system moves between x86-64,
NG-ULTRA, and HPSC, the question is: **how many graph edges can be
retained automatically?** The inputs that are portable by construction
(requirements, contract fields, required tests, deployment identity)
form the "retainable core"; the target-bound inputs (backend behavior,
measured results) form the "re-measure" set. Mapping that split is
Research Problem 5 — see
[research-problems](../research/research-problems) — and is the commercial core of
the project.

`Status: data plane defined (M0); populated graph: does not exist yet;
automatic M5 feed-in: Planned.`
