# Research agenda

## The study question

> **Can one machine-readable partition contract describe and validate
> equivalent mixed-criticality execution semantics across heterogeneous
> space computing architectures and separation mechanisms?**

The important word is **equivalent** — not *identical*. The research
program is about determining **which properties can remain invariant**
when hardware, separation mechanism, and OS stack change.

## The problem set

| # | Problem                                           | Question in one line                                            |
| - | ------------------------------------------------- | ----------------------------------------------------------------|
| RP1 | Portable partition semantics                       | Which contract fields retain equivalent meaning on all backends? |
| RP2 | Multi-channel interference                          | How do CPU/cache/memory/DMA/IRQ/I/O contention move a critical partition's window? |
| RP3 | Fault containment and recovery                      | Can failures be detected, contained, and recovered independently of the failed partition — and in measured time? |
| RP4 | Space-environment-induced faults                     | How well do software fault models predict behavior on space-relevant hardware fault mechanisms? |
| RP5 | Assumption portability                               | When the target changes, how much of the verification/assurance case transfers automatically? |

Full treatments: [research-problems](research-problems).

```{important} These are open problems
None of RP1–RP5 is solved. They are research problems with declared
measurement programs — not capabilities, not features, not results.
No page in this documentation converts a problem statement into an
achievement claim.
```

## Where each problem lives

| Problem | Primary products involved                    | Milestones       |
| ------- | ---------------------------------------------| ----------------- |
| RP1     | GoMyRobotOS (contract/IR/backend comparison)  | M1 → M2 → M4, M6 |
| RP2     | GoMyRobotOS + GoMyRobotBench (GMR-INTERF)      | M3               |
| RP3     | GoMyRobotOS (recovery contract) + Fault + Guard | M1, M3, M5     |
| RP4     | GoMyRobotFault / Bench / Assure (not GoMyRobotOS) | via M3/M5    |
| RP5     | GoMyRobotOS (evidence inputs) + Verify + Assure | M5             |

## Milestone mapping (summary)

* **M0** — freeze the semantics under study *(this documentation)*
* **M1** — first realizable point: x86-64 + Xen
* **M2** — second realizable point: NG-ULTRA + XNG/XtratuM
* **M3** — interference laboratory (RP2)
* **M4** — HPSC research (RP1 extension; RP3 environment on RISC-V)
* **M5** — recovery + assurance integration (RP3/RP4/RP5 data plane)
* **M6** — same conceptual system across heterogeneous targets (RP1/RP5
  demonstration)

Proposed artifacts from this agenda: [publications](publications).
