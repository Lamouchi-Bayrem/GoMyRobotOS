# GoMyRobotBench

[GoMyRobotBench](https://gomyrobot.com/products/bench/) owns the **physical experiment infrastructure** of the
GoMyRobot stack.

```text
GoMyRobotBench
 ├── hardware-in-the-loop
 ├── board orchestration
 ├── FPGA instrumentation
 ├── timing capture
 ├── external instrumentation
 └── experiment control
```

## Division of labor with GoMyRobotOS

* **GoMyRobotBench** decides how the hardware experiment is *physically
  executed*: which board, which scope probes, which FPGA capture plan, how
  boards are orchestrated in a farm.
* **GoMyRobotOS** provides the *measurements and interfaces required by the
  experiment*: the declared timing budgets to be measured against, the
  health/recovery hooks to observe, the deployment identity to log.

That division keeps GoMyRobotOS from becoming "an everything
measurement/safety product" - the bench is the experiment platform, the OS
is the object under experiment that exposes contractual semantics.

## Where Bench shows up in the plan

* **M1** - basic fault containment and reproducible boot on x86-64 run
  through bench-style test harnesses in CI.
* **M3 - Interference laboratory.** Bench builds **GMR-INTERF v1**:
  stressors (CPU, cache, memory, DMA, IRQ, I/O) and
  metrics (latency, jitter, throughput, interference) run progressively on
  x86-64 → NG-ULTRA → HPSC. The science goals are in
  [Research problem 2 (multi-channel
  interference)](../research/research-problems) and
  [Validation: Interference](../validation/interference).
* **M5+** - fault, test, and timing results from Bench, Verify, and
  Fault feed the
  [evidence graph](../assurance/evidence-graph)
  automatically.

## Bench does not redefine platform behavior

A bench run can only *measure* what the contract declares and the backend
realizes. If a measurement contradicts the declared semantics, that is an
architecture bug to be fixed (by ADR and milestone work), not a bench
configuration to be tuned around.

`Status: External product; experiment infrastructure not implemented in
this repository. Bench integrations are planned (M1, M3, M5).`
