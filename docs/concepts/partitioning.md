# Partitioning

## What a partition is

A **partition** is a controlled execution domain with explicitly described
resources. A partition is *not defined by the isolation mechanism that
realizes it* - it is defined by the [Partition Contract](../contract/overview).

Concretely, a partition contract declares:

* **Identity**: unique id, name, criticality, trust domain
* **CPU**: cpu-set allocation, scheduling policy and priority, timing budget
* **Memory**: named regions with size and permissions
* **Devices**: devices the partition owns
* **Interrupts**: interrupts the partition owns
* **DMA**: permitted DMA regions
* **Communication**: endpoints with message-size and rate bounds
* **Startup**: boot artifact and dependencies (defines boot order)
* **Security**: image identity, secure-boot requirement
* **Recovery**: watchdog, restart policy, safe state, escalation policy
* **Requirements / verification**: requirement identifiers and required tests

This list is the minimum conceptual field set of the Partition Contract v1;
the full field reference is the [Specification](../contract/specification).

## Why partition, and not process / container / VM

A GoMyRobotOS partition is described at the level that is invariant across
separation mechanisms:

* a **process or container** is tied to one OS's semantics;
* a **VM / domain** is tied to one hypervisor's model;
* a **partition** is a semantic object - CPU, memory, time, interrupts,
  devices, DMA, communication, startup, recovery - that *each* target
  backend must realize with whatever it offers: Xen domains on x86-64,
  XtratuM partitions on NG-ULTRA, and (as research) hardware WorldGuard
  partitioning on HPSC.

This is the core research question of the project: which partition semantics
are genuinely portable, and which are inherently hardware/backend-specific
(see [Research problems](../research/research-problems)).

## A mixed-criticality system is a set of partitions

The target end-state (milestone M6 reference platform) is a system of
partitions with different criticalities and runtimes, under one supervisor:

```text
                  GoMyRobotOS
                      │
          ┌───────────┼───────────┐
          │           │           │
        Flight     Autonomy     Services
        RTEMS       RTEMS       Linux
          │           │           │
          └───────────┼───────────┘
                      ▼
               GoMyRobotGuard
```

Each column is partitioned independently; the Supervisor (GoMyRobotGuard)
must not depend exclusively on any single partition in order to recover the
others - see [GoMyRobotGuard](../components/gomyrobotguard) and
ADR-0011.

## Partition and partition contract - the distinction

The *contract* is the description; the *partition* is the running realization
of that description on a specific target using a specific backend. One
contract can have many realizations; that distinction is what
[assurance portability](../assurance/evidence-model) depends on.
