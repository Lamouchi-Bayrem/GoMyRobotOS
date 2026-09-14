# Backend: XtratuM

**Used on:** NG-ULTRA (primary flight-reference backend, together with the
XNG tools/flow).
**Status:** `Planned` (M2).**Not implemented in this repository.**

## Role in the model

XtratuM is the **hypervisor** of the NG-ULTRA backend. In the
flight-oriented reference implementation it is the mechanism that realizes
the IR's partition semantics on the four Cortex-R52 cores:

```text
GoMyRobotOS Contract
      ↓
GoMyRobotOS IR
      ↓
NG-ULTRA Backend
      ↓
XNG / XtratuM       ← this page (hypervisor) + [XNG](xng) (spec/naming layer)
      ↓
RTEMS
      ↓
GoMyRobotRT
```

## Ecosystem basis (recorded facts from the Final Architecture)

The architecture records that NG-ULTRA has an established ecosystem around
RTEMS and XtratuM/XNG, that existing RTEMS work lists an ARMv8-R NG-ULTRA
BSP, and that NanoXplore's ecosystem includes RTEMS and XtratuM/XNG
support. Those are *ecosystem facts used to justify the backend choice* —
not claims by this repository.

## What M2 must produce

The GoMyRobotOS NG-ULTRA backend:

1. maps IR partition semantics to XtratuM configuration,
2. realizes the declared memory/interrupt/DMA/device separation,
3. hosts RTEMS as the partition runtime,
4. boots the reference flight partition with
   `Status: Flight Reference / Development`.

M2's gate: **NG-ULTRA executes the same conceptual flight partition** as
the x86-64 reference
([M2](../milestones/m2)).

## Documentation discipline

Until M2 validation exists: no timing claims, no interference claims, no
"isolation guaranteed" phrasing anywhere in this repository about
XtratuM-backed partitions. The validated-properties table for this backend
is **empty by design** at M0.
