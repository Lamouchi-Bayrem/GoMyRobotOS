# Research problems

The five research problems (RP1-RP5) are defined in the frozen M0
architecture baseline, documented in this site.
They are **open problems with proposed measurement programs**, none is
solved, and none is presented here as a capability.

## RP1 Portable partition semantics

Compare the *same conceptual partition* realized on:

```text
x86-64 + Xen
        ↓
NG-ULTRA + XNG/XtratuM
        ↓
HPSC + Xen / WorldGuard research
```

and measure, at the partition level:

* CPU allocation
* memory isolation
* interrupt ownership
* device ownership
* communication
* startup behavior
* recovery behavior

The question:

> **Which partition semantics are genuinely portable, and which are
> inherently hardware/backend-specific?**

That is the core architectural research contribution: the *difference
surface* between backends, made observable and comparable by the IR.

**Method note.** "Same conceptual partition" means the identical
contract (see `examples/*/flight-control.yml`); "realized" means a backend
that validates and boots it. Differences that emerge, a field that maps
differently on two backends, a guarantee one mechanism gives that another
cannot, a hardware property no hypervisor exposes, *define* the
semantics worth documenting. Contract v1 is expected to evolve as RP1
produces findings (via ADR), and that evolution is part of the result:
the frozen M0 contract is the *starting hypothesis*, not the endpoint.

## RP2 Multi-channel interference

A partition can interfere through:

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

Experimental shape (detailed in [validation/interference]
(../validation/interference)): a monitored flight partition, a
stressor partition, one stress channel at a time, then combined; the
platform sweep x86-64 → NG-ULTRA → HPSC; GMR-INTERF v1 is the M3 vehicle.

Measured per channel: latency, jitter, throughput degradation, cache
effects, memory bandwidth, interrupt latency, DMA interference.

Why it matters: a contract that says "300 µs budget" is only as strong as
the list of channels that *cannot* break it, and that list is different
per backend. HPSC is particularly here, because WorldGuard extends
partitioning across multiple hardware resource classes, more channels to
study, and potentially more to *close*.

## RP3 Fault containment and recovery

Standard fault model and the measured intervals
(T_detect / T_contain / T_recover / T_resume) are documented in
[validation/recovery]
(../validation/recovery). The full fault-class list: application crash,
illegal memory access, illegal MMIO, DMA violation, interrupt abuse, CPU
starvation, resource exhaustion, service-domain crash, management-domain
failure, watchdog timeout, corrupted image.

The research question is not "does recovery happen" (the contract
prescribes when it must) but: **can failures be detected, contained, and
recovered independently of the failed partition, and is that
independence *measured* rather than asserted?** The independence property
is exactly the ADR-0011 boundary: GoMyRobotOS specifies, [GoMyRobotGuard](https://gomyrobot.com/products/guard/)
implements, and the measurement decides whether the two are doing their
jobs.

## RP4 Faults caused by the space environment

> **Ownership: this is a [GoMyRobotFault](https://gomyrobot.com/products/fault/) / [GoMyRobotBench](https://gomyrobot.com/products/bench/) / /[GoMyRobotAssure](https://gomyrobot.com/products/assure/)
> research stream, not a GoMyRobotOS subsystem.**

Question:

> How well do software-level fault models predict containment and recovery
> behavior for space-relevant hardware fault mechanisms?

Fault families considered: SEU-like bit flips, register corruption, memory
corruption, configuration corruption, transient execution faults,
communication corruption, watchdog events.

The ladder: software fault models → QEMU/emulation (models *effects*,
never "radiation") → FPGA/HIL → real NG-ULTRA / HPSC → radiation/SEE
testing → correlation. GoMyRobotOS's role in this stream is
contractual: declare recovery semantics, record what recovery actually
did. NG-ULTRA's radiation-hardened-by-design mechanisms (EDAC,
configuration scrubbing, memory/configuration protection) are the
hardware truth the models must correlate with.

## RP5 Assurance portability

The most commercially interesting problem. Given:

```text
Partition P1
      │
      ├── x86-64
      ├── NG-ULTRA
      └── HPSC
```

> **How much of the verification and assurance argument remains valid
> when the deployment platform changes?**

GoMyRobotOS's role: emit the machine-readable metadata that makes the
question answerable -

```text
partition configuration
hardware profile
backend version
image hash
resource allocation
required tests
deployment identity
```

- and GoMyRobotAssure turns that into the actual evidence graph
([evidence-graph](../assurance/evidence-graph)). The "retainable core
vs. re-measure set" split is the deliverable of RP5 as research.
## Status of all five

| Problem | Status        | Milestones        |
| ------- | ------------- | ----------------- |
| RP1     | `Research`    | M1, M2, M4, M6    |
| RP2     | `Research`    | M3                |
| RP3     | `Research`    | M1 (basic), M3, M5 |
| RP4     | `Research` (external products own it) | via M3/M5 |
| RP5     | `Research`    | M5, M6            |

```{important}
These are research problems, not solved properties. No measurement
listed in this section has been performed at M0, and no publication
based on them has existed. If a number, a claim, or a graphic appears
later, it must trace to a real artifact named in the [milestones]
(../milestones/overview).
```

## How problems feed documents

* RP1 → [backend model](../architecture/backend-model),
  [IR](../architecture/ir), platform pages
* RP2 → [interference](../validation/interference), GMR-INTERF (M3)
* RP3 → [recovery model](../architecture/recovery-model),
  [fault injection](../validation/fault-injection),
  [recovery](../validation/recovery)
* RP4 → [GoMyRobotFault](../components/gomyrobotfault)
* RP5 → [evidence model](../assurance/evidence-model),
  [evidence graph](../assurance/evidence-graph)

Planned contribution toward these problems: [publications]
(publications).