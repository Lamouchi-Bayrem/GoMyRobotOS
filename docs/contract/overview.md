# Partition Contract - Overview

The Partition Contract is the central artifact of GoMyRobotOS: a
machine-readable, **hypervisor-independent** description of what a
partition is allowed (and required) to do.

```{important}
The question a contract answers is not *"how do I make a Xen domain?"* or
*"how do I make an XtratuM partition?"* - it is *"what may this execution
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

## Two rules to remember

1. **No backend syntax.** The contract must not contain `xen_dom0`,
   `xtratum_partition_id`, `xng_specific_option`, or similar. Backend data
   lives in the **backend profile** consumed by GoMyRobotBSP.
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
