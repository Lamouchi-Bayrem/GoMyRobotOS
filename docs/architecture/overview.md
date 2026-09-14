# Architecture overview

This section describes *how* GoMyRobotOS is mechanically designed: the
layered model, the Partition Contract, the IR, the backend model, the
runtime model, and the recovery model.

For the *why*, read
[Concepts overview](../concepts/overview) first.

## The final architecture

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

The top row is GoMyRobotOS proper. It has exactly three faces, built from
three deliverables frozen at M0:

| Face                | Deliverable (M0)        | Documented in                                  |
| ------------------- | ----------------------- | ---------------------------------------------- |
| Partition Contract  | Partition Contract v1   | [partition-contract](partition-contract)    |
| IR                  | IR v1                   | [ir](ir)                                    |
| Backend API         | Backend API v1          | [backend-model](backend-model)              |

Everything below the `Target realization` line is *not* GoMyRobotOS: the
target platforms realize the IR with backends, and the workloads (including
GoMyRobotRT) run inside the managed partitions.

## The surrounding ecosystem

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

Each sibling product has its own page in
[Components](../components/gomyrobotrt):

* [GoMyRobotRT](../components/gomyrobotrt) - deterministic flight runtime
* [ROS 2 (Rolling reference)](../components/ros2-rolling) - workload reference
* [GoMyRobotBSP](../components/gomyrobotbsp) - target realization / build
* [GoMyRobotGuard](../components/gomyrobotguard) - independent recovery
* [GoMyRobotFault](../components/gomyrobotfault) - fault and radiation modeling
* [GoMyRobotBench](../components/gomyrobotbench) - physical / HIL experiments
* [GoMyRobotVerify](../components/gomyrobotverify) - verification execution
* [GoMyRobotAssure](../components/gomyrobotassure) - evidence graph / safety argument

## Backend matrix (summary)

```text
                    GoMyRobotOS IR
                          │
             ┌────────────┼─────────────┐
             │            │             │
             ▼            ▼             ▼
           x86-64       NG-ULTRA       HPSC
             │            │             │
            Xen         XNG/XtratuM     Xen*
             │            │             │
         Linux/RTEMS     RTEMS        RTEMS/Linux*
```

`*` research/validation status, not a production claim.

## Five core responsibilities

1. **Partition definition** - the contract and its validation
2. **Resource / isolation semantics** - CPU, memory, interrupt, DMA,
   device, communication, timing semantics in the IR
3. **Backend realization** - the Backend API and the backends implementing
   it
4. **Runtime integration** - hosting GoMyRobotRT (and other workloads)
   inside managed partitions
5. **Partition-level recovery contract** - what a partition must do when
   something goes wrong (implemented independently, by GoMyRobotGuard)

Everything else connects to these five responsibilities but is not
implemented by GoMyRobotOS.
