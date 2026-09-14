# Architecture principles

These are the rules that the Final Architecture requires every design
decision to respect. Each maps to one or more ADRs - see
[Architecture decisions](../development/architecture-decisions).

## 1. Describe the semantics once; realize them per target

> **Describe the required execution semantics once; realize them according to
> the capabilities of the target platform.**

The same conceptual partition (same CPU allocation, memory regions, timing
budget, interrupt and device ownership, communication policy, startup and
recovery behavior) must be describable once in the Partition Contract,
independent of whether the target realizes it on Xen, on XNG/XtratuM, or
through hardware guard bands.

*(ADR-0002, ADR-0003)*

## 2. The hypervisor is a backend, not the abstraction

The abstraction is **not** "generate a Xen configuration" or "generate an XNG
configuration". The abstraction is: **define what a partition is allowed and
required to do.** Target backends are an implementation detail of the
contract, and the documentation must never collapse the two levels.

*(ADR-0003)*

## 3. The contract contains intent and constraints, not backend syntax

The contract must never contain backend-specific syntax such as
`xen_dom0`, `xtratum_partition_id`, or `xng_specific_option` unless the
property genuinely cannot be expressed at the portable semantic layer.
Backend-specific information belongs in the backend profile.

*(ADR-0002)*

## 4. The product stays a platform, not an "everything safety" monolith

GoMyRobotOS owns exactly five core responsibilities (partition definition,
resource/isolation semantics, backend realization, runtime integration,
partition-level recovery contract). Fault injection, benchmarking,
verification execution, assurance arguments, the security chain, and target
build coordination are sibling products - connecting to GoMyRobotOS, not
implemented inside it.

*(ADR-0007, ADR-0009, ADR-0010, ADR-0012)*

## 5. The robotics workload stays a workload

ROS 2 is a workload environment carried by [GoMyRobotRT](https://gomyrobot.com/products/rt/). GoMyRobotOS manages
the execution environment; it does not redefine robotics middleware
concepts. Standard ROS 2 terminology is reused verbatim; the only ROS 2
documentation reference is
[ROS 2 Rolling](https://docs.ros.org/en/rolling/).

*(ADR-0007, ADR-0008)*

## 6. Recovery must be independent of the domain it recovers

The component responsible for recovering a failed component must not depend
exclusively on the failed component. GoMyRobotOS therefore *specifies*
recovery semantics in the contract; the *implementation* of independent
recovery belongs to [GoMyRobotGuard](https://gomyrobot.com/products/guard/).

*(ADR-0011)*

## 7. Targets are honestly staged

Not every board is a product target. The initial matrix contains exactly
three roles - x86-64 (development/reference), NG-ULTRA (flight reference),
PIC64-HPSC (RISC-V research) - and each carries an explicit maturity label
(`Development / Reference`, `Flight Reference / Development`, `Research`).
Xen-on-HPSC is a research track, not a claimed production backend.

*(ADR-0004, ADR-0005, ADR-0006)*

## 8. Evidence, not assertions

GoMyRobotOS produces machine-readable evidence inputs (configuration, image
identity, required properties, test requirements, deployment metadata).
Whether they support a safety argument is decided outside the platform, by
[GoMyRobotVerify](https://gomyrobot.com/products/verify/) and [GoMyRobotAssure](https://gomyrobot.com/products/assure/). No WCET, certification, or
"interference-free" claims exist until measured.

*(ADR-0012)*

## 9. The documentation is versioned with the software

The documentation ships in-repo, is built by CI, and every maturity claim
uses one of the five status labels. Architecture changes require an ADR.

*(ADR-0013)*
