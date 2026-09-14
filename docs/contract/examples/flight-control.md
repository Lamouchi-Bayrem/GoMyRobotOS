# Example contract: `flight-control`

This is the canonical v1 example carried in the Final Architecture
(GoMyRobotOS - Final Architecture, §4). It is identical in
`examples/x86-64/flight-control.yml`,
`examples/ng-ultra/flight-control.yml`, and
`examples/hpsc/flight-control.yml` - the whole point being that *one*
conceptual partition is described once, for three targets.

```{warning} Illustrative contract
This contract is a **specification artifact** (M0). It describes the
intended flight-control partition and is validated against the JSON Schema
by CI, but **no backend has realized it yet**: x86-64 realization is
Planned (M1), NG-ULTRA realization is Planned (M2), HPSC is Research
(M4).
```

```yaml
partition:
  id: flight-control        # stable identity across all three targets
  name: Flight Control
  criticality: high         # highest semantic class short of "critical"
  trust_domain: flight

execution:
  cpu_set: [0]              # pinned to cpu 0
  scheduling:
    policy: fixed_priority  # static priority - no time-slicing between partitions
    priority: 10
  timing_budget:
    period_us: 1000         # 1 ms control period
    budget_us: 300          # 300 µs CPU budget per period

memory:
  regions:
    - name: code
      size: 8M
      permissions: rx       # execute + read; no self-modification
    - name: data
      size: 16M
      permissions: rw

devices:
  ownership:
    - uart0
    - spw0

interrupts:
  owned:
    - timer0
    - irq12

dma:
  permitted_regions:
    - flight_buffer

communication:
  endpoints:
    - name: telemetry
      max_message_size: 1024
      max_rate_hz: 100      # bounded channel - see spec §5

startup:
  boot_artifact: gomr-flight.img
  dependencies: []          # boot-order root of this example

security:
  image_identity: sha256:...  # pinned content identity (illustrative)
  secure_boot_required: true

recovery:
  watchdog: true
  restart_policy: restart
  safe_state: predefined
  escalation_policy: supervisor

requirements:
  - GMR-FLIGHT-CPU-001
  - GMR-FLIGHT-MEM-002

verification:
  required_tests:
    - cpu_isolation
    - memory_isolation
    - irq_isolation
    - timing_bound
```

## Why each group matters

| Group              | Contractual concern it serves                            |
| ------------------ | ---------------------------------------------------------- |
| `partition`          | identity + semantic class (criticality, trust domain)        |
| `execution`          | execution + isolation (temporal)                            |
| `memory`             | isolation (spatial)                                         |
| `devices`/`interrupts`/`dma` | ownership-based isolation                       |
| `communication`      | bounded inter-partition exchange                            |
| `startup`            | boot order                                                  |
| `security`           | image identity -> secure supply chain                       |
| `recovery`           | partition-level recovery contract                           |
| `requirements`/`verification` | assurance traceability                             |

Target-side reading (how each target *may* realize this contract - always
subject to backend documents and validation):

* **x86-64** [platform](../../platforms/x86-64) - Xen backend (M1):
  pinned vcpu, pinned memory, PIRQ/direct device assignment, Inter-Processing
  Bounded Channel (this wording is a target-specific expression, not part of
  the contract).
* **NG-ULTRA** [platform](../../platforms/ng-ultra) - XNG/XtratuM
  backend (M2): partition slot, static scheduler, dedicated IRQ routing.
* **HPSC** [platform](../../platforms/hpsc) - research (M4): hardware
  WorldGuard partitioning plus Xen feasibility work.

The specific realization is documented per backend
([backends](../../backends/overview)), **never** in the contract - and always labeled with its current status.
