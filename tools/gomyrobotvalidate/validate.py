#!/usr/bin/env python3

import sys
import yaml


def check_budget_vs_period(contract):
    errors = []

    tb = (
        contract.get("execution", {})
                .get("timing_budget")
    )

    if not tb:
        return errors

    budget = tb["budget_us"]
    period = tb["period_us"]

    if budget > period:
        errors.append(
            f"budget_us ({budget}) exceeds "
            f"period_us ({period})"
        )

    return errors


def check_wcet_vs_budget(contract):
    errors = []

    tb = (
        contract.get("execution", {})
                .get("timing_budget")
    )

    if not tb:
        return errors

    wcet = tb.get("wcet_bound_us")

    if wcet is None:
        return errors

    if wcet > tb["budget_us"]:
        errors.append(
            f"wcet_bound_us ({wcet}) exceeds "
            f"budget_us ({tb['budget_us']})"
        )

    return errors


def check_dma_regions(contract):
    errors = []

    memory_regions = {
        region["name"]
        for region in contract["memory"]["regions"]
    }

    dma = contract.get("dma", {})
    permitted = dma.get(
        "permitted_regions",
        []
    )

    for region in permitted:
        if region not in memory_regions:
            errors.append(
                f"DMA region '{region}' "
                f"does not exist"
            )

    return errors


def check_duplicate_memory_regions(contract):
    errors = []

    names = []

    for region in contract["memory"]["regions"]:
        name = region["name"]

        if name in names:
            errors.append(
                f"duplicate memory region "
                f"'{name}'"
            )

        names.append(name)

    return errors


def check_duplicate_endpoints(contract):
    errors = []

    endpoints = (
        contract.get("communication", {})
                .get("endpoints", [])
    )

    names = []

    for endpoint in endpoints:

        name = endpoint["name"]

        if name in names:
            errors.append(
                f"duplicate endpoint "
                f"'{name}'"
            )

        names.append(name)

    return errors


def run_checks(contract):

    errors = []

    errors.extend(
        check_budget_vs_period(contract)
    )

    errors.extend(
        check_wcet_vs_budget(contract)
    )

    errors.extend(
        check_dma_regions(contract)
    )

    errors.extend(
        check_duplicate_memory_regions(contract)
    )

    errors.extend(
        check_duplicate_endpoints(contract)
    )

    return errors


def main():

    if len(sys.argv) != 2:
        print(
            "usage: validate.py "
            "<contract.yml>"
        )
        sys.exit(1)

    with open(sys.argv[1]) as f:
        contract = yaml.safe_load(f)

    errors = run_checks(contract)

    if errors:

        print("\nVALIDATION FAILED\n")

        for error in errors:
            print(f"[ERROR] {error}")

        sys.exit(1)

    print("\nVALIDATION PASSED\n")


if __name__ == "__main__":
    main()
