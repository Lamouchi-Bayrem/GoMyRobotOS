# Validation Methodology

This section describes how GoMyRobotOS validates its *own* claims:
reproducible boot, functional runtime validation, temporal isolation,
spatial isolation, interference, fault injection, and recovery timing.

## First rule: what validation is and is not

```{warning} No certification claims exist at M0
GoMyRobotOS validation is an engineering research methodology. The
documentation **does not** claim:

* formal WCET
* certification
* safety certification
* complete freedom from interference

...unless and until actual evidence exists from the experiments described
here. Every page in this section carries the same rule as the rest of the
project: `Status` labels only, no invented results.
```

## The declared validation areas

| Area                              | Page                                    | What it validates                              |
| --------------------------------- | --------------------------------------- | ---------------------------------------------- |
| reproducible boot                 | [M1](../milestones/m1)               | same contract → same boot, machine to machine  |
| functional runtime validation     | [M1](../milestones/m1)               | partition boots, runs, communicates            |
| temporal isolation                | [Temporal isolation](temporal-isolation) | budget respected under load                 |
| spatial isolation                 | [Spatial isolation](spatial-isolation) | declared memory/IRQ/DMA/device boundaries hold |
| interference                      | [Interference](interference)         | cross-partition effects, multi-channel         |
| fault injection                   | [Fault injection](fault-injection)   | contract recovery semantics under fault        |
| recovery timing                   | [Recovery](recovery)                 | T_detect / T_contain / T_recover / T_resume    |

## How the results feed the rest of the ecosystem

```text
validation experiments (this section)
        │
        ▼
test / evidence artifacts
        │
        ├──→ GoMyRobotVerify   (result processing, coverage, traceability)
        └──→ GoMyRobotAssure   (evidence graph, assurance argument)
```

GoMyRobotOS *produces* the artifacts; the external products *interpret*
them (ADR-0012). That is why this section is careful with two words:
"validated" (a runnable experiment existed and its result is recorded)
versus "demonstrated" (the acceptance gate of a milestone passed).

## Ladder of where validation runs

```text
host CI (x86-64)
   → QEMU (reproducible environment)
   → NG-ULTRA hardware (flight reference)
   → HPSC (research)
```

Measurements move *up* this ladder only when a lower-level measurement
calls for hardware-specific evidence; the ladder is the same one
[GoMyRobotBench](../components/gomyrobotbench) uses for physical
experiments.
