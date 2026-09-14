# Assurance: Reproducibility

Reproducibility is the minimum discipline that makes any assurance claim
*reviewable* - if a run cannot be reproduced, its evidence is an
assertion.

## Three reproducibility pillars in GoMyRobotOS

### 1. Reproducible boot

The same contract + the same backend + the same target hardware profile
must produce the same booted system. M1 lists "reproducible boot" as a
test *before* anything fancier - and the M1 gate is "boots and isolates
partitions": a system that cannot reproducibly boot has no further
validation credibility at all.

### 2. Reproducible measurements

M3's gate is literal: **interference measurements are reproducible** -
same stress recipe, same monitored partition, same backend, same numbers
(within documented tolerance) on rerun. Measurement reproducibility is a
gate, not a byproduct, because the entire research program is built on
comparing numbers across targets.

### 3. Reproducible artifacts

Every piece of evidence carries the identity data the [evidence
model](evidence-model) lists: image hashes, backend version,
deployment identity, hardware profile. BSP's
`hashes` and `build metadata` outputs exist specifically for this: two
people with the same manifest should be able to reconstruct what ran -
not just what *might* have run.

## How far reproducibility reaches

```text
reproducible deployment identity   ← this section
        +
reproducible execution semantics   ← backend's problem, contract's hook
        +
reproducible environment           ← BSP/CI's problem (x86-64/QEMU first)
        =
reviewable evidence
```

GoMyRobotOS's obligation is the first row (it owns the contract, the
deployment metadata, the identity pins). It *coordinates* the other two;
it does not own them.

## Status

```text
structure (what must be pinned):   defined (M0)
first reproducible boot:           Status: Planned (M1)
reproducible interference runs:    Status: Planned (M3 gate)
```

```{note}
"Reproducible" here is an engineering property: same input → same
observed behavior within tolerance. It is **not** a certification
property and is never labeled as one in this documentation.
```
