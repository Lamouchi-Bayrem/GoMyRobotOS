# GoMyRobotAssure

GoMyRobotAssure **consumes artifacts rather than being embedded inside
GoMyRobotOS**. The flow it completes:

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

## The role

* **GoMyRobotOS produces evidence inputs.**
* **GoMyRobotAssure builds the assurance argument.**

The "Evidence Graph" is the representation of the assurance case - which
requirement is supported by which contract field, which test, which
measurement, on which deployment identity, with which image hash. This is
what the [evidence model](../assurance/evidence-model) and
[evidence graph](../assurance/evidence-graph) pages in GoMyRobotOS
describe from the *producer's* side.

## Why the boundary exists

Embedding the assurance argument in the platform would couple platform
change rhythm to assurance-case review rhythm, and would blur the
distinction between *logging what happened* (GoMyRobotOS) and *arguing
what it means* (GoMyRobotAssure). Keeping them separate is what makes the
output usable by multiple assurance consumers at once (safety argument,
security/SBOM traceability, operational runbook audit).

## The research hook: assurance portability

The question that makes this boundary commercially interesting:

> When the same conceptual partitioned system moves between x86-64,
> NG-ULTRA and HPSC, how much of the verification and assurance argument
> can be retained automatically?

That is Research Problem 5
([assurance portability](../research/research-problems)). GoMyRobotOS
supports it by emitting the portable metadata
(configuration, hardware profile, backend version, image hash, resource
allocation, required tests, deployment identity) - GoMyRobotAssure
decides what of it survives a target change.

```{warning}
No assurance argument, no certification claim, and no safety standard
conclusion exists at M0 - and none will be framed in this documentation
unless it is produced by a real, external assurance process. This page
documents the *data plane* only.
```

`Status: External product; artifact-consumption interface is planned (M5).
Not implemented in this repository.`
