# GoMyRobotOS Documentation

> **GoMyRobotOS is a partition and execution platform for heterogeneous
> safety-critical space computers.** It defines a hypervisor-independent
> contract for execution, isolation, communication, startup, and recovery,
> then realizes that contract through target-specific backends.

```{attention} Project status: M0 - Architecture and Contract Freeze
GoMyRobotOS is documentation-first. The architecture, the Partition
Contract, and the backend model are frozen as a specification. **No target
system has been implemented yet.** Every maturity statement in these pages
therefore uses one of the labels: `Stable`, `Experimental`, `Research`,
`Planned`, or `Not implemented`.
```

## How to read this documentation

* These pages **are** the documentation source of truth for GoMyRobotOS -
  the architecture, the contract, and the process are defined here and in
  the accompanying schema and examples.
* **ROS 2 Rolling** is the authoritative external reference for all ROS 2
  concepts: see the official
  [ROS 2 Rolling documentation](https://docs.ros.org/en/rolling/).
  This project never duplicates ROS 2 documentation - it links to it and
  documents only GoMyRobot-specific integration and guarantees
  ([compatibility/ros2](compatibility/ros2)).
* Architecture changes are traceable to numbered Architecture Decision
  Records (ADR-0001 … ADR-0013) in
  [development/architecture-decisions](development/architecture-decisions).

## Contents

```{toctree}
:maxdepth: 1
:caption: Getting started

getting-started/overview
getting-started/installation
getting-started/development-environment
```

```{toctree}
:maxdepth: 1
:caption: Concepts

concepts/overview
concepts/architecture-principles
concepts/partitioning
concepts/isolation
concepts/execution-model
concepts/assurance
```

```{toctree}
:maxdepth: 1
:caption: Architecture

architecture/overview
architecture/layered-model
architecture/partition-contract
architecture/ir
architecture/backend-model
architecture/runtime-model
architecture/recovery-model
architecture/frozen-baseline
```

```{toctree}
:maxdepth: 1
:caption: Ecosystem components

components/gomyrobotrt
components/ros2-rolling
components/gomyrobotbsp
components/gomyrobotguard
components/gomyrobotfault
components/gomyrobotbench
components/gomyrobotverify
components/gomyrobotassure
```

```{toctree}
:maxdepth: 1
:caption: Partition Contract

contract/overview
contract/specification
contract/schema
contract/examples/flight-control
```

```{toctree}
:maxdepth: 1
:caption: Platforms

platforms/x86-64
platforms/ng-ultra
platforms/hpsc
```

```{toctree}
:maxdepth: 1
:caption: Backends

backends/overview
backends/xen
backends/xtratum
backends/xng
```

```{toctree}
:maxdepth: 1
:caption: Validation

validation/methodology
validation/temporal-isolation
validation/spatial-isolation
validation/interference
validation/fault-injection
validation/recovery
```

```{toctree}
:maxdepth: 1
:caption: Assurance

assurance/evidence-model
assurance/reproducibility
assurance/evidence-graph
```

```{toctree}
:maxdepth: 1
:caption: Research

research/agenda
research/research-problems
research/publications
```

```{toctree}
:maxdepth: 1
:caption: Milestones

milestones/overview
milestones/m0
milestones/m1
milestones/m2
milestones/m3
milestones/m4
milestones/m5
milestones/m6
```

```{toctree}
:maxdepth: 1
:caption: Compatibility

compatibility/ros2
```

```{toctree}
:maxdepth: 1
:caption: Development

development/contributing
development/testing
development/architecture-decisions
development/architecture-v2
```

