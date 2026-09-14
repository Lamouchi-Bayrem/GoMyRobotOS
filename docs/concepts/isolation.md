# Isolation

Isolation in GoMyRobotOS is a contract-level concept: the Partition Contract
declares *what must not be shared or reachable* between partitions. How that
declaration is enforced is a property of the target backend (Xen,
XNG/XtratuM, hardware WorldGuard - or future mechanisms), which is exactly
the layer the contract deliberately ignores.

## Isolation dimensions in the contract

| Dimension        | Contract expression                                        | Notes                                                                 |
| ---------------- | ---------------------------------------------------------- | --------------------------------------------------------------------- |
| Spatial (CPU)    | `execution.cpu_set`                                        | a partition sees only its assigned cpus                              |
| Temporal         | `execution.scheduling`, `execution.timing_budget`          | static allocation / bounded budget, not best-effort sharing          |
| Memory           | `memory.regions` with name, size, permissions              | partitions do not address each other's regions                       |
| DMA              | `dma.permitted_regions`                                    | DMA may only touch declared regions                                  |
| Interrupts       | `interrupts.owned`                                         | an interrupt belongs to exactly one partition                        |
| Devices          | `devices.ownership`                                        | device access is declared, not discovered                            |
| Communication    | `communication.endpoints` (size + rate bounds)             | everything cross-partition goes through declared, bounded channels   |
| Trust            | `partition.trust_domain`, `partition.criticality`          | drives how strictly the backend must enforce the above               |

Field definitions: [Contract specification](../contract/specification).

## What GoMyRobotOS specifies vs. what a backend realizes

GoMyRobotOS creates the invariants: no undeclared memory access, no
undeclared DMA, no unowned interrupt delivery, no unbounded channel traffic.
A backend *realizes* those invariants with its own mechanisms (page tables /
IOMMU / interrupt controllers on Xen; partition configuration on XtratuM;
hardware guard bands such as WorldGuard on HPSC).

```{warning} No "interference-free" claims
The M0 baseline explicitly forbids claiming complete freedom from
interference. What the architecture does claim is that interference has
*measured, contractual boundaries* - and that those boundaries must be
*measured*, not asserted (see
[Interference validation](../validation/interference) and
[Research problems](../research/research-problems)).
```

## Isolation and assurance

Determining which isolation properties can remain *invariant* across x86-64
+ Xen, NG-ULTRA + XNG/XtratuM, and HPSC + hardware partitioning is Research
Problem 1 - portable partition semantics. That question, not the existence of
any given mechanism, motivates the contract: the contract is what makes
difference-based reasoning between targets possible.
