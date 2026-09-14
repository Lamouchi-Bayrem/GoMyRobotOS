# Validation: Spatial isolation

**Contract hooks:** `memory.regions`, `dma.permitted_regions`,
`interrupts.owned`, `devices.ownership` (see
[contract spec](../contract/specification)).

## What "spatial isolation" means here

Nothing in one partition reaches into another partition's declared space:
memory regions, DMA targets, interrupt lines, or devices - except through
a declared `communication` endpoint.

## The isolation invariants (per contract field)

| Field                  | Invariant to validate                                       |
| ---------------------- | -------------------------------------------------------------|
| `memory.regions`         | a partition cannot read/write memory outside its regions     |
| `dma.permitted_regions`  | DMA from the partition lands only in permitted regions       |
| `interrupts.owned`       | an owned interrupt is delivered only to its partition        |
| `devices.ownership`      | a device is reachable only from its owning partition         |

## How the invariants are tested

The natural test is *negative*: a fault-injection campaign that asks each
inter-partition boundary to be violated, and checks that the backend
contained it:

```text
attempt illegal memory access   → contained?   recorded?
attempt illegal MMIO             → contained?   recorded?
attempt DMA outside region       → contained?   recorded?
attempt unowned interrupt/driver → contained?   recorded?
```

This is Research Problem 3's "illegal memory access / illegal MMIO / DMA
violation" fault classes - see [Fault
injection](fault-injection) and
[Research problem 3](../research/research-problems).

Expected deliverable: a table, per backend, of *which* spatial invariants
are *enforced*, *how* (backend mechanism), and *demonstrated* when -
empty until M1/M2 validation runs exist.

## Status

```text
contract semantics:            specified (M0)
negative-test harness:         Status: Planned (M1 fault containment, M3 per-channel)
any enforcement evidence:      none exists yet
```

```{note}
Xen (IOMMU-backed DMA restrictions), XtratuM/XNG (partition memory maps),
and WorldGuard (hardware guard bands) each realize spatial isolation
differently; that difference is *the point* of measuring it rather than
assuming it - see [Research
problem 1](../research/research-problems) (portable partition
semantics).
```
