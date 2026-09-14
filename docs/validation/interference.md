# Validation: Interference

Interference is the strongest research area in the project (Research
Problem 2). This page is the GoMyRobotOS-side measurement methodology of
the **M3 Interference laboratory** (GMR-INTERF v1); the physical
experiment infrastructure is [GoMyRobotBench](../components/gomyrobotbench).

## The question

A partition does not interfere with another partition only through the
CPU. It can interfere through:

```text
CPU
cache
memory controller
interconnect
DMA
interrupts
I/O
accelerators
```

The methodology is: for each channel, stress one partition, measure the
damage to another, and record which channels actually move the needle on
*which backend*. The answer is **different per backend by design**, that
delta is what Research Problem 1 (portable semantics) consumes.

## The experimental design

```text
Flight partition
       │
       │ latency / jitter
       ▼
    monitored
       ▲
       │
       │ stress
Service partition
 ├── CPU
 ├── cache
 ├── memory
 ├── DMA
 ├── IRQ
 └── I/O
```

* **Monitored partition:** the contract's `timing_budget` and declared
  communication endpoints define the baseline.
* **Stressor partition:** one channel stressed at a time (then combined),
  with its own contract bounding its own resources, it stresses *within
  its own contractual envelope*, which is what makes the comparison fair
  and the result contractual.
* **Platform sweep:** x86-64 → NG-ULTRA → HPSC, same conceptual
  partitions throughout (that invariance is deliberate: it is what makes
  results comparable across targets).

## Measured quantities

| Quantity                  | Interpretation for the contract                          |
| ------------------------- | ----------------------------------------------------------|
| latency                     | window delay vs budget                                  |
| jitter                      | variance of the window, the flight-relevant number        |
| throughput degradation      | endpoint rate vs `max_rate_hz` declaration                |
| cache effects               | which cache policies (if any) absorb the damage            |
| memory bandwidth            | can the declared memory regions hold their envelope?     |
| interrupt latency           | does `interrupts.owned` actually isolate interrupt delivery? |
| DMA interference            | does `dma.permitted_regions` semantically extend to DMA timing? |

## Status

```text
methodology:           specified (this page, M0)
GMR-INTERF v1:         Status: Planned (M3)
any interference data: none exists yet
```

```{warning}
No number on any GoMyRobotOS page is a measured interference result until
an M3 (or later) artifact publishes it. "Low interference" and similar
phrases are *forbidden* phrasings in this documentation at M0, this is an
anti-claim rule as much as a methodology.
```
