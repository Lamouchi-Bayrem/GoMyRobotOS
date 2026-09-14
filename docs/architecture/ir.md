# GoMyRobotOS IR (Intermediate Representation)

## Purpose

The IR is the stable internal representation **between the contract and the
backends**:

```text
Partition Contract
       │
       ▼
Parser
       │
       ▼
Validator
       │
       ▼
GoMyRobotOS IR
       │
       ├───────────────┬────────────────┐
       ▼               ▼                ▼
     Xen            XNG/XtratuM       Future
    Backend           Backend         Backend
```

Without an IR, each backend would consume the contract format directly, and
the contract format would silently become the union of every backend's
quirks. The IR is what protects the portability claim: backends compete at
the IR, not at the YAML.

## Shape

A GoMyRobotOS IR partition carries the full semantic content of its
contract, normalized:

```text
Partition
 ├── CPU resources
 ├── memory resources
 ├── interrupt resources
 ├── DMA resources
 ├── device resources
 ├── communication
 ├── timing
 ├── security
 └── recovery
```

Normalization means, for example, that a declared cpu-set, scheduling policy,
priority, and timing budget together form an *execution requirement* the
backends can reason about uniformly - rather than three fields three
backends interpret three different ways.

The backend then determines how those semantics are expressed on the
target. The IR never encodes that expression.

## Guarantees the IR is responsible for

| Guarantee                      | Meaning                                                        |
| ------------------------------ | --------------------------------------------------------------- |
| Semantic equivalence           | contract → IR is meaning-preserving (checked by validator)     |
| Backend independence           | no IR node is backend-specific; target data rides in a backend profile |
| Reviewability                  | the IR for a deployment is inspectable as assurance evidence   |
| Comparability                  | IR-to-IR comparison across targets is the core measurement primitive for Research Problem 1 |

## Status

```text
IR v1 (specification):  frozen with M0
IR implementation:     Status: Planned (M1)
```

The IR document and the Backend API document both freeze at M0; their code
form appears with the M1 x86-64 reference partition.
