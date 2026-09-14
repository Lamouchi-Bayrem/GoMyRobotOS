# Concepts overview

This section explains *what* GoMyRobotOS is at the conceptual level - the
definitions, the model, and the principles - before the [Architecture
section](../architecture/overview) explains *how* it is mechanically
designed.

## The core definition

> **GoMyRobotOS is a partition and execution platform for heterogeneous
> safety-critical space computers.**

It defines a hypervisor-independent contract for:

1. execution
2. isolation
3. communication
4. startup
5. recovery

It realizes that contract through target-specific execution backends.
The hypervisor is a backend.

## Key terms

| Term                | Meaning in GoMyRobotOS                                                    |
| ------------------- | -------------------------------------------------------------------------- |
| Partition           | A controlled execution domain with explicitly allocated resources          |
| Partition Contract  | The machine-readable, hypervisor-independent description of a partition    |
| IR                  | GoMyRobotOS Intermediate Representation - the stable internal model between contract and backends |
| Backend             | A target-specific mechanism (e.g., Xen, XNG/XtratuM) that realizes the IR  |
| Workload            | The software running inside a partition - e.g., a [GoMyRobotRT](https://gomyrobot.com/products/rt/) ROS 2 workflow |
| GoMyRobotRT         | The sibling product that executes the robotics workload inside a partition |

## Architecture in one diagram

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
              ┌──────────┴──────────┐
              ▼                     ▼
           Hypervisor          Bare metal /
           / separation        future backend
              │
              ▼
           Runtime
              │
              ▼
         GoMyRobotRT
              │
        ┌─────┴─────┐
        ▼           ▼
      RTEMS      ROS 2 APIs
```

ROS 2 is the robotics middleware / workload environment. It is **not** the
architectural center of GoMyRobotOS.

## What GoMyRobotOS is and is not

GoMyRobotOS **is**:

* a partition model
* a machine-readable execution contract
* an intermediate representation
* a target-backend interface
* a partition deployment / orchestration layer
* a runtime integration layer
* a partition health / recovery interface
* a source of configuration and deployment metadata

GoMyRobotOS is **not** RTEMS, Linux, ROS 2, Xen, XtratuM/XNG, Yocto, a BSP, a
simulator, a radiation-testing framework, a complete fault-injection platform,
or a safety-case platform. Those technologies remain components of the larger
GoMyRobot ecosystem, and the boundaries between them are architectural
decisions - see [ADR list](../development/architecture-decisions).

## Reading order

1. [Architecture principles](architecture-principles)
2. [Partitioning](partitioning)
3. [Isolation](isolation)
4. [Execution model](execution-model)
5. [Assurance positioning](assurance)
