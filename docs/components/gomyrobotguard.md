# GoMyRobotGuard

GoMyRobotGuard remains a separate product because its responsibility is
**independent recovery and runtime safety enforcement**
([ADR-0011](../development/architecture-decisions)).

The core principle:

> The component responsible for recovering a failed component must not
> depend exclusively on the failed component.

## Architecture

```text
                 GoMyRobotGuard
                      │
          ┌───────────┼───────────┐
          │           │           │
          ▼           ▼           ▼
       Flight     Service    Platform
       domain     domain     / hypervisor
          │           │           │
          └───────────┼─────────┘
                      ▼
               Recovery action
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
     restart        isolate        reset
```

Guard observes flight, service, and platform/hypervisor domains, and takes
restart / isolate / reset actions when a partition's contractual recovery
semantics are triggered.

## Division of labor with GoMyRobotOS

* **GoMyRobotOS exposes recovery *semantics*** - the contract fields
  (`watchdog`, `restart_policy`, `safe_state`, `escalation_policy`), the
  recovery hooks on the runtime model, and the escalation surface. See the
  [Recovery
  model](../architecture/recovery-model).
* **GoMyRobotGuard implements the *independent* recovery *mechanism*** -
  the watcher + actuator that must survive the failure of any single
  domain, including the one it is about to act on.

## Independence staging

Independence is staged, and every claim records the stage it was
demonstrated under:

| Stage | Guard realization                                    | Independence claim                                              |
| ----- | ---------------------------------------------------- | --------------------------------------------------------------- |
| 0 (software)  | resident in the same flight domain as the hypervisor | no claim against common-mode hypervisor failure                |
| 1 (companion MCU / system controller) | independent watchdog and reset lines; independent of the primary SoC hypervisor/OS state | common-mode independence of the flight domain |
| 2 (evidence)  | Guard feeds the evidence graph directly, with per-fault-class detect / contain / recover timing | recovery claim quantified in time per fault class |

A contract may declare `recovery.guard_independence_stage`, and every
recovery claim in the evidence graph records the stage it was demonstrated
under.

Hardware-level space-fault mechanisms (ECC, scrubbing, latchup current
limiting, power cycling) are implemented by the **Hardware Profile** and
the **Guard implementation**; GoMyRobotOS defines the detect / contain /
recover semantics only (see [Fault injection](../validation/fault-injection)).

## HPSC: hardware independence

On HPSC this boundary becomes concrete: the device includes an independent
system-controller processor suitable for monitoring and fault management -
a natural substrate for Guard's independence from the flight/domains it
recovers. That is a **research-track** use (M4), not a claimed capability.

```{note}
Where recovery is *specified* (contract) vs. *executed* (Guard) is one of
the most audited questions in the M5 milestone
([M5](../milestones/m5)).
```
