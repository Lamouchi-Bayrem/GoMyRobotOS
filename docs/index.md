# GoMyRobotOS Documentation

> **GoMyRobotOS is a partition and execution platform for heterogeneous
> safety-critical space computers.** It defines a hypervisor-independent
> contract for execution, isolation, communication, startup, and recovery,
> then realizes that contract through target-specific backends.

```{attention} Project status: M0 Architecture and Contract Freeze
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
  This project never duplicates ROS 2 documentation, it links to it and
  documents only GoMyRobot-specific integration and guarantees
  ([compatibility/ros2](compatibility/ros2)).
* Architecture changes are traceable to numbered Architecture Decision
  Records (ADR-0001 … ADR-0013) in
  [development/architecture-decisions](development/architecture-decisions).

## Contents

```{toctree}
getting-started/index
concepts/index
architecture/index
components/index
contract/index
platforms/index
backends/index
validation/index
assurance/index
research/index
milestones/index
compatibility/index
development/index
```

