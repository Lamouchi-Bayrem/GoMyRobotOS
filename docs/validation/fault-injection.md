# Validation: Fault injection

## The boundary, stated again

* **GoMyRobotOS** declares *what a partition must do when a fault occurs*
  (contract `recovery.*` - see
  [Recovery model](../architecture/recovery-model)).
* **GoMyRobotFault** provides *how faults are generated* - the fault
  recipes, injection harnesses, and models, including radiation-like
  models. See [GoMyRobotFault](../components/gomyrobotfault).

Validation = running the two together and recording the outcome.

## The fault classes validated against a contract

```text
CPU
memory
DMA
interrupt
I/O
communication
partition crash
watchdog
resource exhaustion
image corruption
```

plus the space-relevant families that GoMyRobotFault models:

```text
SEU-like bit flips
register corruption
memory corruption
configuration corruption
transient execution faults
communication corruption
watchdog events
```

## What each validation run produces

For each fault class, per partition, per backend:

* **was the fault detected, and how** (watchdog, trap, communication
  timeout, …),
* **did the contractual action happen** (`restart` / `safe_state` /
  escalation) *and* within what measured time,
* **did the other partitions survive** (containment - see
  [Spatial isolation](spatial-isolation) for the boundary-violation
  variants),
* **what is recorded** as evidence (the metadata consumed by
  GoMyRobotVerify / GoMyRobotAssure).

That is the [recovery timing model]
(recovery) - T_detect, T_contain, T_recover, T_resume.

## Radiation: the honesty rule

QEMU (and simulation generally) **models** radiation-induced fault
*effects*; it does not reproduce the physical radiation environment.
Consequently:

* a QEMU fault run is *software fault model* evidence,
* FPGA/HIL runs are *emulated physics* evidence,
* real NG-ULTRA / HPSC radiation testing is *physics* evidence
  (and is owned by the GoMyRobotFault/Bench/Assure stream, not by
  GoMyRobotOS).

The documentation never demotes upstream claims and never levels up:
"correlated with an SEU model" is not "radiation-hardened".

## Space fault responsibility split

GoMyRobotOS defines the detect / contain / recover **semantics**. The
physical mechanisms below are deliberately not core GoMyRobotOS
requirements; they belong to the **Hardware Profile**, the **Guard
implementation**, or the **assurance profile**:

| Fault                                   | Defined by                                          |
| --------------------------------------- | --------------------------------------------------- |
| SEU: SRAM / register corruption         | Hardware Profile (ECC / scrubbing) + Guard re-verification |
| Configuration / hypervisor-state corruption | Guard re-verification on watchdog cadence       |
| Single-event latchup                    | power-domain handling (current limiting, power cycling) under Guard control - not a software partitioning feature |
| Common-mode hypervisor failure          | only claimable from Guard Stage 1 onwards ([GoMyRobotGuard](../components/gomyrobotguard)) |

GoMyRobotOS does not become a hardware platform specification.

## Status

```text
recovery contract semantics:   specified (M0)
basic containment (M1 test item): Status: Planned
full class matrix + timing:    Status: Planned (M3/M5)
injection harnesses:           external (GoMyRobotFault), not present here
```
