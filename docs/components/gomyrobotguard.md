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
