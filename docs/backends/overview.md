# Backends

A **backend** is the only layer in GoMyRobotOS allowed to know mechanism
names. Backends consume the GoMyRobotOS IR and realize the declared
execution semantics using what a target actually offers. See the
[Backend model](../architecture/backend-model) for the full contract a
backend must satisfy.

## The initial backend matrix

```text
                    GoMyRobotOS IR
                          │
             ┌────────────┼─────────────┐
             │            │             │
             ▼            ▼             ▼
           x86-64       NG-ULTRA       HPSC
             │            │             │
            Xen         XNG/XtratuM     Xen*
             │            │             │
         Linux/RTEMS     RTEMS        RTEMS/Linux*
```

`*` research/validation status, not a production claim.

| Backend target   | Realization          | Platform role            | Status              |
| ---------------- | -------------------- | ------------------------ | ------------------- |
| x86-64           | Xen                  | Development / Reference  | Planned (M1)        |
| NG-ULTRA         | XNG / XtratuM        | Flight Reference         | Planned (M2)        |
| PIC64-HPSC       | Xen* / WorldGuard*   | RISC-V research target   | Research (M4)       |
| (future)         | bare-metal / native hardware partitioning | research     | Research            |

## Pages in this section

* [Xen](xen) - the x86-64 development backend (Planned) and the HPSC research track
* [XtratuM](xtratum) - the NG-ULTRA hypervisor (Planned)
* [XNG](xng) - the XNG partitioning/pipeline layer of the NG-ULTRA
  backend (Planned)

## What every backend maps

| IR semantics           | Target-side realization question                           |
| ---------------------- | -----------------------------------------------------------|
| CPU resources           | how cpus are pinned/allocated to a partition                 |
| memory resources        | how partition memory is separated + permissioned             |
| interrupt resources     | how interrupts are dedicated to exactly one partition        |
| DMA resources           | how DMA is constrained to declared regions                   |
| device resources        | how owned devices are attached to a partition                |
| communication endpoints | bounded cross-partition channels                             |
| timing                  | the scheduling/timing mechanism the contract declares        |
| startup                 | the boot ordering the contract depends on                    |
| recovery hooks          | watchdog/restart surfaces for the recovery model             |

## Rules for backend work (frozen at M0)

1. Backends consume the **IR**, never the raw contract format.
2. Backend-specific identifiers never leak into the contract layer; they
   live in the **backend profile** consumed by [GoMyRobotBSP](https://gomyrobot.com/products/bsp/).
3. A backend's documented capabilities are exactly its *validated*
   capabilities - no backend claims a semantic its target has not
   demonstrated.
