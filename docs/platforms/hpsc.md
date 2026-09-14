# Platform: PIC64-HPSC

**Role:** next-generation RISC-V research target.
**Status:** `Research` (M4). This is a research platform - **do not
present HPSC as a supported production platform anywhere.**

## What the Final Architecture records

Microchip currently documents RTEMS and Xen support for PIC64-HPSC, as
well as hardware virtualization and WorldGuard end-to-end spatial
partitioning across cores, cache, interconnect, peripherals, and memory.
The device also includes an independent system-controller processor
suitable for monitoring and fault management.

> **Do not claim production RTEMS-on-Xen-HPSC support until it has been
> demonstrated.**

Xen's RISC-V guest support remains an active development area - 2026
development is still adding and refining guest ISA and interrupt
infrastructure - so HPSC/Xen stays explicitly a research track rather than
a claimed mature production backend. That actually strengthens the
research story.

## The research path

```text
HPSC
 ├── RTEMS
 │     └── baseline
 ├── WorldGuard
 │     └── hardware isolation
 └── Xen research
      ├── host bring-up
      ├── domain creation
      ├── virtual timer
      ├── interrupts
      ├── memory
      └── RTEMS guest
```

Each branch above is a research work item, not a supported platform
capability. The eventual question being investigated:

> Can hardware-assisted RISC-V partitioning provide predictable
> mixed-criticality isolation when combined with virtualization?

HPSC must not become a prerequisite for the rest of the architecture - if
Xen-on-HPSC stalls, the contract/IR/backend model stands on x86-64 and
NG-ULTRA.

## Why HPSC is interesting for the science

* **WorldGuard** extends partitioning across multiple hardware resource
  classes (cores, cache, interconnect, peripherals, memory) - exactly the
  multi-channel interference question of Research Problem 2
  ([interference](../validation/interference)).
* The **independent system controller** is the natural substrate for
  GoMyRobotGuard's independence requirement on a RISC-V target
  ([GoMyRobotGuard](../components/gomyrobotguard)).
* As the third realization of the same conceptual partition, HPSC is what
  turns "portability" from a two-point comparison into a research claim
  ([Research problem 1](../research/research-problems),
  [Milestones M4/M6](../milestones/overview)).

```{warning}
Nothing on this page is an implemented capability. M4's gate - "HPSC
demonstrates measurable hardware partitioning / virtualization
feasibility" - is `Planned`; M4 is research, not productization.
```
