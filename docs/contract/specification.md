# Partition Contract v1 - Specification

This is the field reference for **Partition Contract v1**, frozen with
milestone M0. Fields are grouped as they appear in YAML. Normative status:
the JSON Schema in
`schemas/partition-contract.schema.json` is the machine-checkable form of
this page; if the two ever disagree, an ADR decides which side changes -
they must never silently diverge.

The running example in this spec is
`examples/*/flight-control.yml` - see
[the annotated example](examples/flight-control).

## 1. Identity

```yaml
partition:
  id: flight-control        # machine identifier
  name: Flight Control      # human display name
  criticality: high         # low | medium | high | critical
  trust_domain: flight      # free-form domain label
  capabilities_required:    # backend-neutral capability tags
    - cache_partitioning
```

| Field                    | Type   | Required | Meaning                                    |
| ------------------------ | ------ | -------- | -------------------------------------------- |
| `partition.id`             | string | yes  | unique partition identifier; must stay stable across targets |
| `partition.name`           | string | yes  | display name                                 |
| `partition.criticality`    | enum   | yes  | `low`, `medium`, `high`, `critical` - drives how strictly the backend must realize the isolation semantics |
| `partition.trust_domain`   | string | yes  | `flight`, `service`, `platform`, or custom   |
| `partition.capabilities_required` | str[] | no | capability tags the target backend must cover (checked against its Capability Manifest; partial match = waiver, no match = build fails - no silent semantic downgrade) |

```{note}
`criticality` and `trust_domain` are *semantic* tags. The contract does not
say *how* a `high`/`critical` partition is protected on a given target -
the backend (plus the backend profile) decides the enforcement mechanism.
```

## 2. Execution

```yaml
execution:
  cpu_set: [0]
  scheduling:
    policy: fixed_priority
    priority: 10
  timing_budget:
    period_us: 1000
    budget_us: 300
    wcet_bound_us: 300      # explicit WCET bound, or null/omitted
    wcet_evidence_class: measured
```

| Field                             | Type   | Required                     | Meaning                        |
| --------------------------------- | ------ | ---------------------------- | ------------------------------ |
| `execution.cpu_set`                 | int[]| yes                        | cpus the partition may run on  |
| `execution.scheduling.policy`       | string | yes                        | e.g. `fixed_priority`; policy names are target-agnostic, the set may grow by ADR |
| `execution.scheduling.priority`     | int   | yes (for fixed-priority policies) | static priority          |
| `execution.timing_budget.period_us` | int   | no                           | period of the recurring budget, µs |
| `execution.timing_budget.budget_us` | int   | no                           | CPU budget per period, µs      |
| `execution.timing_budget.wcet_bound_us` | int\|null | no                     | explicit WCET bound in µs; absent/null = no bound claimed |
| `execution.timing_budget.wcet_evidence_class` | enum | no | `proven` (formal/static WCET analysis) \| `measured` (validated under a defined stress pattern) \| `unbounded` |

The timing budget is a **declaration** of the required temporal envelope.
Whether the target realizes it (and with what fidelity) is measured - see
[Temporal isolation](../validation/temporal-isolation). Never treat the
presence of a budget as a WCET certification, and never document
`measured` as `proven`: the two classes mean different things
([evidence model - timing evidence
classification](../assurance/evidence-model)).

## 3. Memory

```yaml
memory:
  regions:
    - name: code
      size: 8M
      permissions: rx
    - name: data
      size: 16M
      permissions: rw
```

| Field                           | Type   | Required | Meaning                  |
| ------------------------------- | ------ | -------- | ------------------------- |
| `memory.regions`                  | list  | yes  | named memory regions      |
| `memory.regions[].name`           | string | yes  | region label              |
| `memory.regions[].size`           | string | yes  | human-readable size (e.g., `8M`, `512K`) |
| `memory.regions[].permissions`    | string (r/w/x flags) | yes | per-region permissions |

Region names are referenced elsewhere (e.g., `dma.permitted_regions`) -
they are the portable "address-space geometry" of the partition.

## 4. Devices, interrupts, DMA

```yaml
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
```

| Field                     | Type   | Required | Meaning                                         |
| ------------------------- | ------ | -------- | ------------------------------------------------ |
| `devices.ownership`         | str[]| no   | devices the partition owns (exclusively)          |
| `interrupts.owned`          | str[]| no   | interrupts owned by the partition; one interrupt is owned by at most one partition |
| `dma.permitted_regions`     | str[]| no   | memory regions DMA may touch                     |

## 5. Communication

```yaml
communication:
  endpoints:
    - name: telemetry
      channel: sampling
      max_message_size: 1024
      max_rate_hz: 100
      latency_budget_us: 100
      buffer_ownership: consumer
```

| Field                                        | Type  | Required | Meaning                |
| -------------------------------------------- | ----- | -------- | ------------------------ |
| `communication.endpoints`                        | list | no   | declared cross-partition channels |
| `communication.endpoints[].name`                 | str  | yes  | endpoint label           |
| `communication.endpoints[].max_message_size`     | int  | yes  | bytes per message        |
| `communication.endpoints[].max_rate_hz`          | num  | yes  | maximum message rate (Hz) |
| `communication.endpoints[].channel`               | enum | no   | `sampling` (last-value-wins) \| `queuing` (bounded queue) - a channel class, not a transport |
| `communication.endpoints[].latency_budget_us`     | int  | no   | end-to-end latency budget (µs) |
| `communication.endpoints[].buffer_ownership`      | enum | no   | `producer` \| `consumer` \| `shared` |
| `communication.endpoints[].overflow_policy`       | enum | no   | queuing channels: `block` \| `drop_oldest` \| `drop_newest` \| `fault` |

The channel class is the *semantic* of the endpoint; which mechanism
implements it on a target (shared-memory region, hypervisor-mediated port,
grant table, ...) is backend implementation detail - see [contract
overview](overview).

Communication between partitions runs **only** over declared endpoints.
ROS 2 traffic (where present) maps onto these endpoints; it is *not* an
implicit topic graph crossing partition boundaries.

## 6. Startup

```yaml
startup:
  boot_artifact: gomr-flight.img
  dependencies: []
```

| Field                  | Type   | Required | Meaning                     |
| ---------------------- | ------ | -------- | ----------------------------- |
| `startup.boot_artifact`    | string | yes  | image/artifact identifier     |
| `startup.dependencies`     | str[]  | yes  | partition ids that must start first (empty = none) |

`dependencies` together with `boot_artifact` defines the boot order - the
contractual "startup" concern from the core definition.

## 7. Security

```yaml
security:
  image_identity: sha256:...
  secure_boot_required: true
```

| Field                         | Type  | Required | Meaning                          |
| ----------------------------- | ----- | -------- | ---------------------------------- |
| `security.image_identity`         | str | yes  | content identity of the partition image |
| `security.secure_boot_required`   | bool | yes  | whether the boot path must verify the image identity |

`update` / `rollback` semantics (part of the conceptual minimum field set)
are carried in v1 by [GoMyRobotSecure](https://gomyrobot.com/products/secure/) / [GoMyRobotBSP](https://gomyrobot.com/products/bsp/) metadata; the contract
pins `image_identity` so those processes have a stable target.

## 8. Recovery

```yaml
recovery:
  watchdog: true
  restart_policy: restart
  safe_state: predefined
  escalation_policy: supervisor
  guard_independence_stage: 0
```

| Field                      | Type   | Required | Meaning                              |
| -------------------------- | ------ | -------- | -------------------------------------- |
| `recovery.watchdog`           | bool | yes  | contractual heartbeat required           |
| `recovery.restart_policy`     | str  | yes  | `restart` \| `safe_state` \| escalate-style policy |
| `recovery.safe_state`         | str  | yes  | predefined fallback state               |
| `recovery.escalation_policy`  | str  | yes  | who decides on failed recovery (e.g. `supervisor`) |
| `recovery.guard_independence_stage` | enum | no | `0` (co-resident software Guard) \| `1` (companion MCU / system controller) \| `2` (validated, per-fault timing in the evidence graph) - every recovery claim records the stage it was demonstrated under |

Semantics are specified here; the independent mechanism that *enforces*
them belongs to [GoMyRobotGuard](https://gomyrobot.com/products/guard/) (ADR-0011) -
[Recovery model](../architecture/recovery-model) and [independence
staging](../components/gomyrobotguard).

## 9. Requirements and verification

```yaml
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

These two groups are the traceability hooks consumed by [GoMyRobotVerify](https://gomyrobot.com/products/verify/)
and [GoMyRobotAssure](https://gomyrobot.com/products/assure/) ([evidence
model](../assurance/evidence-model)). Requirement identifiers follow the
`GMR-<CONTEXT>-<AREA>-<NNN>` scheme; test names are stable slugs.

## Non-goals of the contract

The contract intentionally does **not** express:

* backend identifiers (`xen_domN`, `xtratum_partition_id`, …) - they live
  in the **backend profile**
* image *contents* - only image *identity*
* network-level topology - only declared endpoints with bounds
* any certification claim - the contract is evidence *input*, not
  evidence