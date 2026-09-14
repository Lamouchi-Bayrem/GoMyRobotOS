# Frozen baseline scope notes

This page is **normative** for the M0 baseline. It records the naming
rule between the two central objects and what the first architecture
baseline deliberately keeps out of scope.

## Naming rule

The **Partition Contract** is the user-facing declarative
specification. The **GoMyRobotOS IR** is the internal compiler
representation. Related, but they must not be used interchangeably, see
[The Partition Contract](partition-contract) and
[GoMyRobotOS IR](ir).

## Not in the v1 baseline

These concepts are excluded from the core v1 baseline; the schema and the
documentation must not imply otherwise:

* `power`, not part of the v1 contract; reserved only, and not enforced
  by any backend yet
* `fleet`, one flight computer; multi-node synchronization, voting and
  failover are future work
* transport mechanisms, grant tables, event channels, virtio and
  shared-memory ports are backend implementation rules, not contract
  semantics
* per-field certification mapping, GoMyRobotOS maps evidence onto
  existing standards (ECSS Q ST 80C, ECSS E ST 40C, and the ARINC 653 /
  DO-297 lineage where useful); it creates no new certification standard
* hardware-specific assumptions in the core architecture, platform
  features such as system controllers, scrubbing and ECC belong to the
  Hardware Profile and to Guard stage claims
* AI / accelerator criticality classes as contract fields, research
  direction only, deferred to a future contract revision

## Platform position

> **GoMyRobotOS is not an OS that happens to support several hypervisors.
> It is a portable partition and assurance platform that compiles one
> flight-system contract into different execution environments and
> produces evidence that the intended isolation and recovery properties
> were actually realized.**

## Status

```text
Frozen with M0. Changes by ADR only.
```