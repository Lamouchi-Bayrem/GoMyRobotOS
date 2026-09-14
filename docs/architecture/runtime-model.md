# Runtime model

The runtime model describes what happens **after** a backend has realized a
set of partitions: how workloads get into them, how they are supervised, and
where Yocto fits (and does not fit).

## Hosting the workload: GoMyRobotRT

> **GoMyRobotRT executes the robotics workload.**
> **GoMyRobotOS controls the execution environment in which that workload
> runs.**

GoMyRobotOS *consumes or hosts* GoMyRobotRT. Concretely, in the
flight-oriented reference stack:

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
        ↓
ROS 2 (Rolling-based) robotics workload
```

GoMyRobotRT's own responsibilities - RTEMS integration, nano-ros,
rcl/rclcpp, deterministic executors, robotics middleware, hardware
abstraction, flight application interfaces - are documented in
[GoMyRobotRT](../components/gomyrobotrt). From the runtime-model
perspective, GoMyRobotRT is a *workload artifact*: its boot path, resource
needs, and health behavior are declared in the hosting partition's
contract.

## The runtime responsibilities of GoMyRobotOS

For each managed partition, GoMyRobotOS's runtime side provides:

* **deployment** - placing boot artifacts (from the contract's
  `startup.boot_artifact`) into the backend's boot flow, in dependency
  order (from `startup.dependencies`),
* **lifecycle** - start, stop, restart as contractual recovery actions
  prescribe (implemented by GoMyRobotGuard, *specified* here),
* **health** - partition-level health observation usable by the recovery
  mechanism,
* **metadata** - the deployment manifest and hashes an assurance process
  consumes (the flow to GoMyRobotVerify / GoMyRobotAssure).

`Status: Planned` - the runtime layer is implemented at M1-M2 together
with the first backends. No runtime interfaces are defined yet beyond the
contract fields above.

## Service domains (Linux)

Deploys that include a service domain use a Linux image built by
**GoMyRobotBSP** - which is where Yocto/OpenEmbedded lives when a Linux
domain exists:

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

A full deployment can therefore contain:

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

```{important}
An RTEMS-only deployment does **not** need Yocto.
**GoMyRobotOS is not Yocto-based.** Yocto/OpenEmbedded is a target image
construction mechanism used by GoMyRobotBSP when Linux is part of the
deployment. Never describe GoMyRobotOS as "Yocto-based".
```
