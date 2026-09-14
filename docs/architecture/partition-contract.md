# The Partition Contract

## The central innovation

The central artifact of GoMyRobotOS is the **Partition Contract** - the
machine-readable execution contract that decouples *what a partition is
allowed and required to do* from *which mechanism realizes it*.

The abstraction is deliberately **not**:

> *"Generate a Xen configuration."*
> *"Generate an XNG configuration."*

The abstraction **is**:

> *"Define what a partition is allowed and required to do."*

## Why this is the center of the architecture

1. **Portability is the research claim.** If the same partition cannot be
   described once and realized on multiple targets, the project has no
   research contribution. The contract is the object being compared across
   x86-64 + Xen, NG-ULTRA + XNG/XtratuM, and HPSC + hardware partitioning -
   see [Research problem 1](../research/research-problems).
2. **Assurance depends on it.** Machine-readable configuration, image
   identity, required tests, and requirement identifiers are declared *in*
   the contract, which is what makes evidence collection systematic
   ([assurance/evidence-model](../assurance/evidence-model)).
3. **Recovery is contractual.** Watchdog, restart policy, safe state, and
   escalation are contract fields, so recovery behavior is auditable per
   partition before any fault occurs
   ([recovery-model](recovery-model)).

## Minimum conceptual fields

The v1 contract carries at least these groups (full reference:
[specification](../contract/specification)):

```text
identity
criticality
trust domain

CPU
scheduling
timing budget

memory
permissions
cache policy

devices
interrupts
DMA

communication

startup
dependencies

security
image identity
secure boot
update
rollback

recovery

requirements
tests
evidence references
```

## The hard rule: no backend syntax

The contract must **never** contain backend-specific syntax such as:

```text
xen_dom0
xtratum_partition_id
xng_specific_option
```

unless the property genuinely cannot be expressed at the portable semantic
layer. Backend-specific information belongs in the **backend profile**
consumed by GoMyRobotBSP, not in the contract. This rule is what separates
"GoMyRobotOS is a platform" (ADR-0002, ADR-0003) from "GoMyRobotOS is a set
of hypervisor configuration generators."

## Contract ≠ IR

This page describes the **Partition Contract**: the user-facing,
declarative specification - what a partition may do, with requirements.
The **GoMyRobotOS IR** (see [IR](ir)) is the internal, normalized
compiler representation every backend consumes. The two are related but
must not be used interchangeably in documents, interfaces, or commits.

## Status

```text
Partition Contract v1 (specification):  frozen with M0 documentation
JSON Schema (schemas/):                 v1, machine-checkable
Illustrative examples:                  examples/{x86-64,ng-ultra,hpsc}
Parser / validator:                     Status: Planned (M1)
```

```{note}
The JSON Schema shipped in this repository is the M0 deliverable that makes
"described without mentioning Xen, XNG, or any board-specific
implementation" (the M0 gate) checkable. The validator that enforces it at
build time lands at M1.
```

## Example

A complete, field-annotated example contract is
[contract/examples/flight-control](../contract/examples/flight-control).
