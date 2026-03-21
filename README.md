# 📊 Cashflow Model — Fixed Income Analytics Engine

![Status](https://img.shields.io/badge/status-complete-brightgreen)
![Python](https://img.shields.io/badge/python-3.11%20%7C%203.13-blue)

## Overview

This project implements a **modular fixed income analytics engine** from scratch. It models bonds and loans, projects cashflows, calculates present value and yield, and evaluates interest rate risk using scenario analysis.

The goal is to demonstrate a **clear understanding of core fixed income concepts and how they are implemented in code**, not just theoretical knowledge.

### Business Impact (Why it matters)

This engine represents the core logic used in desk/risk workflows where teams need to:

* Value plain-vanilla fixed income instruments consistently
* Estimate interest-rate sensitivity quickly for scenario discussions
* Standardize JSON-based inputs/outputs for integration with APIs, notebooks, or dashboards

In practical terms, it provides a reliable foundation for pricing checks, what-if analysis, and portfolio-level extensions.

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
│   ├── test_cf1.py
│   ├── test_cf2.py
│   ├── test_cf3.py
│   ├── test_cf4.py
│   ├── test_cf5.py
│   ├── test_cf6.py
│
├── .github/workflows/
│   └── tests.yml          # CI: run tests on push/PR
│
├── Makefile               # local shortcut: make test
│
├── requirements.txt
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

This project is designed as a compact fixed income analytics library for learning, portfolio modeling, and interview demonstration.

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

### Scenario Analysis

```
Scenario        NPV      $ Change   % Change
-------------------------------------------
Rates +1%     999.76     -44.56      -4.27%
Rates -1%    1091.43      47.12       4.51%
```

### Duration Approximation

```
Estimated P&L: -45.81
Actual P&L:    -44.56
```

Representative outputs above are generated from the included scripts in [tests](tests).

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

* **Stability over speed:** bisection for YTM is slower than Newton methods, but more robust for interview/demo-grade code.
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
* Portfolio-level risk aggregation (DV01, VaR)
* Real market data integration via APIs or data vendors

---

## Skills Demonstrated

* Fixed income mathematics (NPV, YTM, duration)
* Numerical methods (bisection root finding)
* Date and time convention handling
* Financial modeling in Python
* Object-oriented design
* Risk analysis and scenario testing

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

Run an individual module if needed:

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

## Key Takeaways

This project demonstrates:

* Understanding of fixed income fundamentals
* Ability to translate finance theory into code
* Structured, modular system design
* Practical handling of real-world data formats
* Risk analysis using duration and scenario testing

