# GoMyRobotBSP

GoMyRobotBSP owns **target realization and build coordination**.

> **GoMyRobotBSP is the target realization/build system.** It is not
> GoMyRobotOS.

GoMyRobotOS declares *what* a partition needs; GoMyRobotBSP decides *which
artifacts* the target needs to run it, and how those artifacts are built.

## Inputs and outputs

GoMyRobotBSP consumes:

```text
Partition Contract
      +
Hardware Profile
      +
Backend Profile
      +
Boot Profile
      +
Runtime Profile
```

and produces:

```text
boot artifacts
hypervisor configuration
RTEMS configuration
device tree / hardware description
Linux image
memory map
deployment manifest
hashes
build metadata
```

The split matters: contract + IR are what GoMyRobotOS *owns*; the profiles
(Hardware, Backend, Boot, Runtime) are what GoMyRobotBSP *consumes* to turn
semantics into buildable targets. Backend-specific information therefore
lives in the **backend profile** — never in the contract itself
([ADR-0002](../development/architecture-decisions),
[ADR-0009](../development/architecture-decisions)).

## Yocto's role

```{important}
**GoMyRobotOS is not Yocto-based.** Yocto/OpenEmbedded may be used by
GoMyRobotBSP to construct Linux deployment images — and only when a Linux
domain is part of the deployment.
```

Yocto sits *inside the target build pipeline* in that case:

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

So a final deployment can contain:

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

An RTEMS-only deployment does **not** need Yocto at all.

## Relationship to GoMyRobotOS

| Concern                     | Owner          | Notes                                        |
| --------------------------- | -------------- | -------------------------------------------- |
| Partition semantics          | GoMyRobotOS    | contract + IR                                |
| Boot ordering & recovery     | GoMyRobotOS    | contract `startup`, `recovery`               |
| Image construction           | GoMyRobotBSP   | dts, hypervisor config, Linux image, hashes  |
| Deployment manifest & hashes | GoMyRobotBSP   | consumed by assurance metadata               |

The deployment manifest and hashes GoMyRobotBSP produces are exactly the
evidence inputs the [assurance
model](../assurance/evidence-model) assumes.

`Status: As a product boundary, defined at M0. The GoMyRobotBSP build
pipeline itself is out of this repository's scope and is not implemented
here.`
