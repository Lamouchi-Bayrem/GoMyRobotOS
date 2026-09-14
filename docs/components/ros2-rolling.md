# ROS 2 (Rolling) as the workload reference

This page records the documentation and version policy for ROS 2 in the
GoMyRobotOS project. It is the hub every other page links to for ROS 2
concepts.

## The position

ROS 2 is the **robotics middleware / workload environment** of the flight
stack. It is **not** the architectural center of GoMyRobotOS, not a
runtime, and not part of what "the OS" defines.

```text
ROS 2 Rolling
     │
     │ official robotics middleware / API model
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

The boundary is:

> **ROS 2 defines the robotics software model; GoMyRobotRT makes that model
> usable in the deterministic flight runtime; GoMyRobotOS controls the
> execution environment in which the workload runs.**

## The reference: ROS 2 Rolling, exclusively

For **all** ROS 2 concepts and APIs, the authoritative external reference
is the official Rolling documentation:

<https://docs.ros.org/en/rolling/>

This project documents terminology and API names consistent with Rolling —
including `rcl`, `rclcpp`, `rclpy`, executors, nodes, publishers,
subscriptions, services, actions, parameters, QoS, callback groups,
middleware / RMW, DDS, the ROS 2 graph, and lifecycle concepts.

Documentation from other ROS 2 distributions (Humble, Iron, Jazzy, Kilted,
older releases) is **not** mixed in unless a historical comparison is
explicitly required, and even then it is labeled as such.

## What this documentation does *not* do

* It does not reproduce large sections of the ROS 2 documentation.
* It does not create a second ROS 2 conceptual model, and it never makes
  ROS 2 the definition of GoMyRobotOS.
* It does not invent GoMyRobot-flavored replacements for standard concepts.
  The following fabricated terms are explicitly prohibited in this project
  and must never appear:

  ```text
  GoMyRobotNode
  GoMyRobotPublisher
  GoMyRobotExecutor
  ```

  A GoMyRobot-specific abstraction may be introduced only when there is a
  real architectural reason (e.g., the *partition contract*, which has none
  of these names — it is about execution domains, not ROS 2 objects).

## When GoMyRobotRT behavior differs from ROS 2

Any such difference must be documented as:

1. state the standard ROS 2 behavior (with the Rolling link),
2. state the GoMyRobotRT behavior separately,
3. identify whether the difference is implemented, experimental, or planned.

A GoMyRobotRT extension is never presented as an "official ROS 2 concept",
and ROS 2 terminology is never altered to make the GoMyRobot architecture
look cleaner.

## Linking rule

Use direct links to the official Rolling documentation wherever relevant —
the preferred pattern is:

> See the official
> [ROS 2 Rolling documentation](https://docs.ros.org/en/rolling/)
> for the underlying ROS 2 concept.

Links to random tutorials, outdated distributions, unofficial mirrors, or
third-party summaries are not used, unless a specific research reference
requires one (and then labeled as such). The complete concept-by-concept
status is in [compatibility/ros2](../compatibility/ros2).
