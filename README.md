# GoMyRobotOS

**GoMyRobotOS is a partition and execution platform for heterogeneous safety-critical space computers.** It defines a hypervisor-independent contract for execution, isolation, communication, startup, and recovery, then realizes that contract through target-specific backends.

> **Current status: M0 - Architecture and Contract Freeze.**
> GoMyRobotOS is documentation-first: the architecture, the Partition Contract, and the backend
> model are frozen as a specification. **No target system has been implemented yet.**
> Every maturity statement in this repository uses the labels
> `Stable`, `Experimental`, `Research`, `Planned`, or `Not implemented`.

---

## Why it exists

Safety-critical flight computers are becoming heterogeneous: x86-64 development and CI
machines, flight-oriented ARM platforms such as NG-ULTRA, and next-generation RISC-V
processors such as PIC64-HPSC with hardware spatial partitioning (WorldGuard). Each platform
offers a different separation mechanism - Xen, XNG/XtratuM, hardware guard bands - and each
one typically forces teams to re-derive the same execution-semantics decisions from scratch.

GoMyRobotOS expresses those decisions once, in a **Partition Contract**: a machine-readable,
hypervisor-independent description of what a partition is allowed (and required) to do.
Target-specific backends then realize the contract using the separation mechanisms that each
platform actually provides.

> **Describe the required execution semantics once; realize them according to the
> capabilities of the target platform.**
> The hypervisor is an implementation backend - not the product abstraction.

## What GoMyRobotOS is (and is not)

GoMyRobotOS **is**:

* a partition model
* a machine-readable execution contract
* an intermediate representation (IR)
* a target-backend interface
* a partition deployment/orchestration layer
* a runtime integration layer
* a partition health/recovery interface
* a source of configuration and deployment metadata

GoMyRobotOS is **not**:

* an RTOS, a hypervisor, a Linux distribution, or a ROS 2 replacement
* a BSP, a simulator, or a radiation-testing framework
* a complete fault-injection platform or a safety-case platform

Those capabilities belong to sibling GoMyRobot products; the boundaries between them are a
central part of this architecture.

## Architecture

```text
                        GoMyRobotOS
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
  Partition Contract          IR           Backend API
         │                   │                   │
         └───────────────────┼───────────────────┘
                             ▼
                   Target realization
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
       x86-64             NG-ULTRA                HPSC
         │                   │                   │
        Xen             XNG/XtratuM          Xen / WG*
         └───────────────────┼───────────────────┘
                             ▼
                      GoMyRobotRT
                             │
                        RTEMS + ROS
                             │
                         Workloads
```

`*` research/validation status, not a production claim.
Surrounding ecosystem:

```text
              ┌──────────────────────────┐
              │       GoMyRobotOS        │
              │  Partition + Execution   │
              └────────────┬─────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
 GoMyRobotFault     GoMyRobotBench    GoMyRobotVerify
         │                 │                 │
         └─────────────────┼─────────────────┘
                           ▼
                    GoMyRobotAssure

 GoMyRobotSecure ─────── security chain
 GoMyRobotBSP ────────── target realization/build
 GoMyRobotRT ─────────── flight runtime
 GoMyRobotSim ────────── simulation
```

## The Partition Contract

The central artifact of GoMyRobotOS is a **hypervisor-independent Partition Contract**.
Instead of *"generate a Xen configuration"* or *"generate an XNG configuration"*, the
contract answers: **what is a partition allowed and required to do?**

```yaml
partition:
  id: flight-control
  name: Flight Control
  criticality: high
  trust_domain: flight

execution:
  cpu_set: [0]
  scheduling:
    policy: fixed_priority
    priority: 10
  timing_budget:
    period_us: 1000
    budget_us: 300

recovery:
  watchdog: true
  restart_policy: restart
  safe_state: predefined
  escalation_policy: supervisor
```

The contract describes **intent and constraints, not backend syntax**. The full
specification, JSON Schema, and examples live in the documentation
(`docs/contract/` and `schemas/`).

## Relationship with GoMyRobotRT

> **[GoMyRobotRT](https://gomyrobot.com/products/rt/) executes the robotics workload.**
> **GoMyRobotOS controls the execution environment in which that workload runs.**

GoMyRobotRT remains a separate product: RTEMS, deterministic executors, robotics
middleware (including ROS 2-based workloads), hardware abstraction, and flight
application interfaces. GoMyRobotOS consumes or hosts GoMyRobotRT inside a managed
partition.

## Relationship with ROS 2

ROS 2 is **a workload**, not the architectural center of GoMyRobotOS.

The official documentation reference for all ROS 2 concepts in this project is
**ROS 2 Rolling** (<https://docs.ros.org/en/rolling/>). The GoMyRobotOS
documentation never duplicates ROS 2 documentation - it links to Rolling for
standard concepts and documents only the GoMyRobot-specific integration and
execution guarantees. No ROS 2 support is implemented in this repository today
(`Status: Research` for GoMyRobotRT).

## Initial targets

| Target     | Role                                                          | Status                     |
| ---------- | ------------------------------------------------------------- | -------------------------- |
| x86-64     | development / reference (CI, QEMU, backend development)       | Development / Reference    |
| NG-ULTRA   | space / flight reference (RTEMS + XtratuM/XNG ecosystem)      | Flight Reference / Development |
| PIC64-HPSC | next-generation RISC-V research (WorldGuard, Xen feasibility) | Research                   |

## Current status and roadmap

| Milestone | Objective                                | Acceptance gate                                                             | Status             |
| --------- | ---------------------------------------- | --------------------------------------------------------------------------- | ------------------ |
| M0        | Contract and architecture freeze         | A complete workload can be described without backend-specific fields        | In progress (docs) |
| M1        | x86-64 reference platform                | x86-64 reference boots and isolates partitions                              | Planned            |
| M2        | NG-ULTRA flight reference                | NG-ULTRA executes the same conceptual flight partition                      | Planned            |
| M3        | Interference laboratory                  | Interference measurements are reproducible                                  | Planned            |
| M4        | HPSC research                            | HPSC demonstrates measurable hardware partitioning / virtualization feasibility | Planned / Research |
| M5        | Recovery and assurance integration       | Faults, tests and artifacts automatically feed assurance                    | Planned            |
| M6        | ServiceReady reference platform          | Same conceptual mixed-criticality system demonstrated on heterogeneous targets | Planned          |

## Research direction

> **Can one machine-readable partition contract describe and validate equivalent
> mixed-criticality execution semantics across heterogeneous space computing
> architectures and separation mechanisms?**

Core research problems: portable partition semantics, multi-channel interference
(CPU, cache, memory, DMA, interrupts, I/O), fault containment and recovery, and
assurance portability. Space-environment fault modeling is researched through
[GoMyRobotFault](https://gomyrobot.com/products/fault/) / [GoMyRobotBench](https://gomyrobot.com/products/bench/) / [GoMyRobotAssure](https://gomyrobot.com/products/assure/) rather than inside GoMyRobotOS.
See `docs/research/` in the documentation.

## Documentation

* Documentation home: <https://gomyrobotos.readthedocs.io>
  (Sphinx + MyST Markdown, hosted on Read the Docs, rebuilt by CI on every push)
* Repository: <https://github.com/gomyrobot/GoMyRobotOS>
* Architectural, contract, and process documentation: this site
  (Sphinx + MyST sources under `docs/`, built by CI and hosted above)

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## License

[Apache License 2.0](LICENSE).

