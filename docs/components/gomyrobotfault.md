# GoMyRobotFault

Fault injection and fault modeling **remain outside GoMyRobotOS**
([ADR-0010](../development/architecture-decisions)).

The split is precise:

* **GoMyRobotOS defines:** *what the partition should do when a fault
  occurs*, the `recovery.*` contract fields, the recovery hooks, the
  escalation surface ([Recovery
  model](../architecture/recovery-model)).
* **[GoMyRobotFault](https://gomyrobot.com/products/fault/) defines:** *how the fault is generated*, the fault
  library, the fault recipes, and the harnesses that apply them.

## Fault classes

```text
CPU
memory
DMA
interrupt
I/O
communication
partition crash
watchdog
resource exhaustion
image corruption
```

Validating GoMyRobotOS's recovery semantics against these classes is one of
the declared verification areas, see
[Validation: Fault injection](../validation/fault-injection).

## Radiation belongs here, not in GoMyRobotOS

Radiation effects are **not** implemented as a GoMyRobotOS function. The
pipeline is:

```text
Radiation / SEU / TID models
            ↓
      GoMyRobotFault
            ↓
     QEMU / emulator
            ↓
    target fault mechanism
            ↓
       GoMyRobotOS
            ↓
 detection → containment → recovery
            ↓
     verification evidence
```

QEMU can therefore *model radiation-induced fault effects*, but QEMU does
**not** reproduce the physical radiation environment. The documentation
never describes QEMU as "radiation", and never describes a QEMU experiment
as radiation-qualification evidence.

NG-ULTRA is particularly relevant to this stream because it is
explicitly radiation-hardened-by-design and includes mechanisms such as
EDAC, configuration scrubbing, and memory/configuration protection -
hardware behavior the fault models must stay correlated with.

## Ladder from model to physics

The intended progression for every fault family:

```text
software fault model
        ↓
QEMU / emulation
        ↓
FPGA / HIL
        ↓
real HPSC / NG-ULTRA
        ↓
radiation / SEE testing
        ↓
correlation
```

The science result is: *how well do software-level fault models predict
containment and recovery behavior for space-relevant hardware fault
mechanisms*, a GoMyRobotFault / [GoMyRobotBench](https://gomyrobot.com/products/bench/) / [GoMyRobotAssure](https://gomyrobot.com/products/assure/) research
stream, not a GoMyRobotOS subsystem
([Research problem 4](../research/research-problems)).

```{note}
GoMyRobotOS's only obligation in this chain is to *react* to injected
faults per the contract, and to *record* what it did (recovery action,
safe state, escalation) so the external stream can measure
T_detect / T_contain / T_recover / T_resume.
```
