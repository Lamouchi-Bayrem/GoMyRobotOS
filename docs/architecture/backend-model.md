# Backend model

## The rule

**Hypervisors are target-specific backends** (ADR-0003). A "backend" in
GoMyRobotOS is the thin layer that:

1. consumes the GoMyRobotOS IR (never the raw contract), and
2. realizes the declared execution semantics using what the target actually
   offers - a hypervisor, an RTOS partition system, or (future) native
   hardware partitioning.

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

## A backend is a mapping, not a product

Each backend implements the **Backend API v1** by mapping IR semantics to
target mechanisms:

| IR semantics (intent)   | What a backend must provide                              |
| ------------------------ | ---------------------------------------------------------- |
| CPU resources            | a way to pin/allocate cpus to a partition                  |
| memory resources         | a way to separate partition memory + declare permissions  |
| interrupt resources      | a way to dedicate interrupts to exactly one partition      |
| DMA resources            | a way to constrain DMA to declared regions                 |
| device resources         | a way to attach owned devices to a partition               |
| communication            | bounded channels between declared partition endpoints      |
| timing                    | the scheduling/timing mechanism the contract declares      |
| startup                   | the boot ordering the contract depends on                  |
| recovery hooks            | watchdog/restart surfaces the recovery model can consume   |

A backend *may* exploit extra target capabilities (hardware guard bands,
EDAC, system controllers) - as long as the contract/IR never depend on
them.

## Initial backends and their status

| Backend target            | Realization                | Status        |
| ------------------------- | -------------------------- | ------------- |
| x86-64                    | Xen                        | Planned (M1)  |
| NG-ULTRA                  | XNG / XtratuM              | Planned (M2)  |
| PIC64-HPSC                | Xen (research) / WorldGuard (research) | Research (M4) |
| future mechanisms         | bare-metal / native hardware partitioning | Research |

Status pages per backend:
[Xen](../backends/xen), [XtratuM](../backends/xtratum), [XNG](../backends/xng),
platform context:
[x86-64](../platforms/x86-64),
[NG-ULTRA](../platforms/ng-ultra),
[HPSC](../platforms/hpsc).

## What backends must never do

* read the raw contract format directly (they take the IR)
* expose backend-specific identifiers to the contract layer
* claim semantics the target has not demonstrated - the backend's
  documented capabilities are exactly its validated capabilities
