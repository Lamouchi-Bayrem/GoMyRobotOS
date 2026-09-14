# Platform: NG-ULTRA

**Role:** space / flight reference - the first genuine space-oriented
execution reference.
**Status:** `Flight Reference / Development`; the GoMyRobotOS
XNG/XtratuM realization is `Planned` (M2).

## Why NG-ULTRA

Per the Final Architecture: NG-ULTRA is the first genuine space-oriented
execution reference. The platform has four Cortex-R52 cores and an
established ecosystem around RTEMS and XtratuM/XNG - existing RTEMS work
explicitly lists an ARMv8-R NG-ULTRA BSP, and NanoXplore's ecosystem
includes RTEMS and XtratuM/XNG support.

NG-ULTRA is also explicitly **radiation-hardened-by-design**, with
mechanisms such as EDAC, configuration scrubbing, and
memory/configuration protection - hardware behavior that the
fault-modeling stream ([GoMyRobotFault](https://gomyrobot.com/products/fault/)) correlates against, and that no
simulation can reproduce.

## Realization path

This is the **flight-oriented reference implementation**:

```text
GoMyRobotOS Contract
        ↓
GoMyRobotOS IR
        ↓
NG-ULTRA Backend
        ↓
XNG / XtratuM
        ↓
RTEMS
        ↓
GoMyRobotRT
```

M2 demonstrates: real target boot, partition configuration, resource
ownership, an RTEMS workload, timing measurement, and basic fault
containment - the acceptance gate being that NG-ULTRA executes *the same
conceptual flight partition* as x86-64
([M2](../milestones/m2)).

## Honest status notes

* The RTEMS BSP and XtratuM/XNG ecosystem facts above are **recorded
  ecosystem facts** from the Final Architecture, not claims made by this
  repository.
* "GoMyRobotOS on NG-ULTRA" is **not** a claim of implemented support:
  the GoMyRobotOS NG-ULTRA backend (contract → IR → XNG/XtratuM → RTEMS)
  is the M2 work item, `Status: Planned`.
* Until M2 produces measured results, no timing, WCET, or interference
  claim about this platform exists anywhere in this documentation.

## Role in the research program

NG-ULTRA is the primary non-x86 arm of the portable-partition-semantics
comparison (x86-64 + Xen **vs** NG-ULTRA + XNG/XtratuM) - Research
Problem 1 - and the first repetition target of the M3 interference
laboratory; see [Research
agenda](../research/agenda).
