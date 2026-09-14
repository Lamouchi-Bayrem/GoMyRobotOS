# Partition Contract v1 - Schema

## Location

```text
schemas/partition-contract.schema.json   (repository root)
```

The schema is the **machine-checkable** form of the
[specification](specification). Both were frozen together at M0 and must
evolve together under ADR control.

## Format

* JSON Schema, draft 2020-12.
* Describes the same field groups as the specification: identity
  (`partition`), `execution`, `memory`, `devices`, `interrupts`, `dma`,
  `communication`, `startup`, `security`, `recovery`, `requirements`,
  `verification`.
* The schema intentionally has **no backend-specific keys**: no
  `xen_*`, `xtratum_*`, `xng_*` properties exist in v1 - that is the
  machine-level expression of ADR-0002/0003 ("hypervisors are backends").

## What the schema enforces today

* required structural groups (`partition`, `execution`, `memory`,
  `recovery`)
* value types (ints, strings, booleans, lists)
* the `criticality` enum: `low` / `medium` / `high` / `critical`
* non-empty message bounds on communication endpoints
* the rule that backend identifiers are not legal keys

Open for ADR at M1+: whether `additionalProperties` stays closed at each
level (v1 keeps the top-level contract closed to the known groups).

## How the schema is validated

The schema is exercised by the CI
`schema` job (`.github/workflows/docs.yml`): each
`examples/<target>/flight-control.yml` is loaded and validated against the
schema on every push. The *build-time contract validator* used by real
deployments (part of the M1 parser/validator) will reuse the same schema.

```{note}
Until M1 ships that validator, "a contract is valid" means:
1. it validates against `schemas/partition-contract.schema.json`, and
2. a human has checked it against the [specification](specification).
```
