# Compatibility: ROS 2

```{note} Required statement (documentation policy)
```text
ROS 2 Documentation Reference: Rolling

Primary reference:
https://docs.ros.org/en/rolling/

[GoMyRobotRT](https://gomyrobot.com/products/rt/) ROS 2 compatibility:
Not implemented (this repository does not contain GoMyRobotRT).
Roadmap status: Planned research (see GoMyRobotRT page); no feature is
claimed as supported until implemented and documented.
```
```

This page separates two things that must never be conflated:

```text
ROS 2 Rolling documentation reference
    ≠
full ROS 2 Rolling runtime compatibility
```

The first is a *documentation choice* (this project uses the official
Rolling documentation as the authority for ROS 2 terminology and API
names). The second is an *implementation property* that does **not**
currently exist - nothing in this repository executes, integrates, or
wraps ROS 2 at all, and the documentation does not imply otherwise.

## Concept-by-concept status

The table lists the ROS 2 concepts this project's documentation refers
to, with the status of *GoMyRobotRT* support. (GoMyRobotOS has no ROS 2
"support" level at all - it manages an execution environment; see the
policy page
[components/ros2-rolling]
(../components/ros2-rolling).)

| ROS 2 concept (Rolling term) | GoMyRobotRT status | Notes |
| ---------------------------- | ------------------ | ----- |
| `rcl` / `rclcpp` / `rclpy` | Not implemented | planned: C/C++ client libs on RTEMS; `rclpy` out of flight profile |
| node | Not implemented | planned concept; standard Rolling semantics preserved |
| executor | Not implemented | deterministic execution constraints are *planned research*, not standard ROS 2 |
| publisher / subscription | Not implemented | cross-partition traffic maps to *contract endpoints*, not the topic graph |
| service | Not implemented | planned as a workload primitive |
| action | Not implemented | no plan published yet - documented only if planned later |
| parameter | Not implemented | - |
| QoS | Not implemented | which profiles survive a bounded partition: research |
| callback group | Not implemented | standard meaning preserved; RT-side behavior TBD by research |
| middleware / RMW / DDS | Not implemented | role on RTEMS partitions: open research |
| ROS 2 graph | Not implemented | graph topology belongs to the workload, not to the contract |
| lifecycle | Not implemented | alignment of lifecycle state with contract recovery: open question |

Rules for any future update to this table (documentation policy):

1. "Implemented" requires code in the repository that implements the
   feature *and* a page that documents it.
2. Behavior that *differs* from standard ROS 2 must be written as:
   standard behavior (with Rolling link) + GoMyRobotRT behavior separately
   + label (implemented / experimental / planned).
3. No GoMyRobot-named alternatives to standard concepts (`GoMyRobotNode`
   etc. are prohibited).
4. This page is updated whenever GoMyRobotRT lands a ROS 2 integration -
   it must never drift from the component page
   [components/gomyrobotrt]
   (../components/gomyrobotrt).

## What "compatible" could mean (future, not now)

If and when GoMyRobotRT implements ROS 2 integration, compatibility will
be stated as a *list of supported concepts* (per the table), not as "we
support ROS 2". Supported lists, limitations on RTEMS targets, and
deterministic-execution constraints will all live on the component page;
this page remains the cross-check table.
