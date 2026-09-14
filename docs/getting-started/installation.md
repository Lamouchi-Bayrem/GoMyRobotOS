# Installation

```{warning} GoMyRobotOS software is not implemented yet
GoMyRobotOS is at milestone **M0** (Architecture and Contract Freeze).
There is no GoMyRobotOS binary, daemon, or command-line tool to install
today, and none of the described targets host a GoMyRobotOS deployment.

`Status: Not implemented` - the first implementations land at milestone
**M1** (x86-64 reference partition), which will:

* parse and validate a Partition Contract
* produce the GoMyRobotOS IR
* realize partitions through a Xen backend on x86-64
* boot and deploy partitions
* provide basic partition monitoring
```

## What is available today

The M0 deliverables are specification artifacts, all in this repository:

* This documentation (Sphinx + MyST), including the Partition Contract v1
  specification: [Specification](../contract/specification)
* The Partition Contract JSON Schema:
  `schemas/partition-contract.schema.json`
* Illustrative contract examples per target: `examples/x86-64/`,
  `examples/ng-ultra/`, `examples/hpsc/`

## Building this documentation locally

The documentation is built with Sphinx and MyST Markdown. No proprietary
tooling is required:

```bash
git clone https://github.com/gomyrobot/GoMyRobotOS.git
cd GoMyRobotOS

python3 -m venv .venv
. .venv/bin/activate
pip install -r docs/requirements.txt

python -m sphinx -b html docs docs/_build/html
```

Open `docs/_build/html/index.html` in a browser. The same build runs in
GitHub Actions (`.github/workflows/gh-pages.yml`) and deploys the live
site (<https://gomyrobot.github.io/GoMyRobotOS/>) on every push to
`main`; a read-only mirror is kept on Read the Docs
(<https://gomyrobotos.readthedocs.io>).

## What M1 will add

When milestone M1 ships, this page will be updated with:

* the x86-64 reference deployment (partition boot, deployment artifacts)
* the host toolchain requirements for the Xen backend
* the QEMU-based CI configuration used for reproducible boot testing

Until then, avoid documentation that references GoMyRobotOS tool names, CLI
flags, or deployment commands - the architecture deliberately does not
define them yet, and inventing them would violate the project's
anti-hallucination policy.
