# Validation: Temporal isolation

**Contract hooks:** `execution.cpu_set`, `execution.scheduling`,
`execution.timing_budget` (see
[contract spec](../contract/specification)).

## What "temporal isolation" means here

A partition's declared timing envelope must hold *independently of what
other partitions are doing*. The contractual claim is:

> Given the declared cpu-set, static priority, and timing budget, the
> partition's execution window is bounded.

What must then be *measured*: whether the target backend realizes that
claim, with what fidelity, and under what interference.

## What gets measured

| Quantity              | Meaning                                              |
| --------------------- | ---------------------------------------------------- |
| deadline impact         | does budget usage stay within `budget_us`?          |
| jitter                  | variance of end-to-end window vs nominal budget      |
| latency under stress    | latency of the partition's callbacks while stressed  |
| priority preemption     | does a lower-criticality partition disturb the window? |

## Experimental plan (research, not implemented)

The temporal side of the M3 interference laboratory runs a
flight-style partition (monitored) against service-style stressors
(CPU-bound, cache-thrashing, memory-bandwidth, DMA, IRQ, I/O) and records
the quantities above, on x86-64 first, then repeated on NG-ULTRA, then
HPSC as feasible:

```text
Flight partition            (monitored: latency / jitter vs declared budget)
       ▲
       │ stress
Service partition
 ├── CPU
 ├── cache
 ├── memory
 ├── DMA
 ├── IRQ
 └── I/O
```

See [Interference](interference) for the full multi-channel design.

## Status

```text
contract semantics (budget, policy):  specified (M0)
measurement harness:                  Status: Planned (M3)
any timing result:                    none exist yet
```

```{warning}
A declared `timing_budget` is a **requirement**, not a measurement. No
page in this repository treats a budget as a demonstrated WCET.
```
