# Publications

Status of this page: **no paper has been published from this project as
of M0.** This page records the *planned* contribution directions and their
scope. Anything published later must trace to milestone artifacts; until
then, treat everything below as working titles with proposed scope.

## Planned paper 1

### "A Portable Partition Contract and Measurement Framework for
Mixed-Criticality Space Computing"

Initial experimental scope:

```text
x86-64 + Xen
        vs.
NG-ULTRA + XNG/XtratuM
```

Comparison dimensions:

* partition semantics
* memory isolation
* timing
* communication
* boot reproducibility
* fault containment
* deployment complexity

HPSC then becomes the next-generation extension (M4-onward data). Driver
milestones: M1 → M2 (the same conceptual flight partition on both targets);
the measurement program starts at M3.

## Planned paper 2

### "Measuring Multi-Channel Interference on Heterogeneous Space
Computing Platforms"

Platforms: x86-64, NG-ULTRA, HPSC (when M4 data exists).
Interference channels: CPU, cache, memory, DMA, interrupts, I/O.
Output form (a reproducible benchmark, not a board-specific performance
report):

```text
Stressor
  ↓
latency
jitter
bandwidth
deadline impact
containment
```

## Planned paper 3

### "Assumption Portability for Heterogeneous Flight Software
Partitioning"

Question:

> When the same conceptual partitioned system moves between x86-64,
> NG-ULTRA, and HPSC, how much of the verification and assurance argument
> can be preserved automatically?

Driver milestones: M5 (evidence feeds in automatically), M6 (the same
conceptual system demonstrated on multiple heterogeneous targets).

## Relationship to the agenda

* All three papers are downstream artifacts of the research agenda
  ([agenda](agenda)); none is initiated independently of the milestones.
* Publication readiness criteria (proposed): at least one measured result
  per paper that traces to a named milestone deliverable, a reproducible
  experiment description, and an honest limitations section. These
  criteria are goals, not claims to be met at M0.
