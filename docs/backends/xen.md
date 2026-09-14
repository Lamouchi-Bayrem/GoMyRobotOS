# Backend: Xen

**Used on:** x86-64 (primary development/reference backend) and, as
research, PIC64-HPSC.
**Status:** x86-64 realization `Planned` (M1); HPSC realization
`Research` (M4). **Not implemented in this repository.**

## Role in the model

On x86-64, Xen is the mechanism that realizes the partition semantics of
the IR:

```text
Partition Contract
      → IR
      → Xen backend
      → Linux / RTEMS guests
      → (flight partition) GoMyRobotRT
```

The map from IR constructs to Xen-side mechanisms (cpu pinning, domain
memory, interrupt routing, device attachment, event channels) is designed
as part of Milestone M1's "Xen backend" work item - it will be documented
*when implemented*, with its validated properties only.

## x86-64 status

`Status: Planned (M1).` Deliverables that will make this a real backend:
parser, validator, IR, the Xen backend itself, boot/deployment, and basic
partition monitoring; tests: reproducible boot, CPU allocation, memory
isolation, communication, basic fault containment.

## HPSC status - research track

Xen on RISC-V (i.e., hosting RTEMS/Linux guests on PIC64-HPSC) is an
**active development area upstream**: contemporary Xen development is
still adding and refining RISC-V guest ISA and interrupt infrastructure.
Per the M0 baseline:

> **Do not claim production RTEMS-on-Xen-HPSC support until you have
> demonstrated it.**

The HPSC/Xen work items are explicitly staged:

```text
Xen research
 ├── host bring-up
 ├── domain creation
 ├── virtual timer
 ├── interrupts
 ├── memory
 └── RTEMS guest
```

M4's gate is "*measurable* hardware partitioning / virtualization
feasibility", not "production Xen on HPSC".

## What Xen must never be

Even though Xen is the natural candidate backend on x86-64, the
documentation keeps the ADR-0003 discipline: **the hypervisor is a backend,
not the product abstraction.** No contract field, no IR node, no
GoMyRobotOS API is named after, or only expressible in, Xen terms.
