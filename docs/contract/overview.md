# Partition Contract Overview

The Partition Contract is the central artifact of GoMyRobotOS: a
machine-readable, **hypervisor-independent** description of what a
partition is allowed (and required) to do.

```{important}
The question a contract answers is not *"how do I make a Xen domain?"* or
*"how do I make an XtratuM partition?"*, it is *"what may this execution
domain do, and what must it do, regardless of mechanism?"*
```

## Where the contract sits

```text
                    GoMyRobotOS
                         │
            Partition Contract        ← this section
                         │
                         ▼
                       IR
                         │
               Target Backend
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
           Hypervisor          Bare metal /
           / separation        future backend
```

The contract is the **author-facing** input of the whole pipeline; the IR
is the stable machine representation; the backend is the only layer that
may know mechanism names.

## What this section contains

| Page                                                        | Content                                    |
| ----------------------------------------------------------- | ------------------------------------------- |
| [Specification](specification)                           | Field reference for Contract v1              |
| [Schema](schema)                                         | Location and use of the JSON Schema          |
| [Example: flight-control](examples/flight-control)       | Complete, field-annotated contract           |
| Repository `schemas/partition-contract.schema.json`         | Machine-checkable schema v1 (in the repo)    |
| Repository `examples/{x86-64,ng-ultra,hpsc}/flight-control.yml` | Same conceptual partition, three targets        |

## Channel semantics

Communication endpoints are typed by **channel class**, not by transport
mechanism, modeled on the ARINC 653 sampling/queuing port distinction:

* **`sampling`**: periodic state data; last value wins; bounded staleness.
  Used for continuously updated telemetry-style data (joint state, sensor
  readings).
* **`queuing`**: event or command data; bounded queue depth; explicit
  overflow policy. Used for commands, mode transitions and discrete
  events.

Every channel declaration carries the same properties:

| Property            | Meaning                              | Examples of values           |
| ------------------- | ------------------------------------ | ---------------------------- |
| `max_message_size`  | upper bound on message size          | `512` (bytes)                 |
| `max_rate_hz`         | maximum message rate                 | `1000` (Hz)                   |
| `latency_budget`    | end-to-end budget                    | `100` (us)                    |
| `buffer_ownership`  | who owns the message buffer          | `producer`, `consumer`, shared |
| `overflow_policy`   | behavior when the queue is full      | `block`, `drop_oldest`, `drop_newest`, `fault` |

Each backend maps these semantics to its own mechanism (shared-memory
regions, hypervisor-mediated ports, grant tables, and so on). The
transport choice is **backend implementation detail**, declared in the
backend's documentation, never in the contract.

## Capability requirements

A contract may carry a `capabilities_required` list: backend-neutral
capability tags (for example, cache partitioning, DMA remapping, interrupt
pass-through, the sampling / queuing channel classes above) that the target
backend's Capability Manifest must cover. The three-way check and the
no-silent-downgrade rule are defined in the
[Backend model](../architecture/backend-model) (section "Backend
Capability Manifest").

## Two rules to remember

1. **No backend syntax.** The contract must not contain `xen_dom0`,
   `xtratum_partition_id`, `xng_specific_option`, or similar. Backend data
   lives in the **backend profile** consumed by [GoMyRobotBSP](https://gomyrobot.com/products/bsp/).
2. **Machine-checkable intent.** Every field exists either to (a) bound a
   resource, (b) declare an ownership/permission, (c) order startup, or
   (d) declare a recovery/reassurance hook. If a field serves none of
   those, it does not belong in the contract.

## Status

```text
Contract v1 specification:     frozen with M0 documentation
JSON Schema v1:                shipped in the repository (schemas/)
Parser / validator:            Status: Planned (M1)
Per-target example files:      illustrative (examples/)
```
