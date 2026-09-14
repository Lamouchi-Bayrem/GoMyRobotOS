# Backend: XNG

**Used on:** NG-ULTRA, in combination with [XtratuM](xtratum).
**Status:** `Planned` (M2). **Not implemented in this repository.**

## What XNG is in the GoMyRobotOS model

XNG is the **partitioning / pipeline layer** of the NG-ULTRA backend —
the side that deals in *partition specifications* (partition slots,
resource assignment, the inter-partition structure of the system) down the
`XNG / XtratuM → RTEMS` chain, whereas XtratuM is the hypervisor that
actually enforces the separation.

In the backend README terms:

```text
NG-ULTRA Backend
      ├── XNG      ← partition specification / pipeline
      └── XtratuM  ← hypervisor enforcement
```

Both together satisfy the backend's mapping duties
(IR → target mechanisms: cpus, memory, interrupts, DMA, devices, channels,
boot ordering) — see [Backend
model](../architecture/backend-model).

## Why a separate page

The Final Architecture and its target matrix write the backend as
"XNG/XtratuM"; keeping the two names distinct here:

* prevents documenting XtratuM configuration as if it *were* the XNG
  specification, and vice versa
* keeps the ADR-0003 rule visible: both are backend-level details,
  **neither** may leak into the contract or IR vocabulary
* makes backend-profile authoring (GoMyRobotBSP) unambiguous: the profile
  carries the XNG/XtratuM-specific data, the contract does not

## Status and scope at M0

* What will be documented when M2 lands: the IR→XNG mapping, the
  IR→XtratuM configuration mapping, and the validated properties of the
  NG-ULTRA backend (empty until measured).
* What will **not** be claimed at any unresearched state: specific XNG
  pipeline versions, XtratuM partition-slot guarantees, or timing
  behavior of any kind.

The flight-oriented reference chain including XNG is in
[M2](../milestones/m2) and
[NG-ULTRA](../platforms/ng-ultra).
