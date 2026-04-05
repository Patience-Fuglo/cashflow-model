# 📊 Cashflow Model — Fixed Income Analytics Engine

![Status](https://img.shields.io/badge/status-complete-brightgreen)
![Python](https://img.shields.io/badge/python-3.11%20%7C%203.13-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Overview

This project implements a **modular fixed income analytics engine** from scratch. It models bonds and loans, projects cashflows, calculates present value and yield, and evaluates interest rate risk using scenario analysis.

The goal is to provide a **clear, from-scratch implementation of core fixed income concepts** with clean, readable code.

### Business Impact (Why it matters)

This engine represents the core logic used in desk/risk workflows where teams need to:

* Value plain-vanilla fixed income instruments consistently
* Estimate interest-rate sensitivity quickly for scenario discussions
* Standardize JSON-based inputs/outputs for integration with APIs, notebooks, or dashboards

In practical terms, it provides a reliable foundation for pricing checks and what-if analysis.

---

## What This Project Covers

This system replicates the **core building blocks used in real-world quant and trading systems**:

* Instrument modeling (bonds, loans)
* Day count conventions (ACT/360, ACT/365, 30/360, ACT/ACT)
* Interest calculations (simple & compound)
* Accrued interest and clean vs dirty pricing
* Cashflow projection engine
* Present value (NPV) and Yield-to-Maturity (YTM)
* Duration and interest rate sensitivity
* Scenario analysis (rate shocks)
* JSON input/output integration

---

## Project Structure

```
Cashflow Model/
│
├── cashflow_model/
│   ├── __init__.py          # Public API exports
│   ├── instrument.py        # Bond and Loan classes
│   ├── day_count.py         # Year fraction calculations
│   ├── accrual.py           # Interest & accrued interest
│   ├── present_value.py     # NPV, YTM, duration
│   ├── scenario.py          # Scenario analysis engine
│   └── io_adapter.py        # JSON input/output integration
│
├── examples/
│   ├── instrument_schema.json
│   └── cashflow_examples.json
│
├── tests/
│   ├── test_cf1.py          # Scenario analysis tests
│   ├── test_cf2.py          # Day count convention tests
│   ├── test_cf3.py          # Accrual & interest tests
│   ├── test_cf4.py          # Cashflow engine tests
│   ├── test_cf5.py          # Present value tests
│   └── test_cf6.py          # Rate sensitivity tests
│
├── .github/workflows/
│   └── tests.yml            # CI: run tests on push/PR
│
├── demo.py                  # Interactive demo script
├── Makefile                 # local shortcut: make test
├── requirements.txt
├── LICENSE
└── README.md
```

### High-Level Architecture

```text
JSON Input -> io_adapter -> instrument/day_count/accrual/cashflow_engine
         |
         v
       present_value + scenario
         |
         v
          JSON/console output
```

---

## Environment

Built and tested with Python 3.11 and 3.13.

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Key Features

### 1. Instrument Modeling

Supports:

* Fixed coupon bonds
* Amortizing loans


* Face value
* Coupon rate

---

### 2. Day Count Conventions

Implements:

* ACT/360
* ACT/365
* 30/360
* ACT/ACT

These determine how time is measured between dates for interest calculations.

---

### 3. Interest Calculations

* Simple interest:

  ```
  principal × rate × time
  ```
* Compound interest:

  ```

---

### 4. Accrued Interest & Pricing

* Calculates accrued interest between coupon dates
* Converts:

  * Dirty price → actual transaction price
  * Clean price → quoted market price

---

### 5. Cashflow Engine

Projects all future payments:

#### Bonds

* Coupon payments
* Principal repayment at maturity

#### Loans

* Monthly interest + principal breakdown
* Decreasing balance over time

---

### 6. Present Value & Yield

Implements:

* Discounting:

  ```
  PV = CF / (1 + r)^t
  ```

* Net Present Value (NPV)

* Yield-to-Maturity (YTM) via bisection search

* Macaulay Duration

* Modified Duration

---

### 7. Scenario Analysis

Simulates interest rate shocks:

* ±0.5%, ±1%, ±2%

Outputs:

* New bond price (NPV)
* Dollar change
* Percentage change

Also includes:

```
P&L ≈ -Duration × ΔRate × Price
```

---

### 8. JSON Integration

Supports real-world data formats:

#### Input

* Schema-based instrument definition

#### Output

* Structured cashflow format:

```json
{
  "date": "2024-07-01",
  "type": "coupon",
  "amount": 25.0
}
```

---

## Example Output

### Bond Cashflow Schedule

```
Date            Type         Amount   Running Total
----------------------------------------------------------
2025-01-01      COUPON        50.00           50.00
2026-01-01      COUPON        50.00          100.00
2027-01-01      COUPON        50.00          150.00
2027-01-01      PRINCIPAL   1000.00         1150.00
```

### Present Value & Duration

```
Bond: 3Y 5% Annual Coupon
Discount Rate: 4%
NPV: $1027.75 (premium bond)
Macaulay Duration: 2.86 years
Modified Duration: 2.75
YTM (at market price $1027.75): 4.00%
```

### Scenario Analysis

```
Base NPV: $1044.31

Scenario        NPV       $ Change    % Change
-----------------------------------------------
Rates +0.5%    1021.70      -22.61       -2.17%
Rates +1%       999.76      -44.56       -4.27%
Rates +2%       957.88      -86.44       -8.28%
Rates -0.5%    1067.62       23.31        2.23%
Rates -1%      1091.65       47.34        4.53%
Rates -2%      1142.16       97.85        9.37%
```

### Loan Amortization

```
Date            Type         Amount   Running Total
----------------------------------------------------------
Month 1         INTEREST      41.67           41.67
Month 1         PRINCIPAL    158.33          200.00
Month 2         INTEREST      40.35          240.35
Month 2         PRINCIPAL    159.65          400.00
...
Month 60        INTEREST       1.64        10645.05
Month 60        PRINCIPAL    198.36        10843.41

Total Interest Paid: $843.41
```

### Test Suite Output

```
$ python -m tests

=== tests.test_cf1 ===
PASS test_estimate_pnl_from_duration
PASS test_run_all_scenarios
PASS test_run_scenario
...
5 run, 5 passed, 0 failed in 0.00s

=== tests.test_cf2 ===
PASS test_actual_360_jan_to_jul
PASS test_actual_365_jan_to_jul
...
11 run, 11 passed, 0 failed in 0.00s

=== SUMMARY ===
All modules passed.
```

All outputs above are generated from the included test modules.

---

## Results & Validation

The model was validated against known financial relationships:

* A 5% coupon bond priced at a 4% discount rate produced NPV ≈ $1027, consistent with a premium bond
* The YTM solver converged to ~4% when market price was set equal to the calculated NPV
* Macaulay duration for the sample 3-year bond was ≈ 2.86 years, which is directionally consistent with theory
* Scenario analysis showed the expected inverse relationship between rates and price:
  * Rates ↑ → Price ↓
  * Rates ↓ → Price ↑
* Duration-based P&L approximation closely matched full repricing results

These checks provide confidence that the pricing and risk outputs are numerically consistent.

---

## Design Decisions

* Modular architecture: each financial concept (instrument modeling, accrual, pricing, scenario analysis) is isolated in its own module
* Explicit day count conventions to reflect real market calculation standards
* Bisection method for YTM to favor numerical stability and predictable convergence
* Separation between analytics modules and test/integration scripts for cleaner extensibility

---

## Design Trade-offs

* **Stability over speed:** bisection for YTM is slower than Newton methods, but more robust and easier to debug.
* **Clarity over market completeness:** flat-rate discounting keeps pricing logic readable at the cost of full curve realism.
* **Deterministic flows over realism:** no prepayments/default modeling in loan cashflows to keep outputs auditable.

---

## Limitations

* Assumes flat interest rates rather than a full yield curve
* Does not incorporate convexity in rate sensitivity estimates
* Loan cashflow model assumes fixed payments and no prepayments
* No stochastic interest rate or Monte Carlo modeling

---

## Future Work

* Yield curve integration and term structure modeling
* Convexity adjustment for more accurate sensitivity estimates
* Monte Carlo interest rate simulations
* Multi-instrument risk aggregation (DV01, VaR)
* Real market data integration via APIs or data vendors

---

## Technical Coverage

* Fixed income mathematics: NPV, YTM, duration
* Numerical methods: bisection root finding
* Date handling: multiple day count conventions
* Risk analysis: scenario testing and sensitivity

---

## Quick Start

```bash
pip install -r requirements.txt
make test
```

or:

```bash
python -m tests
```

Run the interactive demo:

```bash
python demo.py
```

Run an individual test module:

```bash
python -m tests.test_cf1
python -m tests.test_cf2
python -m tests.test_cf3
python -m tests.test_cf4
python -m tests.test_cf5
python -m tests.test_cf6
python -m tests.test_download_integration
```

Note: Tests are executable as plain Python modules and do not require `pytest`.

---

## Continuous Integration

GitHub Actions runs `python -m tests` automatically on every push and pull request using Python 3.11 and 3.13.

---

## Performance Snapshot

On local macOS runs with Python 3.13, full-suite execution (`python -m tests`) completes in about **0.81s** (`real` time), while all tests pass.

---

## Summary

This project provides a self-contained implementation of core fixed income analytics:

* Accurate cashflow projection for bonds and loans
* Standard day count conventions used in industry
* NPV, YTM, and duration calculations
* Scenario analysis for interest rate risk
* JSON-based input/output for integration

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

