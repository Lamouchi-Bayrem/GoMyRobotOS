# GoMyRobotOS Documentation Implementation Prompt

You are working on the **GoMyRobotOS** open-source repository.

Build the project's documentation as a professional, versioned, open-source systems project using:

* Sphinx
* MyST Markdown
* Read the Docs
* GitHub Actions
* Git-based version control

Repository:

```text
gomyrobot/gomyrobotos
```

Documentation:

```text
gomyrobotos.readthedocs.io
```

Do not depend on a proprietary documentation platform.

---

# 1. Primary architectural source of truth

Use the current **GoMyRobotOS Final Architecture** as the primary source of truth.

Do not invent architecture.

Core definition:

> **GoMyRobotOS is a partition and execution platform for heterogeneous safety-critical space computers.**

It defines a hypervisor-independent contract for:

1. execution
2. isolation
3. communication
4. startup
5. recovery

It realizes that contract through target-specific execution backends.

The hypervisor is a backend.

GoMyRobotOS is not:

* an RTOS
* a hypervisor
* a Linux distribution
* a ROS 2 replacement
* a BSP
* a simulator
* a fault-injection platform
* a safety-case platform

---

# 2. Explicit ROS 2 Rolling reference

The official ROS 2 Rolling documentation is the authoritative external reference for all ROS 2 concepts and APIs:

**https://docs.ros.org/en/rolling/**

Use **ROS 2 Rolling** explicitly throughout the documentation.

Do not silently mix documentation from:

* Humble
* Iron
* Jazzy
* Kilted
* older ROS 2 distributions

unless a historical comparison is explicitly required.

When documenting ROS 2 integration, always use terminology and API names consistent with the **ROS 2 Rolling documentation**.

Examples include:

* `rcl`
* `rclcpp`
* `rclpy`
* executors
* nodes
* publishers
* subscriptions
* services
* actions
* parameters
* QoS
* callback groups
* middleware / RMW
* DDS
* ROS 2 graph
* lifecycle concepts where applicable

Do not invent GoMyRobot-specific alternatives to standard ROS 2 concepts.

---

# 3. ROS 2 documentation relationship

GoMyRobotOS must **not duplicate the ROS 2 documentation**.

Instead:

```text
Official ROS 2 Rolling Documentation
        ↓
ROS 2 concepts / APIs / semantics
        ↓
GoMyRobotRT integration
        ↓
GoMyRobotOS execution environment
```

Use external references to ROS 2 Rolling for generic ROS 2 behavior.

GoMyRobot documentation should explain only:

* how GoMyRobotRT integrates ROS 2
* what execution guarantees GoMyRobotRT provides
* what GoMyRobotOS does to the ROS 2 workload
* what limitations exist on RTEMS/embedded targets
* what is deterministic vs non-deterministic
* which ROS 2 APIs are supported
* how ROS 2 workloads map onto GoMyRobotOS partitions

Do not reproduce large sections of the ROS 2 documentation.

---

# 4. Important architectural distinction

The documentation must consistently preserve this model:

```text
                    GoMyRobotOS
                         │
               Partition Contract
                         │
                         ▼
                       IR
                         │
                 Target Backend
                         │
                ┌────────┴────────┐
                ▼                 ▼
             Hypervisor       Bare metal/
             /separation      future backend
                │
                ▼
              Runtime
                │
                ▼
           GoMyRobotRT
                │
        ┌───────┴────────┐
        ▼                ▼
      RTEMS          ROS 2 APIs
```

ROS 2 is the robotics middleware/workload environment.

It is **not** the architectural center of GoMyRobotOS.

---

# 5. GoMyRobotRT documentation

Create a dedicated GoMyRobotRT section.

It must explicitly reference the ROS 2 Rolling documentation.

Structure:

```text
GoMyRobotRT
├── Overview
├── ROS 2 Rolling integration
├── RTEMS integration
├── rcl/rclcpp
├── executors
├── callback execution
├── QoS
├── middleware/RMW
├── deterministic execution
├── hardware abstraction
├── health monitoring
└── flight workload integration
```

For every ROS 2 concept:

1. explain the official ROS 2 meaning briefly
2. link to the relevant ROS 2 Rolling documentation
3. explain GoMyRobotRT's implementation/integration
4. explicitly identify differences or limitations on RTEMS

Example:

```markdown
## Executors

GoMyRobotRT follows the ROS 2 executor model described in the
ROS 2 Rolling documentation.

See:
[ROS 2 Rolling - Executors](https://docs.ros.org/en/rolling/...)

GoMyRobotRT may impose additional deterministic execution constraints
for flight workloads.

Those constraints are GoMyRobot-specific and must not be presented
as standard ROS 2 behavior.
```

Do not claim a ROS 2 feature is supported by GoMyRobotRT unless the repository actually implements it.

---

# 6. Explicit ROS 2 Rolling terminology policy

Use:

```text
ROS 2
ROS 2 Rolling
rcl
rclcpp
rclpy
RMW
DDS
QoS
executor
node
publisher
subscription
service
action
callback group
parameter
lifecycle
```

Do not introduce:

```text
GoMyRobotNode
GoMyRobotPublisher
GoMyRobotExecutor
```

as replacements for standard ROS 2 concepts.

Only introduce a GoMyRobot-specific abstraction when there is a real architectural reason.

---

# 7. ROS 2 references inside the documentation

Use direct links to the official Rolling documentation wherever relevant.

Preferred pattern:

```markdown
See the official
[ROS 2 Rolling documentation](https://docs.ros.org/en/rolling/)
for the underlying ROS 2 concept.
```

For specific concepts, link directly to the relevant Rolling page.

Do not link readers to:

* random tutorials
* outdated ROS distributions
* unofficial mirrors
* third-party summaries

unless a specific research reference requires it.

---

# 8. ROS 2 version policy

Create a page:

```text
docs/compatibility/ros2.md
```

It must state:

```text
ROS 2 Documentation Reference: Rolling

Primary reference:
https://docs.ros.org/en/rolling/

GoMyRobotRT ROS 2 compatibility:
[fill only with verified repository status]
```

Do not claim that GoMyRobotRT is fully compatible with all of ROS 2 Rolling merely because the documentation is based on Rolling.

Separate:

```text
Documentation reference
```

from:

```text
Implemented API support
```

For example:

```text
ROS 2 Rolling documentation reference
    ≠
full ROS 2 Rolling runtime compatibility
```

---

# 9. Repository structure

Use:

```text
gomyrobotos/

├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CHANGELOG.md
│
├── docs/
│   ├── conf.py
│   ├── index.md
│   ├── requirements.txt
│   │
│   ├── getting-started/
│   │   ├── overview.md
│   │   ├── installation.md
│   │   └── development-environment.md
│   │
│   ├── concepts/
│   │   ├── overview.md
│   │   ├── architecture-principles.md
│   │   ├── partitioning.md
│   │   ├── isolation.md
│   │   ├── execution-model.md
│   │   └── assurance.md
│   │
│   ├── architecture/
│   │   ├── overview.md
│   │   ├── layered-model.md
│   │   ├── partition-contract.md
│   │   ├── ir.md
│   │   ├── backend-model.md
│   │   ├── runtime-model.md
│   │   └── recovery-model.md
│   │
│   ├── components/
│   │   ├── gomyrobotrt.md
│   │   ├── ros2-rolling.md
│   │   ├── gomyrobotbsp.md
│   │   ├── gomyrobotguard.md
│   │   ├── gomyrobotfault.md
│   │   ├── gomyrobotbench.md
│   │   ├── gomyrobotverify.md
│   │   └── gomyrobotassure.md
│   │
│   ├── contract/
│   │   ├── overview.md
│   │   ├── specification.md
│   │   ├── schema.md
│   │   └── examples/
│   │
│   ├── platforms/
│   │   ├── x86-64/
│   │   ├── ng-ultra/
│   │   └── hpsc/
│   │
│   ├── backends/
│   │   ├── overview.md
│   │   ├── xen.md
│   │   ├── xtratum.md
│   │   └── xng.md
│   │
│   ├── validation/
│   │   ├── methodology.md
│   │   ├── temporal-isolation.md
│   │   ├── spatial-isolation.md
│   │   ├── interference.md
│   │   ├── fault-injection.md
│   │   └── recovery.md
│   │
│   ├── assurance/
│   │   ├── evidence-model.md
│   │   ├── reproducibility.md
│   │   └── evidence-graph.md
│   │
│   ├── research/
│   │   ├── agenda.md
│   │   ├── research-problems.md
│   │   └── publications.md
│   │
│   ├── milestones/
│   │   ├── overview.md
│   │   ├── m0.md
│   │   ├── m1.md
│   │   ├── m2.md
│   │   ├── m3.md
│   │   ├── m4.md
│   │   ├── m5.md
│   │   └── m6.md
│   │
│   ├── compatibility/
│   │   └── ros2.md
│   │
│   └── development/
│       ├── contributing.md
│       ├── testing.md
│       └── architecture-decisions.md
│
├── schemas/
│   └── partition-contract.schema.json
│
├── examples/
│   ├── x86-64/
│   ├── ng-ultra/
│   └── hpsc/
│
└── .github/
    └── workflows/
        └── docs.yml
```

Do not create pages merely to fill the tree.

Pages must contain meaningful content.

---

# 10. Sphinx + ROS 2 Rolling references

Configure Sphinx/MyST normally.

Use Sphinx external linking or intersphinx where appropriate.

The goal is:

```text
GoMyRobotOS documentation
        │
        ├── local architecture
        ├── local implementation
        └── official external references
                  │
                  ▼
           ROS 2 Rolling docs
```

Do not attempt to mirror the entire ROS 2 documentation locally.

---

# 11. Architecture Decisions

Create:

```text
ADR-0001 - GoMyRobotOS is a partition and execution platform

ADR-0002 - Partition Contract is the central abstraction

ADR-0003 - Hypervisors are target-specific backends

ADR-0004 - x86-64 is the initial development/reference platform

ADR-0005 - NG-ULTRA is the primary flight-oriented reference

ADR-0006 - HPSC is the initial RISC-V research target

ADR-0007 - GoMyRobotRT is separate from GoMyRobotOS

ADR-0008 - ROS 2 Rolling is the primary ROS 2 documentation reference

ADR-0009 - GoMyRobotBSP owns target build/image realization

ADR-0010 - Fault and radiation modeling belongs outside GoMyRobotOS

ADR-0011 - GoMyRobotGuard must be independent of the failure domain it recovers

ADR-0012 - Verification and assurance are external platform services

ADR-0013 - Documentation is versioned with the software
```

---

# 12. Partition Contract

Document the Partition Contract as the central machine-readable interface.

Minimum conceptual fields:

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

The contract must never contain backend-specific syntax such as:

```text
xen_dom0
xtratum_partition_id
xng_specific_option
```

unless the property genuinely cannot be expressed at the portable semantic layer.

Backend-specific information belongs in the backend profile.

---

# 13. Target status

Use explicit maturity labels everywhere.

Allowed status values:

```text
Stable
Experimental
Research
Planned
Not implemented
```

Initial targets:

### x86-64

Status:

```text
Development / Reference
```

Purpose:

* CI
* QEMU experimentation
* backend development
* reproducibility
* fault injection
* performance experiments

### NG-ULTRA

Status:

```text
Flight Reference / Development
```

Do not claim support that has not been implemented.

### PIC64-HPSC

Status:

```text
Research
```

Do not claim production-ready RTEMS-on-Xen support.

---

# 14. HPSC documentation

Document the HPSC research path as:

```text
HPSC
 ├── RTEMS baseline
 ├── WorldGuard investigation
 ├── Xen feasibility
 ├── RISC-V guest feasibility
 ├── timer
 ├── interrupts
 ├── memory
 └── RTEMS guest
```

Clearly label uncertain or unimplemented portions.

Do not turn research tasks into product capability claims.

---

# 15. Fault and radiation architecture

Do not place radiation testing inside GoMyRobotOS documentation as an OS responsibility.

Document the relationship as:

```text
GoMyRobotFault
       │
       ├── software faults
       ├── hardware fault models
       ├── communication faults
       └── radiation / SEU models
               │
               ▼
          QEMU / HIL / target
               │
               ▼
          GoMyRobotOS
               │
          detect/contain/recover
               │
               ▼
       GoMyRobotVerify
               │
               ▼
       GoMyRobotAssure
```

QEMU may be used to reproduce modeled fault effects.

Do not describe QEMU as physically reproducing radiation.

---

# 16. Yocto

Document Yocto under GoMyRobotBSP.

Correct relationship:

```text
GoMyRobotBSP
       │
       ├── RTEMS artifacts
       ├── hypervisor artifacts
       └── Yocto/OpenEmbedded
                  │
                  ▼
             Linux image
```

Never describe GoMyRobotOS as:

```text
Yocto-based OS
```

Use:

```text
Yocto/OpenEmbedded may be used by GoMyRobotBSP
to construct Linux deployment images.
```

---

# 17. Validation

Document:

* reproducible boot
* functional runtime validation
* temporal isolation
* spatial isolation
* CPU interference
* cache interference
* memory interference
* interconnect interference
* DMA interference
* interrupt interference
* I/O interference
* resource exhaustion
* fault injection
* recovery timing

Do not claim:

* formal WCET
* certification
* safety certification
* complete freedom from interference

unless actual evidence exists.

---

# 18. Research agenda

Document four primary research questions:

### R1 - Portable partition semantics

Can one contract describe equivalent partition behavior across heterogeneous backends?

### R2 - Multi-channel interference

How do CPU, cache, memory, DMA, interrupt, and I/O contention affect critical workloads?

### R3 - Fault containment and recovery

Can failures be detected, contained, and recovered independently of the failed partition?

### R4 - Assurance portability

How much of the verification/evidence argument can move with the partition when hardware/backend changes?

Do not present these as solved.

They are research problems.

---

# 19. Milestones

Use:

```text
M0 - Architecture and Contract Freeze

M1 - x86-64 Reference Partition

M2 - NG-ULTRA Flight Reference

M3 - Interference Laboratory

M4 - HPSC Research

M5 - Recovery and Assurance Integration

M6 - ServiceReady Reference Platform
```

Each milestone contains:

* objective
* scope
* deliverables
* tests
* acceptance gate
* current status
* known limitations

Do not create M7 unless a future architecture decision establishes a separate milestone.

---

# 20. README

README must contain:

* GoMyRobotOS name
* one-sentence description
* architecture diagram
* why it exists
* Partition Contract
* relationship with GoMyRobotRT
* relationship with ROS 2
* initial targets
* current status
* roadmap
* research direction
* documentation
* contribution information
* license

Suggested description:

> GoMyRobotOS is a partition and execution platform for heterogeneous safety-critical space computers. It defines a hypervisor-independent contract for execution, isolation, communication, startup, and recovery, then realizes that contract through target-specific backends.

---

# 21. Anti-hallucination rules for Qwen + Cline

This is mandatory.

Never invent:

* APIs
* command-line tools
* hardware support
* hypervisor support
* RTEMS support
* ROS 2 support
* certification
* safety properties
* benchmark results
* timing results

When uncertain, write:

```text
Status: Research
Status: Experimental
Status: Not yet implemented
```

instead of creating an implementation claim.

Never convert:

```text
architecture proposal
```

into:

```text
implemented feature
```

Never convert:

```text
research target
```

into:

```text
supported platform
```

---

# 22. ROS 2-specific anti-hallucination rule

When discussing ROS 2:

**Use the official ROS 2 Rolling documentation as the external authority.**

When GoMyRobotRT behavior differs from standard ROS 2 behavior:

1. state the standard ROS 2 behavior
2. link to ROS 2 Rolling
3. state the GoMyRobotRT behavior separately
4. identify whether the difference is implemented, experimental, or planned

Never present a GoMyRobotRT extension as an official ROS 2 concept.

Never alter ROS 2 terminology merely to make the GoMyRobot architecture look cleaner.

---

# 23. Final documentation principle

The documentation should make this distinction obvious:

```text
ROS 2 Rolling
     │
     │ official robotics middleware/API model
     ▼
GoMyRobotRT
     │
     │ deterministic flight-runtime integration
     ▼
GoMyRobotOS
     │
     │ partition / execution-domain management
     ▼
Backend
     │
     ├── Xen
     ├── XNG/XtratuM
     └── future mechanisms
     ▼
Hardware
```

The documentation should therefore **reuse standard ROS 2 terminology, explicitly reference ROS 2 Rolling, and document only the GoMyRobot-specific integration and execution guarantees**.

Do not fork or reproduce the ROS 2 documentation.

Do not create a second ROS 2 conceptual model.

Do not make ROS 2 the definition of GoMyRobotOS.

The boundary must remain:

> **ROS 2 defines the robotics software model; GoMyRobotRT makes that model usable in the deterministic flight runtime; GoMyRobotOS controls the execution environment in which the workload runs.**
