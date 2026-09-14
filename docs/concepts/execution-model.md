# Execution model

## The realization pipeline

Execution in GoMyRobotOS is the result of a pipeline from the portable layer
down to a concrete target:

```text
Partition Contract
       │
       ▼
Parser
       │
       ▼
Validator
       │
       ▼
GoMyRobotOS IR
       │
       ├───────────────┬────────────────┐
       ▼               ▼                ▼
     Xen            XNG/XtratuM       Future
    Backend           Backend         Backend
       │               │
       ▼               ▼
target artifacts   target artifacts
```

* The **contract** is author-facing, human-auditable intent.
* The **IR (GoMyRobotOS Intermediate Representation)** is the stable
  internal representation shared by all backends — see
  [IR](../architecture/ir).
* A **backend** is the only layer allowed to know about Xen, XtratuM/XNG,
  or raw hardware — see [Backend model](../architecture/backend-model).

## What "execution" means per partition

A partition's execution profile is fixed by its contract:

* which cpus it may run on,
* with what scheduling policy and priority,
* within what timing budget (period and budget in microseconds),
* over what memory regions, interrupt vector, device set, and DMA
  region.

Deterministic execution properties (fixed priorities, bounded budgets,
static allocation) are *declared in the contract*; whether the target
backend enforces them with what fidelity is a backend matter — and it is
*measured in validation*, not assumed (see
[Temporal isolation](../validation/temporal-isolation)).

## Runtime integration

The software that *runs* inside a partition is the workload. For the
flight-oriented reference stack, the workload is **GoMyRobotRT**:

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
            ┌────────┴────────┐
            ▼                 ▼
         Hypervisor       Bare metal /
         / separation    future backend
            │
            ▼
          Runtime
            │
            ▼
        GoMyRobotRT
            │
       ┌────┴─────┐
       ▼          ▼
     RTEMS     ROS 2 APIs
```

* **GoMyRobotOS** hosts or consumes GoMyRobotRT — it controls the
  execution environment.
* **GoMyRobotRT** executes the robotics workload (deterministic executors,
  robotics middleware including ROS 2 concepts, hardware abstraction) —
  see [GoMyRobotRT](../components/gomyrobotrt).

The two remain separate products
([ADR-0007](../development/architecture-decisions)).

## Non-partition execution

Not every workload is a flight partition. The reference deployment shapes
also include service domains running Linux (built, where applicable, by the
GoMyRobotBSP target-build pipeline using Yocto/OpenEmbedded — see
[Yocto's role](../components/gomyrobotbsp)). GoMyRobotOS
still manages those domains as partitions: startup order, recovery
behavior, and health monitoring are contractual.
