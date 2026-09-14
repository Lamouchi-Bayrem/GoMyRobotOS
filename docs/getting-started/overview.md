# Overview

GoMyRobotOS is a partition and execution platform for heterogeneous
safety-critical space computers. It defines a hypervisor-independent contract
for execution, isolation, communication, startup, and recovery, and then
realizes that contract through target-specific execution backends.

One addition from the M0 baseline: GoMyRobotOS is **not** an RTOS, a
hypervisor, a Linux distribution, a ROS 2 replacement, a BSP, a simulator, a
fault-injection platform, or a safety-case platform. Those capabilities belong
to sibling products in the GoMyRobot ecosystem.

## The five core responsibilities

After removing the responsibilities that belong to sibling products, the
GoMyRobotOS core is:

1. **Partition definition**
2. **Resource / isolation semantics**
3. **Backend realization**
4. **Runtime integration**
5. **Partition-level recovery contract**

Everything else - fault injection, benchmarking, verification execution,
safety cases, security tooling, target build coordination - connects to these
five responsibilities without being implemented by GoMyRobotOS.

## Where to read next

| If you want to…                 | Start here                                                 |
| ------------------------------- | ---------------------------------------------------------- |
| Understand the why and the model | [Concepts overview](../concepts/overview) and [Architecture overview](../architecture/overview) |
| Read the central artifact       | [Partition Contract overview](../contract/overview)        |
| See what runs inside a partition| [GoMyRobotRT](../components/gomyrobotrt)                   |
| Track what gets built when      | [Milestones](../milestones/overview)                       |

```{note} Status
Everything in this documentation is specification-level: milestone M0
(Architecture and Contract Freeze). Implementation begins at milestone M1
(x86-64 reference partition).
```
