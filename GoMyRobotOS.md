# GoMyRobotOS — Final Architecture

# 1. Product definition

### GoMyRobotOS

**Partition & Execution Platform for Safety-Critical Space Robotics**

GoMyRobotOS defines how a heterogeneous flight computer is divided into controlled execution domains and how those domains are described, deployed, monitored, and recovered.

It does **not** attempt to become a new kernel, a universal hypervisor, a universal BSP, or a complete verification system.

Its central artifact is a **hypervisor-independent Partition Contract**.

The contract describes:

* execution resources
* memory resources
* timing requirements
* interrupt ownership
* DMA permissions
* device ownership
* communication policies
* trust and criticality
* startup requirements
* partition-level recovery requirements

GoMyRobotOS then realizes that contract through target-specific execution backends.

The architectural principle is:

> **Describe the required execution semantics once; realize them according to the capabilities of the target platform.**

The hypervisor is therefore an **implementation backend**, not the product abstraction.

---

# 2. What GoMyRobotOS is and is not

## GoMyRobotOS is

* a partition model
* a machine-readable execution contract
* an intermediate representation
* a target-backend interface
* a partition deployment/orchestration layer
* a runtime integration layer
* a partition health/recovery interface
* a source of configuration and deployment metadata

## GoMyRobotOS is not

* RTEMS
* Linux
* ROS 2
* Xen
* XtratuM/XNG
* Yocto
* a BSP
* a simulator
* a radiation-testing framework
* a complete fault-injection platform
* a safety-case platform

Those technologies remain components of the larger GoMyRobot ecosystem.

---

# 3. Position in the GoMyRobot product stack

The clean separation is:

```text
                     GoMyRobot
                         │
       ┌─────────────────┼──────────────────┐
       │                 │                  │
       ▼                 ▼                  ▼
  GoMyRobotOS      GoMyRobotRT        GoMyRobotBSP
  partitioning       RTEMS/ROS        target/build
                         │
                         │
       ┌─────────────────┼────────────────────┐
       │                 │                    │
       ▼                 ▼                    ▼
 GoMyRobotFault   GoMyRobotBench      GoMyRobotVerify
 fault injection      HIL/test            verification
       │                 │                    │
       └─────────────────┼────────────────────┘
                         ▼
                  GoMyRobotAssure
                  evidence / safety
```

And:

```text
GoMyRobotGuard
       │
       ├── independent recovery
       └── runtime safety enforcement

GoMyRobotSim
       │
       └── simulation of flight workloads

GoMyRobotSecure
       │
       ├── secure boot
       ├── image signing
       ├── SBOM
       ├── update integrity
       └── runtime integrity
```

This prevents GoMyRobotOS from becoming an enormous "everything safety-related" product.

---

# 4. Core abstraction: Partition Contract

This is the central innovation.

Do **not** make the abstraction:

> Generate a Xen configuration.

or:

> Generate an XNG configuration.

Make it:

> Define what a partition is allowed and required to do.

For example:

```yaml
partition:
  id: flight-control
  name: Flight Control
  criticality: high
  trust_domain: flight

execution:
  cpu_set: [0]
  scheduling:
    policy: fixed_priority
    priority: 10
  timing_budget:
    period_us: 1000
    budget_us: 300

memory:
  regions:
    - name: code
      size: 8M
      permissions: rx

    - name: data
      size: 16M
      permissions: rw

devices:
  ownership:
    - uart0
    - spw0

interrupts:
  owned:
    - timer0
    - irq12

dma:
  permitted_regions:
    - flight_buffer

communication:
  endpoints:
    - name: telemetry
      max_message_size: 1024
      max_rate_hz: 100

startup:
  boot_artifact: gomr-flight.img
  dependencies: []

security:
  image_identity: sha256:...
  secure_boot_required: true

recovery:
  watchdog: true
  restart_policy: restart
  safe_state: predefined
  escalation_policy: supervisor

requirements:
  - GMR-FLIGHT-CPU-001
  - GMR-FLIGHT-MEM-002

verification:
  required_tests:
    - cpu_isolation
    - memory_isolation
    - irq_isolation
    - timing_bound
```

The example is meant to be representative; the full field set (including cache policy and update/rollback) is defined in the contract specification.

The contract describes **intent and constraints**, not backend syntax.

---

# 5. Partition Contract → IR → Backend

The internal pipeline should be:

```text
Partition Contract
       │
       ▼
Parser
       │
       ▼
Validator
       │
       ▼
GoMyRobotOS IR
       │
       ├───────────────┬────────────────┐
       ▼               ▼                ▼
     Xen            XNG/XtratuM       Future
    Backend           Backend         Backend
       │               │
       ▼               ▼
 target artifacts   target artifacts
```

The IR is important because it creates the stable internal representation between the contract and the backend.

For example:

```text
Partition
 ├── CPU resources
 ├── memory resources
 ├── interrupt resources
 ├── DMA resources
 ├── device resources
 ├── communication
 ├── timing
 ├── security
 └── recovery
```

The backend then determines how those semantics are expressed on the target.

---

# 6. Target strategy

Do not treat every possible board as a product target.

The initial GoMyRobotOS target matrix should be:

| Target     | Role                            | Status   |
| ---------- | ------------------------------- | -------- |
| x86-64     | development/reference           | Planned  |
| NG-ULTRA   | space/flight reference          | Planned  |
| PIC64-HPSC | next-generation RISC-V research | Research |

## x86-64

x86-64 is primarily a **development and reproducibility platform**, not the intended flight processor.

It gives you:

* fast iteration
* CI
* automated tests
* QEMU virtualization
* fault-injection experiments
* backend development
* reproducible regression tests

It should be the environment in which the GoMyRobotOS software architecture is developed before moving to space targets.

---

# 7. NG-ULTRA

NG-ULTRA is your first genuine space-oriented execution reference.

The platform has four Cortex-R52 cores and has an established ecosystem around RTEMS and XtratuM/XNG. Existing RTEMS work explicitly lists an ARMv8-R NG-ULTRA BSP, and NanoXplore's ecosystem includes RTEMS and XtratuM/XNG support.

Therefore the NG-ULTRA backend should initially focus on:

```text
GoMyRobotOS Contract
        ↓
GoMyRobotOS IR
        ↓
NG-ULTRA Backend
        ↓
XNG / XtratuM
        ↓
RTEMS
        ↓
GoMyRobotRT
```

This is the **flight-oriented reference implementation**.

---

# 8. PIC64-HPSC

HPSC is the next-generation research platform.

Microchip currently documents RTEMS and Xen support for PIC64-HPSC, as well as hardware virtualization and WorldGuard end-to-end spatial partitioning across cores, cache, interconnect, peripherals, and memory. The device also includes an independent system-controller processor suitable for monitoring and fault management.

But this distinction is critical:

> **Do not claim production RTEMS-on-Xen-HPSC support until you have demonstrated it.**

Instead:

```text
HPSC
 │
 ├── RTEMS
 │     └── baseline
 │
 ├── WorldGuard
 │     └── hardware isolation
 │
 └── Xen research
       ├── host bring-up
       ├── domain creation
       ├── virtual timer
       ├── interrupts
       ├── memory
       └── RTEMS guest
```

Xen's RISC-V guest support remains an active development area. Current 2026 Xen development is still adding and refining guest ISA and interrupt infrastructure, so HPSC/Xen should remain explicitly a research track rather than a claimed mature production backend.

That actually strengthens the research story.

---

# 9. GoMyRobotRT

GoMyRobotRT remains a separate product.

Its responsibility is:

```text
GoMyRobotRT
 ├── RTEMS
 ├── nano-ros (legacy name for ROS 2 on RTEMS support)
 ├── rcl/rclcpp
 ├── deterministic executors
 ├── robotics middleware
 ├── hardware abstraction
 └── flight application interfaces
```

GoMyRobotOS consumes or hosts GoMyRobotRT.

The distinction is:

> **GoMyRobotRT executes the robotics workload.**

> **GoMyRobotOS controls the execution environment in which that workload runs.**

ROS 2 is therefore **a workload**, not the central abstraction of GoMyRobotOS.

---

# 10. GoMyRobotBSP

GoMyRobotBSP owns target realization and build coordination.

It consumes:

```text
Partition Contract
      +
Hardware Profile
      +
Backend Profile
      +
Boot Profile
      +
Runtime Profile
```

and produces:

```text
boot artifacts
hypervisor configuration
RTEMS configuration
device tree / hardware description
Linux image
memory map
deployment manifest
hashes
build metadata
```

The key distinction is:

> **GoMyRobotBSP is the target realization/build system.**

It is not GoMyRobotOS.

---

# 11. Yocto's role

Yocto is **inside the target build pipeline when a Linux domain exists**.

For example:

```text
GoMyRobotBSP
      │
      ├── RTEMS build
      ├── hypervisor configuration
      └── Yocto/OpenEmbedded
              │
              ▼
         Linux image
```

The final deployment can therefore contain:

```text
Boot
├── bootloader
├── hypervisor
├── Linux service domain
│      └── Yocto-built image
├── RTEMS flight domain
│      └── GoMyRobotRT
└── deployment metadata
```

But an RTEMS-only deployment does not need Yocto.

Therefore:

> **GoMyRobotOS is not Yocto-based.**

Yocto is a **target image construction mechanism** used by GoMyRobotBSP when Linux is part of the deployment.

---

# 12. GoMyRobotGuard

Guard remains separate because its responsibility is **independent recovery and runtime safety enforcement**.

The core principle is:

> The component responsible for recovering a failed component must not depend exclusively on the failed component.

Architecture:

```text
                 GoMyRobotGuard
                       │
            ┌──────────┼──────────┐
            │          │          │
            ▼          ▼          ▼
         Flight     Service    Platform
         domain     domain      /hypervisor
            │          │          │
            └──────────┼──────────┘
                       ▼
                 Recovery action
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       restart       isolate      reset
```

On HPSC this becomes particularly interesting because the system controller can serve as an independent monitoring/fault-management mechanism.

GoMyRobotOS should expose **recovery semantics**.

GoMyRobotGuard should implement the independent recovery mechanism.

---

# 13. GoMyRobotVerify

Full verification does not belong inside GoMyRobotOS.

Instead:

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
     tests  results coverage
```

GoMyRobotVerify owns:

* test planning
* test execution
* result processing
* coverage
* regression
* requirement-to-test relationships

---

# 14. GoMyRobotFault

Fault injection also remains outside GoMyRobotOS.

GoMyRobotOS defines:

> what the partition should do when a fault occurs.

GoMyRobotFault defines:

> how the fault is generated.

Fault classes can include:

```text
CPU
memory
DMA
interrupt
I/O
communication
partition crash
watchdog
resource exhaustion
image corruption
```

## Radiation belongs here

Radiation effects should **not** be implemented as a GoMyRobotOS function.

Instead:

```text
Radiation / SEU / TID models
            ↓
      GoMyRobotFault
            ↓
     QEMU / emulator
            ↓
   target fault mechanism
            ↓
       GoMyRobotOS
            ↓
 detection → containment → recovery
            ↓
      verification evidence
```

QEMU can therefore model radiation-induced fault effects, but QEMU itself does not reproduce the physical radiation environment.

NG-ULTRA is particularly relevant because it is explicitly radiation-hardened-by-design and includes mechanisms such as EDAC, configuration scrubbing and memory/configuration protection.

The progression should eventually be:

```text
software fault model
        ↓
QEMU/emulation
        ↓
FPGA/HIL
        ↓
real HPSC / NG-ULTRA
        ↓
radiation / SEE testing
        ↓
correlation
```

---

# 15. GoMyRobotBench

Bench owns the physical experiment infrastructure.

```text
GoMyRobotBench
 ├── hardware-in-the-loop
 ├── board orchestration
 ├── FPGA instrumentation
 ├── timing capture
 ├── external instrumentation
 └── experiment control
```

GoMyRobotOS should provide the measurements and interfaces required by the experiment.

Bench decides how the hardware experiment is physically executed.

---

# 16. GoMyRobotAssure

GoMyRobotAssure should consume artifacts rather than being embedded inside GoMyRobotOS.

The flow is:

```text
GoMyRobotOS
      │
      ├── partition definition
      ├── configuration
      ├── hashes
      ├── required properties
      └── evidence references
             │
             ▼
      GoMyRobotVerify
      GoMyRobotFault
      GoMyRobotBench
             │
             ▼
       test/evidence artifacts
             │
             ▼
      GoMyRobotAssure
             │
             ▼
        Evidence Graph
```

This is a much cleaner product architecture.

GoMyRobotOS **produces evidence inputs**.

GoMyRobotAssure **builds the assurance argument**.

---

# 17. The actual GoMyRobotOS core

After removing the responsibilities that belong elsewhere, the core becomes:

```text
                     GoMyRobotOS
                          │
        ┌─────────────────┼──────────────────┐
        │                 │                  │
        ▼                 ▼                  ▼
 Partition Contract       IR           Backend API
        │                 │                  │
        └─────────────────┼──────────────────┘
                          ▼
                  Execution realization
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
        Target backend           Runtime interface
              │                       │
              ▼                       ▼
       Xen / XNG / ...          GoMyRobotRT
              │                       │
              └───────────┬───────────┘
                          ▼
                   managed partition
```

Its five core responsibilities are therefore:

1. **Partition definition**
2. **Resource/isolation semantics**
3. **Backend realization**
4. **Runtime integration**
5. **Partition-level recovery contract**

Everything else is connected to it, but not necessarily implemented by it.

---

# 18. The target backend model

The initial backend matrix should be:

```text
                    GoMyRobotOS IR
                          │
             ┌────────────┼─────────────┐
             │            │             │
             ▼            ▼             ▼
          x86-64       NG-ULTRA       HPSC
             │            │             │
           Xen         XNG/XtratuM     Xen*
             │            │             │
        Linux/RTEMS     RTEMS        RTEMS/Linux*
```

`*` research/validation status, not a production claim.

This is much better than pretending that every hypervisor exists equally everywhere.

---

# 19. Research contribution

The research contribution is now more focused.

## Research Question

> **Can one machine-readable partition contract describe and validate equivalent mixed-criticality execution semantics across heterogeneous space computing architectures and separation mechanisms?**

The important word is **equivalent**.

You do not need identical implementation.

You need to determine which properties can remain invariant.

---

# 20. Research Problem 1 — Portable partition semantics

Compare the same conceptual partition on:

```text
x86-64 + Xen
       ↓
NG-ULTRA + XNG/XtratuM
       ↓
HPSC + Xen / WorldGuard research
```

Measure:

* CPU allocation
* memory isolation
* interrupt ownership
* device ownership
* communication
* startup behavior
* recovery behavior

The question is:

> Which partition semantics are genuinely portable, and which are inherently hardware/backend-specific?

That is the core architectural research contribution.

---

# 21. Research Problem 2 — Multi-channel interference

This should remain one of the strongest research areas.

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

Experiment:

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

Measure:

* latency
* jitter
* throughput degradation
* cache effects
* memory bandwidth
* interrupt latency
* DMA interference

This is where the HPSC architecture becomes particularly interesting because WorldGuard extends partitioning across multiple hardware resource classes.

---

# 22. Research Problem 3 — Fault containment and recovery

Standard fault model:

```text
fault
  ↓
detect
  ↓
contain
  ↓
recover
  ↓
resume / safe state
```

Measure:

```text
T_detect
T_contain
T_recover
T_resume
```

Fault classes:

* application crash
* illegal memory access
* illegal MMIO
* DMA violation
* interrupt abuse
* CPU starvation
* resource exhaustion
* service-domain crash
* management-domain failure
* watchdog timeout
* corrupted image

The final result should be a measurable recovery model rather than merely a statement that "recovery exists."

---

# 23. Research Problem 4 — Faults caused by the space environment

This becomes a **GoMyRobotFault / GoMyRobotBench / GoMyRobotAssure** research stream rather than a GoMyRobotOS subsystem.

The question is:

> How well do software-level fault models predict containment and recovery behavior for space-relevant hardware fault mechanisms?

Potential fault families:

```text
SEU-like bit flips
register corruption
memory corruption
configuration corruption
transient execution faults
communication corruption
watchdog timeouts (indicate a fault, not cause it)
```

QEMU and simulation provide the early stage.

HPSC and NG-ULTRA provide the hardware stage.

---

# 24. Research Problem 5 — Assurance portability

This remains one of the most commercially interesting areas.

For example:

```text
Partition P1
     │
     ├── x86-64
     ├── NG-ULTRA
     └── HPSC
```

The question becomes:

> How much of the verification and assurance argument remains valid when the deployment platform changes?

GoMyRobotOS should therefore produce machine-readable metadata such as:

```text
partition configuration
hardware profile
backend version
image hash
resource allocation
required tests
deployment identity
```

GoMyRobotAssure then turns those into the actual evidence graph.

---

# 25. ELISA relationship

ELISA should remain a **parallel integration/upstream workstream**, not the foundation.

```text
GoMyRobotOS
      │
      └── ELISA integration
           ├── Linux configuration
           ├── timing/latency measurements
           ├── tracing
           ├── metrics
           ├── safety tooling
           ├── SBOM / supply chain
           └── reusable upstream artifacts
```

The distinction is:

> **GoMyRobotOS is a space execution/partition platform.**

> **ELISA is an ecosystem for enabling Linux in safety-critical systems.**

This lets GoMyRobotOS contribute to ELISA without becoming dependent on it.

---

# 26. Updated milestone structure

I would now replace the previous M0–M7 plan with a tighter six-stage program.

## M0 — Contract and architecture freeze

Deliver:

* GoMyRobotOS specification
* Partition Contract v1
* IR v1
* Backend API v1
* Hardware Profile v1
* Recovery model v1

Gate:

> A complete workload can be described without mentioning Xen, XNG, or any board-specific implementation.

---

## M1 — x86-64 reference platform

Goal:

```text
Partition Contract
        ↓
IR
        ↓
Xen
        ↓
RTEMS / Linux
```

Implement:

* parser
* validator
* IR
* backend
* boot/deployment
* basic partition monitoring

Tests:

* reproducible boot
* CPU allocation
* memory isolation
* communication
* basic fault containment

This becomes the **CI/reproducibility platform**.

---

## M2 — NG-ULTRA flight reference

Goal:

```text
GoMyRobotOS
      ↓
NG-ULTRA backend
      ↓
XNG/XtratuM
      ↓
RTEMS
      ↓
GoMyRobotRT
```

Demonstrate:

* real target boot
* partition configuration
* resource ownership
* RTEMS workload
* timing measurement
* basic fault containment

The existing NG-ULTRA/RTEMS/XNG ecosystem makes this a realistic flight-oriented reference.

---

## M3 — Interference laboratory

Build:

**GMR-INTERF v1**

Stress:

* CPU
* cache
* memory
* DMA
* IRQ
* I/O

Measure:

* latency
* jitter
* throughput
* interference

Run progressively on:

```text
x86-64
   ↓
NG-ULTRA
   ↓
HPSC
```

---

## M4 — HPSC research

Start with:

```text
HPSC
 ├── RTEMS baseline
 ├── WorldGuard experiments
 └── Xen feasibility
```

Then investigate:

```text
Xen
 ↓
RISC-V guest
 ↓
RTEMS guest
```

Do not make Xen-on-HPSC a prerequisite for the entire architecture.

The research result is the important part:

> Can hardware-assisted RISC-V partitioning provide predictable mixed-criticality isolation when combined with virtualization?

HPSC's current hardware/software ecosystem makes this a credible research direction, while the evolving Xen RISC-V guest stack means it should remain explicitly experimental.

---

## M5 — Recovery and assurance integration

Integrate:

```text
GoMyRobotOS
      │
      ├── GoMyRobotFault
      ├── GoMyRobotBench
      ├── GoMyRobotVerify
      └── GoMyRobotAssure
```

Generate:

```text
partition configuration
      +
image identity
      +
test results
      +
fault results
      +
timing results
      +
deployment profile
      ↓
Evidence Graph
```

---

## M6 — ServiceReady reference

Final demonstration:

```text
                 GoMyRobotOS
                     │
          ┌──────────┼───────────┐
          │          │           │
        Flight     Autonomy    Services
        RTEMS       RTEMS       Linux
          │          │           │
          └──────────┼───────────┘
                     ▼
               GoMyRobotGuard
                     │
                     ▼
             GoMyRobotVerify
                     │
                     ▼
             GoMyRobotAssure
```

Demonstrate at least two target realizations using the same conceptual partition system.

That is the **ServiceReady proof**.

---

# 27. Milestone gates

| Milestone | Gate                                                                                  |
| --------- | ------------------------------------------------------------------------------------- |
| M0        | Contract describes the system without backend-specific fields                         |
| M1        | x86-64 reference boots and isolates partitions                                        |
| M2        | NG-ULTRA executes the same conceptual flight partition                                |
| M3        | Interference measurements are reproducible                                            |
| M4        | HPSC demonstrates measurable hardware partitioning / virtualization feasibility       |
| M5        | Faults, tests and artifacts automatically feed assurance                              |
| M6        | Same conceptual mixed-criticality system is demonstrated across heterogeneous targets |

---

# 28. First research paper

The strongest first paper is no longer an XtratuM-vs-Xen comparison across many legacy boards.

I would use:

### "A Portable Partition Contract and Measurement Framework for Mixed-Criticality Space Computing"

Initial experimental scope:

```text
x86-64 + Xen
        vs
NG-ULTRA + XNG/XtratuM
```

Compare:

* partition semantics
* memory isolation
* timing
* communication
* boot reproducibility
* fault containment
* deployment complexity

Then HPSC becomes the next-generation extension.

---

# 29. Second paper

### "Measuring Multi-Channel Interference in Heterogeneous Space Computing Platforms"

Platforms:

```text
x86-64
NG-ULTRA
HPSC
```

Interference:

```text
CPU
cache
memory
DMA
interrupts
I/O
```

Output:

```text
Stressor
  ↓
latency
jitter
bandwidth
deadline impact
containment
```

The goal is a reproducible benchmark rather than a board-specific performance report.

---

# 30. Third paper

### "Evidence Portability for Heterogeneous Flight Software Partitioning"

Question:

> When the same conceptual partitioned system moves between x86-64, NG-ULTRA and HPSC, how much of the verification and assurance argument can be retained automatically?

This aligns strongly with GoMyRobot's broader interoperability philosophy.

---

# 31. Final architecture

The final architecture is therefore:

```text
                        GoMyRobotOS
                             │
             ┌───────────────┼────────────────┐
             │               │                │
             ▼               ▼                ▼
      Partition Contract     IR          Backend API
             │               │                │
             └───────────────┼────────────────┘
                             ▼
                   Target realization
                             │
             ┌───────────────┼────────────────┐
             │               │                │
             ▼               ▼                ▼
          x86-64         NG-ULTRA           HPSC
             │               │                │
            Xen          XNG/XtratuM       Xen / WorldGuard*
             │               │                │
             └───────────────┼────────────────┘
                             ▼
                      GoMyRobotRT
                             │
                        RTEMS + ROS
                             │
                         Workloads
```

Surrounding it:

```text
             ┌──────────────────────────┐
             │       GoMyRobotOS        │
             │  Partition + Execution   │
             └────────────┬─────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
GoMyRobotFault     GoMyRobotBench    GoMyRobotVerify
        │                 │                 │
        └─────────────────┼─────────────────┘
                          ▼
                   GoMyRobotAssure

GoMyRobotSecure ─────── security chain
GoMyRobotBSP ────────── target realization/build
GoMyRobotRT ─────────── flight runtime
GoMyRobotSim ────────── simulation
```

---

# 32. Final strategic statement

I would now freeze the positioning as:

> **GoMyRobotOS is a partition and execution platform for heterogeneous safety-critical space computers. It defines a hypervisor-independent contract for resource isolation, timing, communication, startup, and recovery, then realizes that contract through target-specific execution backends and integrates the resulting deployment with GoMyRobot's runtime, verification, fault-injection, and assurance systems.**

And the deeper research statement is:

> **GoMyRobotOS investigates whether partition semantics and their associated evidence can remain portable and measurable across heterogeneous space-computing architectures and separation mechanisms.**

That is a cleaner architecture than the earlier design iterations (v8 and before).

The important architectural boundaries are now explicit:

**GoMyRobotOS** → partition/execution semantics
**GoMyRobotRT** → deterministic flight runtime
**GoMyRobotBSP** → target/build realization
**GoMyRobotGuard** → independent runtime safety/recovery
**GoMyRobotFault** → fault and radiation modeling/injection
**GoMyRobotBench** → physical/HIL experiment infrastructure
**GoMyRobotVerify** → verification execution and traceability
**GoMyRobotAssure** → evidence graph and safety argument
**GoMyRobotSecure** → security chain
**GoMyRobotSim** → simulation

That is the version I would use as the **new frozen architecture baseline**.
