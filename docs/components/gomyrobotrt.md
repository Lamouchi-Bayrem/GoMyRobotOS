# GoMyRobotRT

GoMyRobotRT is the **deterministic flight runtime** of the GoMyRobot stack.
It remains a separate product from GoMyRobotOS.

> **GoMyRobotRT executes the robotics workload.**
> **GoMyRobotOS controls the execution environment in which that workload
> runs.**

This page documents GoMyRobotRT's **intended integration architecture** as
frozen at M0. Nothing on this page is implemented in this repository
(`Status: Not implemented` for GoMyRobotRT itself; the integration work is
planned research).

## Overview and responsibilities

```text
GoMyRobotRT
 ├── RTEMS
 ├── nano-ros
 ├── rcl/rclcpp
 ├── deterministic executors
 ├── robotics middleware
 ├── hardware abstraction
 └── flight application interfaces
```

| Responsibility              | What it means                                          |
| --------------------------- | ------------------------------------------------------ |
| RTEMS                       | the flight RTOS on which the runtime executes          |
| nano-ros                    | embedded robotics middleware support                   |
| rcl / rclcpp                | the ROS 2 client libraries (see below)                 |
| deterministic executors     | executor behavior adapted to flight-grade determinism  |
| robotics middleware         | the ROS 2 concepts the flight workloads are written in |
| hardware abstraction        | the seam between workload code and flight hardware     |
| flight application interfaces | the stable interfaces mission software programs  against |

GoMyRobotOS consumes or hosts GoMyRobotRT inside managed partitions - the
hosting mechanics are in the
[Runtime model](../architecture/runtime-model).

## ROS 2 Rolling integration

The ROS 2 reference for every concept below is the official
[ROS 2 Rolling documentation](https://docs.ros.org/en/rolling/). This page
(and the whole GoMyRobotOS documentation) **never duplicates ROS 2
documentation** - for each concept we (1) state the standard ROS 2 meaning
briefly, (2) link the Rolling page, (3) state GoMyRobotRT's planned
integration, and (4) identify GoMyRobot-specific constraints or RTEMS
limitations. Everything in section (3) below is
`Status: Not implemented / Research` - per the project's
anti-hallucination policy, no ROS 2 feature is claimed as supported by
GoMyRobotRT before it exists (see
[Compatibility](../compatibility/ros2)).

### rcl / rclcpp / rclpy - client libraries

*Standard ROS 2.* `rcl`, `rclcpp` (C++) and `rclpy` (Python) are the client
libraries above the middleware (RMW); they implement nodes, publishers,
subscriptions, services, actions, parameters, timers, and the executor
service patterns. See the
[ROS 2 Rolling documentation](https://docs.ros.org/en/rolling/) for the
client-library entry points
([How-to: Basic client
libraries](https://docs.ros.org/en/rolling/Tutorials/Beginner-Client-Libraries/)):

*GoMyRobotRT.* Planned to carry `rcl`/`rclcpp` (C/C++) on RTEMS. `rclpy`
(Python) is **not** part of the flight-partition profile: the flight domain
is C/C++ on RTEMS, and Python-based development stays in service (Linux)
domains. That split is a GoMyRobotRT profile decision, not a ROS 2
limitation, and GoMyRobotRT does **not** claim rclpy support on RTEMS.

### Executors

*Standard ROS 2.* An executor drives callbacks for one or more nodes by
polling the middleware; callback groups and multi-threaded executors shape
when and where callbacks run. See the Rolling
[ROS 2 Rolling Glossary](https://docs.ros.org/en/rolling/Glossary.html)
for the executor and callback-group terms.

*GoMyRobotRT.* Planned to follow the ROS 2 executor model while imposing
GoMyRobot-specific deterministic constraints (fixed priorities, bounded
callback windows tied to the partition's contract `timing_budget`). Those
constraints are **not** standard ROS 2 behavior and must never be
presented as such.

### Publishers, subscriptions, services, actions, parameters

*Standard ROS 2.* These are the ROS 2 communication and parameter
primitives, implemented over the middleware (RMW); type, QoS, and graph
semantics are defined by ROS 2. See the Rolling documentation's
[ROS 2 middleware and design
concepts](https://docs.ros.org/en/rolling/Concepts/About-ROS-2-Middleware.html).

*GoMyRobotRT.* Planned to support ROS 2 pub/sub + services as the flight
workload primitives. Cross-*partition* communication is **not** the ROS 2
topic graph - it is the bounded endpoint declared in the GoMyRobotOS
Partition Contract (`communication.endpoints`). How ROS 2 traffic maps onto
those contract channels is research work to be documented when implemented.
**No ROS 2 feature support is claimed at this time.**

### QoS

*Standard ROS 2.* QoS profiles (reliability, durability, history,
liveliness) are negotiated between publishers and subscriptions. See the
Rolling [Quality of
Service](https://docs.ros.org/en/rolling/Concepts/About-Quality-of-Service-Settings.html)
page.

*GoMyRobotRT.* Managing QoS inside a deterministically bounded partition is
**research**: which standard profiles make sense under a contract timing
budget will be documented when investigated.

### Middleware / RMW, DDS

*Standard ROS 2.* The ROS 2 Middleware (RMW) abstraction decouples client
libraries from the wire protocol (a DDS implementation or other
middleware). See the Rolling [ROS 2
Middleware](https://docs.ros.org/en/rolling/Concepts/About-ROS-2-Middleware.html)
concepts.

*GoMyRobotRT.* On RTEMS flight partitions the RMW/DDS stack plays a reduced
role compared to desktop Linux. What runs, how transports bind to contract
channels, and whether in-process or wire transports are used are research
decisions - documented only when chosen and implemented.

### Graph and lifecycle

*Standard ROS 2.* The ROS 2 graph (topics, services, actions and their
endpoints) and lifecycle node states are ROS 2 concepts documented in
Rolling (e.g., the [lifecycle
node](https://docs.ros.org/en/rolling/How-To-Guides/Understanding-ROS-2-Lifecycle-Nodes.html)
guide).

*GoMyRobotRT.* Aligning lifecycle states with *partition-level* recovery
(contract `recovery.*`) is an open integration question - not a claimed
feature.

## Deterministic execution

Where GoMyRobotRT differs from standard ROS 2 behavior, the documentation
policy applies: (1) state the standard behavior with the Rolling link,
(2) state the GoMyRobotRT behavior separately, (3) label it
(implemented / experimental / planned / research). At M0 every
GoMyRobotRT "deterministic execution" capability is `Status: Research` -
defined conceptually, not yet built or measured.

## Hardware abstraction and health monitoring

* **Hardware abstraction** isolates workload code from flight hardware so
  the same mission logic runs on x86-64 reference, NG-ULTRA, and future
  targets. `Status: Not implemented` here.
* **Health monitoring** exposes runtime health to the partition-level
  recovery surfaces GoMyRobotOS defines
  ([Recovery model](../architecture/recovery-model)).
  `Status: Not implemented` here.

## Flight workload integration

The end-state integration is: a GoMyRobotRT ROS 2 (Rolling-based) flight
workload runs inside a GoMyRobotOS-managed partition on RTEMS, with its
resources, timing, devices, and recovery declared in the partition's
contract - demonstrated first on NG-ULTRA (M2), with the same conceptual
flight partition booting on x86-64 (M1) before that. This is the
ServiceReady proof path: the *workload* is invariant; the *execution
environment* changes per target.