# Development environment

GoMyRobotOS development happens per platform role. This page describes the
development environments that the architecture commits to, with explicit
status labels.

## Documentation toolchain (available today)

| Tool            | Role                                  | Status |
| --------------- | ------------------------------------- | ------ |
| Python 3        | build runtime for Sphinx              | Available |
| Sphinx          | documentation builder                 | Available |
| MyST Markdown   | document authoring format             | Available |
| Read the Docs   | hosted, versioned documentation       | Available |
| GitHub Actions  | documentation build CI                | Available |

Local build: see [Installation](installation).

## Planned platform environments (from milestone M1 onward)

### x86-64 - development and reference

`Status: Development / Reference` as a platform role; backend implementation
`Status: Planned` (M1).

x86-64 is where the GoMyRobotOS software architecture is developed before
moving to space targets. It provides:

* fast iteration
* continuous integration (CI)
* automated tests
* QEMU virtualization for reproducible experiments
* fault-injection experiments
* backend development
* reproducible regression tests

### NG-ULTRA - flight reference

`Status: Flight Reference / Development` as a platform role; integration
work `Status: Planned` (M2).

The M0 baseline records that NG-ULTRA (four Cortex-R52 cores) has an
established ecosystem around RTEMS and XtratuM/XNG, and that existing RTEMS
work lists an ARMv8-R NG-ULTRA BSP. The NG-ULTRA development environment
therefore builds on that ecosystem - the GoMyRobotOS integration itself is
the planned work:

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

### PIC64-HPSC - RISC-V research

`Status: Research` (M4).

HPSC work is a research track: RTEMS baseline, WorldGuard investigation,
and Xen feasibility (host bring-up, domain creation, virtual timer,
interrupts, memory, RTEMS guest). Xen's RISC-V guest support is an active
development area, so HPSC must never be described as a supported production
platform - see [HPSC](../platforms/hpsc).

```{note}
No target-environment toolchain (cross compilers, QEMU machine types,
RTEMS BSP versions, hypervisor versions) is pinned anywhere in this
documentation until the corresponding milestone lands. Pins are added when
they are actually demonstrated.
```
