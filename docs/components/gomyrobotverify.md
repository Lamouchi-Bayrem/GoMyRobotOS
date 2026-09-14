# GoMyRobotVerify

Full verification **does not belong inside GoMyRobotOS**
([ADR-0012](../development/architecture-decisions)).
Verification is an external platform service that consumes GoMyRobotOS
artifacts.

## The flow

```text
GoMyRobotOS
     │
     ├── configuration manifest
     ├── required properties
     ├── test requirements
     └── deployment metadata
             │
             ▼
     GoMyRobotVerify
             │
      ┌──────┼───────┐
      ▼      ▼       ▼
    tests  results  coverage
```

## What GoMyRobotVerify owns

* test planning
* test execution
* result processing
* coverage
* regression
* requirement-to-test relationships

## What GoMyRobotOS contributes to verification

Every partition contract carries the traceability hooks Verify needs:

* `requirements:` - requirement identifiers the partition must satisfy
  (e.g., `GMR-FLIGHT-CPU-001`, `GMR-FLIGHT-MEM-002` in the v1 example)
* `verification.required_tests:` - the tests the contract declares as
  mandatory (e.g., `cpu_isolation`, `memory_isolation`, `irq_isolation`,
  `timing_bound` in the v1 example)
* configuration manifest, image identity, and deployment artifacts -
  what a test run is running (see [BSP
  outputs](gomyrobotbsp))

Verification's declared scope (reproducible boot, functional runtime
validation, temporal/spatial isolation, interference, fault injection,
recovery timing) is documented in the
[Validation section](../validation/methodology).

## Boundaries

* [GoMyRobotVerify](https://gomyrobot.com/products/verify/) decides *how* verification runs (harnesses,
  environments, schedules, regression policy).
* GoMyRobotOS decides *what* must be verified per partition (contract
  requirements) and *what ran* (deployment metadata).
* Neither claims certification. Verification execution and result
  aggregation are engineering activities; any assurance statement derived
  from them belongs to [GoMyRobotAssure](https://gomyrobot.com/products/assure/), and no assurance statement exists
  at M0 at all.

`Status: External product; integration with GoMyRobotOS artifacts is
planned (M5). Not implemented in this repository.`
