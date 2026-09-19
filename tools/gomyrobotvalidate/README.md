# GoMyRobotValidate

Semantic validator for
GoMyRobotOS partition contracts.

## Checks

- Budget <= Period
- WCET <= Budget
- DMA regions exist
- Duplicate memory regions
- Duplicate endpoint names

## Usage

```bash
python3 validate.py \
../../examples/x86-64/flight-control.yml
