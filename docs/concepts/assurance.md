# Assurance positioning

GoMyRobotOS is deliberately **not** a safety-case platform. This page pins
down exactly where assurance sits relative to the partition platform —
it is frequently the most misunderstood boundary in the architecture.

## The boundary

```text
GoMyRobotOS
     │
     ├── configuration manifest
     ├── required properties
     ├── test requirements
     └── deployment metadata
             │
             ▼
     GoMyRobotVerify        (test planning, execution, coverage,
             │               regression, requirement-to-test traceability)
             │
     GoMyRobotFault / GoMyRobotBench   (fault models, HIL experiments)
             │
             ▼
     test / evidence artifacts
             │
             ▼
     GoMyRobotAssure         (evidence graph → assurance argument)
```

* **GoMyRobotOS produces evidence inputs.** It does not judge them,
  complete them, or present them as an assurance case.
* **GoMyRobotVerify and GoMyRobotAssure are external platform services.**
  The architecture treats them as consumers of GoMyRobotOS artifacts
  (ADR-0012), not as subsystems to embed.

## What GoMyRobotOS contributes to an assurance argument

Every deployment is accompanied by machine-describable metadata:

```text
partition configuration
hardware profile
backend version
image hash
resource allocation
required tests
deployment identity
```

together with the requirement identifiers declared in each contract
(e.g., `GMR-FLIGHT-CPU-001`) and the tests the contract declares as
required (`cpu_isolation`, `memory_isolation`, `irq_isolation`,
`timing_bound` in the v1 example). That traceability — requirement →
contract field → declared test → measured result — is the raw material an
external assurance case can use.

## What GoMyRobotOS explicitly does not claim

```{warning} No assurance claims in this documentation
GoMyRobotOS documentation never claims:

* formal WCET
* certification or safety certification (e.g., of any standard)
* complete freedom from interference
* that any particular deployment is "safe"

Those are conclusions an external assurance process may reach from
measured evidence. Until M1 onward produces such evidence, nothing of the
sort exists to claim.
```

## Why the boundary exists

1. **Coupling risk**: embedding verification in the platform couples the
   platform's change rhythm to the assurance process's evidence
   requirements — and the reverse.
2. **Reuse**: the same configuration and deployment metadata can feed
   independent verification, traceability, and supply-chain (SBOM)
   processes.
3. **Honesty**: the project's research contribution is about *portable,
   measurable partition semantics* — see
   [Assurance portability](../research/research-problems) — not about
   asserting safety.
