# Pricing Refactor Regression - Answers

## 1. Naive `v2_total != v1_total` count

**Answer: 16,000 rows.**

This is not a useful bug count because the assignment explicitly says that tiny one- or two-cent differences are expected from floating-point/operation-order changes, and the `books` category was intentionally repriced. So a simple inequality check mixes harmless rounding noise and an approved pricing change with the actual regression.

## 2. Genuine pricing regression

**Answer: 985 orders.**

All 985 affected orders share these input conditions:

- `category = fragile`
- `express = True`
- `coupon` can be either empty or `SAVE10`

Breakdown by coupon:
- No coupon: **772**
- `SAVE10`: **213**

There were no affected orders outside the `fragile + express=True` combination after excluding the documented `books` pricing change and filtering out the stated cent-level floating-point noise.

## 3. Total customer overcharge

**Answer: $19,779.14 overcharged.**

This is the sum of `v2_total - v1_total` across the 985 genuine regression rows.

For reference, the average overcharge on an affected order is approximately **$20.08034518**.

## 4. Baseline sanity check

For orders that are **not in `books`** and **not affected by the `fragile + express=True` bug**, the average absolute difference between `v1_total` and `v2_total` is:

**$0.00988265306122449 (about 0.99 cents).**

The signed average `v1_total - v2_total` for the same baseline is approximately **$0.00022449**.

That baseline is at roughly the one-cent level described in the assignment, while the affected orders differ by an average of about $20.08. This makes the regression a distinct input-dependent pattern rather than a general shift in all prices.

## 5. Bonus - likely code-level bug

Based only on the data pattern, the refactored code appears to be **adding an extra express-related charge for `fragile` orders when `express=True`**.

The extra amount is very close to:

- **No coupon:** `5.00 + 0.10 * distance_km`
- **With `SAVE10`:** roughly 90% of that amount, consistent with the coupon discount

That suggests the fragile/express path in the refactor is probably applying an additional base-plus-distance charge that the old implementation did not apply. In plain English: **the express logic for fragile orders appears to add the delivery/base-distance component a second time (or otherwise route through a pricing branch that adds it again).**

## Investigation process

- Loaded all **20,000** rows from `pricing_diff.csv`.
- Computed `v2_total - v1_total` for every order using decimal arithmetic to avoid introducing new floating-point noise during the investigation.
- First counted exact inequality (`v2_total != v1_total`) and got **16,000** rows.
- Confirmed that the `books` rows form a separate, intentional pricing pattern rather than the regression.
- Applied the assignment's stated cent-level noise rule by treating absolute differences of **$0.02 or less** as non-material.
- Excluded `books` and inspected the remaining material differences.
- Found that every material non-book difference occurs at **`category=fragile` and `express=True`**.
- Grouped those rows by coupon and confirmed both coupon states are present, so `SAVE10` is not the root trigger.
- Summed the material differences to get the exact aggregate overcharge of **$19,779.14**.
- Computed the non-book, non-bug baseline mean absolute difference to verify that ordinary refactor noise is about **one cent**, not tens of dollars.
- As a bonus diagnostic, checked the affected-row difference against distance and found a strong match to an extra **$5 + $0.10/km** component, with the `SAVE10` rows behaving consistently with a 10% discount.

> Note: The bonus section is an inference from the observed input/output pattern; the assignment does not provide the pricing source code, so the exact code line cannot be determined from the CSV alone.
