# Architecture Decisions

GoMyRobotOS architecture changes are made through Architecture Decision
Records. Every ADR has: **context**, **decision**, **consequences**,
**status**. The M0 baseline is ADR-0001 through ADR-0018.

Rules: the next free number is used for new decisions; an accepted ADR is
never silently edited, it is *superseded* by a new ADR that points back;
existing numbers are never re-used.

## Index

| ADR | Title                                             | Status   |
| --- | ------------------------------------------------- | -------- |
| 0001 | GoMyRobotOS is a partition and execution platform | Accepted |
| 0002 | Partition Contract is the central abstraction     | Accepted |
| 0003 | Hypervisors are target-specific backends          | Accepted |
| 0004 | x86-64 is the initial development/reference platform | Accepted |
| 0005 | NG-ULTRA is the primary flight-oriented reference  | Accepted |
| 0006 | HPSC is the initial RISC-V research target         | Accepted |
| 0007 | [GoMyRobotRT](https://gomyrobot.com/products/rt/) is separate from GoMyRobotOS           | Accepted |
| 0008 | ROS 2 Rolling is the primary ROS 2 documentation reference | Accepted |
| 0009 | [GoMyRobotBSP](https://gomyrobot.com/products/bsp/) owns target build/image realization   | Accepted |
| 0010 | Fault and radiation modeling belongs outside GoMyRobotOS | Accepted |
| 0011 | [GoMyRobotGuard](https://gomyrobot.com/products/guard/) must be independent of the failure domain it recovers | Accepted |
| 0012 | Verification and assurance are external platform services | Accepted |
| 0013 | Documentation is versioned with the software       | Accepted |
| 0014 | IPC is described by channel class, not transport mechanism | Accepted |
| 0015 | Backends publish a capability manifest; no silent semantic downgrade | Accepted |
| 0016 | Guard independence is staged (0 / 1 / 2)           | Accepted |
| 0017 | WCET claims carry an evidence class (proven / measured / unbounded) | Accepted |
| 0018 | The documentation site is the architecture source of truth | Accepted |

---

### ADR-0001 GoMyRobotOS is a partition and execution platform

* **Context.** The GoMyRobot ecosystem spans flight runtimes, hypervisors,
  BSPs, verification, and assurance; a failure mode to avoid is one
  "everything safety-related" product.
* **Decision.** GoMyRobotOS is a *partition and execution platform*: a
  partition model, a machine-readable execution contract, an IR, a
  target-backend interface, a deployment/orchestration layer, a runtime
  integration layer, a partition health/recovery interface, and a source
  of configuration and deployment metadata.
* **Consequences.** Every other capability (RTOS, hypervisors, builds,
  fault injection, verification, assurance, simulation) is a *sibling*
  product; GoMyRobotOS connects to them via artifacts, not by embedding
  them.
* **Status.** Accepted.

### ADR-0002 Partition Contract is the central abstraction

* **Context.** Two abstraction candidates: "generate a hypervisor
  configuration" vs. "define what a partition is allowed and required to
  do".
* **Decision.** The central abstraction is the latter, the Partition
  Contract. It expresses intent and constraints, never backend syntax;
  backend-specific data lives in the backend profile.
* **Consequences.** The contract is readable across targets; assurance
  traceability (requirements → fields → tests) is contractual; any field
  that smells mechanism-specific is a design bug.
* **Status.** Accepted.

### ADR-0003 Hypervisors are target-specific backends

* **Context.** Xen, XtratuM/XNG, and (research) hardware WorldGuard all
  "do isolation"; making any one of them the product abstraction would
  end portability.
* **Decision.** A backend is the only layer that may know mechanism
  names; a hypervisor is one kind of backend. Contract and IR are written
  so that no Xen/XtratuM concept appears in them.
* **Consequences.** New mechanisms (bare metal, native hardware
  partitioning) join without contract changes; backend validation is its
  own documented work per target.
* **Status.** Accepted.

### ADR-0004 x86-64 is the initial development/reference platform

* **Context.** The platform must be iterable in CI, cheap to run, and
  representative enough to develop backends on.
* **Decision.** x86-64 (QEMU-capable) is the development/reference
  platform; it is *not* a flight processor and never carries flight
  timing claims.
* **Consequences.** M1 is an x86-64 milestone; cross-target results must
  be repeated on flight hardware to count as flight evidence.
* **Status.** Accepted.

### ADR-0005 NG-ULTRA is the primary flight-oriented reference

* **Context.** A flight reference with an existing RTEMS + XtratuM/XNG
  ecosystem (ARMv8-R BSP, ecosystem support) keeps the flight path
  realistic.
* **Decision.** NG-ULTRA is the flight-oriented reference; the M2 gate is
  that it executes the *same conceptual flight partition* as M1.
* **Consequences.** The NG-ULTRA backend targets XNG/XtratuM + RTEMS +
  GoMyRobotRT; recorded ecosystem facts stay labeled as ecosystem facts.
* **Status.** Accepted.

### ADR-0006 HPSC is the initial RISC-V research target

* **Context.** Next-generation RISC-V with hardware partitioning
  (WorldGuard), virtualization, and an independent system controller is
  the natural third data point for the portability research, but the
  Xen RISC-V guest stack is still an active upstream development area.
* **Decision.** PIC64-HPSC is a `Research` target (M4), with staged work
  (RTEMS baseline; WorldGuard; Xen feasibility). No production claim on
  it, ever, until a gate passes.
* **Consequences.** RP1 becomes a three-point comparison when M4 lands;
  HPSC failure is a research finding, not an architecture failure.
* **Status.** Accepted.

### ADR-0007 GoMyRobotRT is separate from GoMyRobotOS

* **Context.** Robotics middleware execution (RTEMS, executors, ROS 2
  concepts, hardware abstraction) has a different change rhythm from an
  execution-environment platform.
* **Decision.** GoMyRobotRT remains its own product: *GoMyRobotRT
  executes the workload; GoMyRobotOS controls the execution environment
  in which the workload runs.* GoMyRobotOS consumes/hosts GoMyRobotRT; it
  does not include it.
* **Consequences.** All ROS 2 / RTEMS execution semantics are documented
  on the GoMyRobotRT side; GoMyRobotOS keeps workload-agnostic contract
  fields.
* **Status.** Accepted.
### ADR-0008 ROS 2 Rolling is the primary ROS 2 documentation reference

* **Context.** Multiple ROS 2 distributions exist (Humble, Iron, Jazzy,
  Kilted, Rolling); mixing editions silently produces documentation drift.
* **Decision.** [ROS 2
  Rolling](https://docs.ros.org/en/rolling/) is the sole authority for
  ROS 2 concepts/APIs in all GoMyRobotOS documentation; other editions
  appear only with explicit historical-comparison labels. No replacement
  names are invented for standard terms.
* **Consequences.** All "standard behavior" statements elsewhere in the
  documentation carry Rolling links; concept support tables
  ([compatibility/ros2]
  (../compatibility/ros2)) are checked against Rolling terminology.
* **Status.** Accepted.

### ADR-0009 GoMyRobotBSP owns target build and image realization

* **Context.** Boot artifacts, hypervisor configuration, RTEMS
  configuration, device trees, Linux images, memory maps, deployment
  manifests, hashes, someone must own producing them from profiles.
* **Decision.** GoMyRobotBSP consumes (contract + hardware profile +
  backend profile + boot profile + runtime profile) and produces the
  build artifacts. GoMyRobotOS declares *what*; BSP realizes *which
  artifacts*.
* **Consequences.** Backend-specific data lives in the backend profile
  (not the contract); BSP outputs are the source of deployment identity
  and hashes used by assurance; Yocto/OpenEmbedded is a *BSP tool* for
  Linux-domain images, never a description of GoMyRobotOS itself.
* **Status.** Accepted.

### ADR-0010 Fault and radiation modeling belongs outside GoMyRobotOS

* **Context.** Fault *generation* (software faults, hardware fault
  models, communication faults, radiation/SEU models) is a different
  discipline from fault *response policy*.
* **Decision.** GoMyRobotOS declares what a partition does when a fault
  occurs (contract `recovery.*`); [GoMyRobotFault](https://gomyrobot.com/products/fault/) generates faults and
  models radiation effects; QEMU models *effects* and never reproduces
  radiation physics.
* **Consequences.** "Radiation" and "robustness" are results of that
  external stream only if measured; the OS side stays a semantics +
  logging obligation.
* **Status.** Accepted.

### ADR-0011 GoMyRobotGuard must be independent of the failure domain it recovers

* **Context.** A recovery mechanism that lives inside (or depends
  exclusively on) the domain it recovers fails when that domain fails.
* **Decision.** The recovering component (GoMyRobotGuard) must not depend
  exclusively on the component it recovers; on HPSC the independent
  system controller is the natural substrate (research). GoMyRobotOS
  specifies recovery semantics; Guard implements independent recovery.
* **Consequences.** Contracts carry `escalation_policy`; recovery
  validation explicitly includes *service-domain crash*,
  *management-domain failure*, and *corrupted image* classes.
* **Status.** Accepted.

### ADR-0012 Verification and assurance are external platform services

* **Context.** Coupling verification execution or assurance-argument
  construction into the platform couples change rhythms and blurs
  evidence/interpretation boundaries.
* **Decision.** GoMyRobotOS emits evidence inputs (config manifest,
  required properties, test requirements, deployment metadata, recovery
  log); [GoMyRobotVerify](https://gomyrobot.com/products/verify/) and [GoMyRobotAssure](https://gomyrobot.com/products/assure/) are external consumers.
* **Consequences.** The documentation claims no certification, WCET, or
  immunity from interference; the assurance data plane is documented as a
  data plane; future assurance statements must trace to external
  processes.
* **Status.** Accepted.

### ADR-0013 Documentation is versioned with the software

* **Context.** Architecture and contract are the product at M0-M1;
  undocumented or separately-versioned documentation would drift from
  implementation.
* **Decision.** The documentation lives in-repo (`docs/`), is built by
  CI, is versioned with the code, and carries the project's status-label
  discipline; the GitHub Pages site is the host.
* **Consequences.** Doc build failures block merges (CI `docs` job);
  maturity labels are mandatory on every capability statement; the ADR
  process documented here is that authority.
* **Status.** Accepted.

---

### ADR-0014 IPC is described by channel class, not transport mechanism

* **Context.** The communication references in the v2 architecture draft
  enumerated transport mechanisms (grant tables, event channels, virtio),
  which would couple the contract to a specific backend. The contract
  must express only the channel *semantics* (ADR-0002, ADR-0003).
* **Decision.** Communication endpoints of a partition are typed by
  channel class, `sampling` (periodic state, last value wins) or
  `queuing` (bounded queue with explicit overflow policy), and carry
  `max_message_size`, `max_rate_hz`, `latency_budget_us`,
  `buffer_ownership`, and, for queuing channels, `overflow_policy`.
  Mapping those semantics to a concrete mechanism is backend
  implementation detail and must never appear in the contract or the IR.
* **Consequences.** `communication.endpoints` fields grow (all optional,
  schema-compatible). Backend documentation may explain mechanisms;
  contract fields that introduce mechanism names must be rejected in
  review.
* **Status.** Accepted.

### ADR-0015 Backends publish a capability manifest; no silent semantic downgrade

* **Context.** A single target cannot realize every contract field at the
  same fidelity (cache-partitioning granularity, DMA remap, interrupt
  virtualization). A compile that silently drops a field is a
  correctness failure: the evidence graph would then claim semantics the
  target does not provide.
* **Decision.** Each backend publishes a **capability manifest** (which
  contract fields and value ranges it realizes, at what fidelity).
  Before compile, the pipeline checks the contract's
  `capabilities_required` list against it: no match fails the build;
  partial match compiles only with a reviewable waiver recorded in the
  evidence graph. Rule: **no silent semantic downgrade**.
* **Consequences.** The manifest concept freezes with M0; its *schema* is
  not yet published (planned with the M1 parser/validator). The contract
  gains `partition.capabilities_required` (optional).
* **Status.** Accepted.

### ADR-0016 Guard independence is staged (0 / 1 / 2)

* **Context.** "Guard is independent" is a spectrum, not a boolean: a
  co-resident software guard cannot claim against a common-mode
  hypervisor failure, while a companion system controller can
  (ADR-0011).
* **Decision.** Guard independence operates at three stages:
  **0** software guard (no common-mode protections claimed),
  **1** companion MCU / system controller (common-mode independence),
  **2** validated with per-fault-class detect / contain / recover
  timing in the evidence graph. The contract declares
  `recovery.guard_independence_stage`; every recovery claim records the
  stage it was demonstrated under.
* **Consequences.** M1-M3 operate at stage 0; M5 requires stage
  recording on claims; M6 requires stage-2 quantification for the
  reference system. A specific platform's system controller is one
  possible stage-1 realization, not a core assumption.
* **Status.** Accepted.

### ADR-0017 WCET claims carry an evidence class

* **Context.** "Measured under budget" and "WCET proven" are different
  claims; presenting one as the other is a classic over-certification
  error in documentation.
* **Decision.** Every timing claim carries an explicit evidence class:
  `proven` (formal / static WCET analysis), `measured` (validated under
  a defined stress pattern), or `unbounded`. The contract carries
  `execution.timing_budget.wcet_bound_us` and
  `wcet_evidence_class`; documentation and artifacts must never present
  `measured` as `proven`.
* **Consequences.** The `timing_bound` test and every timing assertion in
  M3+ comparison pages must state the class; a timing claim without a
  class is a review defect.
* **Status.** Accepted.

### ADR-0018 The documentation site is the architecture source of truth

* **Context.** The M0 freeze initially named the root-level
  `GoMyRobotOS.md` as the source of truth and the rendered site as a
  secondary rendering, inviting drift between the two. The site is the
  visible, versioned, CI-built artifact.
* **Decision.** This documentation site's sources (`docs/`) are the
  primary source of truth for architecture, contract, and process.
  `GoMyRobotOS.md` and `docs.md` are removed; the normative scope notes
  of the removed document (naming rule, v1 exclusions, platform
  position) are captured in the
  [frozen baseline page](../architecture/frozen-baseline).
* **Consequences.** Architecture changes are made against `docs/` pages
  through this ADR process; nothing may cite the deleted root documents.
* **Status.** Accepted.

## Supersession log

None yet. When an ADR is superseded, it stays as *Accepted, superseded by
ADR-XXXX* with a dated note here.