# Milestones overview

GoMyRobotOS runs a six-stage program, M0-M6, frozen at architecture
review. Each milestone has, and is judged by, an acceptance gate.
**M7 does not exist and must not be referenced** unless a future
architecture decision establishes it.

| Milestone | Objective                               | Acceptance gate                                                       |
| --------- | --------------------------------------- | --------------------------------------------------------------------- |
| [M0](m0)  | Architecture and Contract Freeze          | A complete workload can be described without backend-specific fields  |
| [M1](m1)  | x86-64 Reference Partition                | x86-64 reference boots and isolates partitions                        |
| [M2](m2)  | NG-ULTRA Flight Reference                 | NG-ULTRA executes the same conceptual flight partition                |
| [M3](m3)  | Interference Laboratory                   | Interference measurements are reproducible                            |
| [M4](m4)  | HPSC Research                             | HPSC demonstrates measurable hardware partitioning / virtualization feasibility |
| [M5](m5)  | Recovery and Assurance Integration        | Faults, tests and artifacts automatically feed assurance              |
| [M6](m6)  | ServiceReady Reference Platform           | Same conceptual mixed-criticality system is demonstrated across heterogeneous targets |

## Status snapshot (M0)

| Milestone | Status                          |
| --------- | ------------------------------- |
| M0        | **In progress**: this documentation is the freeze artifact |
| M1        | `Planned`                       |
| M2        | `Planned`                       |
| M3        | `Planned`                       |
| M4        | `Planned` (research track)      |
| M5        | `Planned`                       |
| M6        | `Planned`                       |

## How milestones are written

Every milestone page contains the same seven items:

1. objective
2. scope
3. deliverables
4. tests
5. acceptance gate
6. current status
7. known limitations

A milestone page is a *plan* until its gate passes; the status column is
the only thing that may change as work proceeds.
