# Recovery model

## What a partition must do when something goes wrong

Recovery in GoMyRobotOS is declared **per partition**, in the contract,
before any fault happens:

```yaml
recovery:
  watchdog: true
  restart_policy: restart
  safe_state: predefined
  escalation_policy: supervisor
```

| Field                | Meaning                                                  |
| -------------------- | --------------------------------------------------------- |
| `watchdog`           | whether the partition uses a contractual heartbeat          |
| `restart_policy`     | what a failure means: restart / safe state / escalation     |
| `safe_state`         | the predefined state the partition may fall back to         |
| `escalation_policy`  | who decides when recovery exceeds the partition's authority |

## The detect → contain → recover → resume pipeline

The recovery semantics follow the fault model that
[GoMyRobotFault](../components/gomyrobotfault) and
[GoMyRobotVerify](../components/gomyrobotverify) test against:

```text
fault
  ↓
detect
  ↓
contain
  ↓
recover
  ↓
resume / safe state
```

and the associated research-measured recovery model:

```text
T_detect  T_contain  T_recover  T_resume
```

The Final Architecture requires the end result to be a **measurable
recovery model** - not merely a statement that "recovery exists". Until
milestone M3+ produces these measurements, no recovery time claims exist
in this documentation.

## The independence boundary (ADR-0011)

> The component responsible for recovering a failed component must not
> depend exclusively on the failed component.

The division of labor is therefore strict:

* **GoMyRobotOS exposes recovery *semantics*** - contract fields,
  recovery hooks on the runtime model, and the escalation surface.
* **[GoMyRobotGuard](https://gomyrobot.com/products/guard/) implements the *independent recovery mechanism*** -
  monitoring flight, service, and platform/hypervisor domains and taking
  restart / isolate / reset actions:

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

On HPSC this boundary has hardware teeth: the device includes an
independent system-controller processor suitable for monitoring and fault
management - a candidate for Guard's independence (research track, M4).

## Recovery as assurance evidence

Each contract's `requirements` + `verification.required_tests` pair with the
recovery actions actually taken: GoMyRobotOS records *what* happened
(restart, safe state, escalation), and the external assurance process
decides *whether* that behavior supports the intended argument. That is
part of the [M5 recovery/assurance
integration](../milestones/m5).
