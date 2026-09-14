# Layered model

GoMyRobotOS is organized as a strict vertical stack. Each layer has one job,
and each layer only talks to its neighbors:

```text
                    GoMyRobotOS
                         │
            Partition Contract
                         │
                         ▼
                       IR
                         │
               Target Backend
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
           Hypervisor          Bare metal /
           / separation        future backend
              │
              ▼
           Runtime
              │
              ▼
         GoMyRobotRT
              │
        ┌─────┴─────┐
        ▼           ▼
      RTEMS      ROS 2 APIs
```

## The layers

### 1. Partition Contract

The *author-facing* layer: a machine-readable description of intent and
constraints (execution, isolation, communication, startup, recovery).
Hypervisor-independent by definition, it cannot mention Xen or XtratuM.
See [partition-contract](partition-contract).

### 2. IR (GoMyRobotOS Intermediate Representation)

The *stable internal representation* between contract and backends. The
contract is parsed and validated into the IR; the IR is what every backend
consumes. The IR keeps the system coherent: adding a new backend must not
require touching the contract format, and changing a backend must not
invalidate the contract. See [ir](ir).

### 3. Target backend

The *only* layer allowed to be platform-specific. A backend maps IR
semantics onto what the target actually offers, a hypervisor's domains,
an RTOS partition system's slots, or (future) native hardware partitioning.
See [backend-model](backend-model).

### 4. Runtime

The execution substrate the backend produces: a running partition with
booted guests/domains, wired communication, owned devices, and exposed
health/recovery hooks.

### 5. GoMyRobotRT and the workload

The *workload* layer. [GoMyRobotRT](https://gomyrobot.com/products/rt/) executes robotics workloads on RTEMS,
including ROS 2 concepts; ROS 2 is the robotics middleware/workload
environment and is **not** the architectural center of GoMyRobotOS. See
[GoMyRobotRT](../components/gomyrobotrt) and
[ROS 2 (Rolling)](../components/ros2-rolling).

## Invariant vs. target-specific

| Concern                      | Level            | Example                                     |
| ---------------------------- | ---------------- | ------------------------------------------- |
| "Partition P runs at priority 10 on CPU 0 with a 300 µs budget" | Contract / IR | backend-agnostic |
| "Partition P is domain 1 pinned to CPU 0"                   | Backend         | may legitimately mention the hypervisor    |
| "GoMyRobotRT runs the flight ROS 2 workflow"                   | Runtime / RT    | host-specific but product-stable          |

This separation is what makes the central research question
([portable partition semantics](../research/research-problems))
tractable: it makes the *difference* between backends observable and
measurable rather than hidden in configuration.
