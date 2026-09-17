🛠️ Tooling & Approach
Tech Stack Used: Python (Pandas)

Methodology:
To solve this within the 2-hour time limit, I treated this as a data isolation problem. My approach was to progressively filter out the "knowns" to expose the "unknown" bug:

Ignored Floating-Point Noise: Filtered out differences (v2_total - v1_total) that were less than $0.01.

Ignored Documented Changes: Filtered out the books category entirely, as the rate change was approved and intentional.

Pattern Recognition: Ran value counts and cross-tabulations on the remaining anomalous dataset to identify the specific input conditions (express, category, coupon) triggering the regression.

Verification: Validated the findings by running a baseline sanity check against the unaffected orders to ensure the mean difference was practically zero.

🚀 Reproducing the Analysis
If you wish to run the analysis code provided in answers.json locally:

Ensure Python 3.x and pandas are installed.

Place the pricing_diff.csv file in the same directory as the script.

Run the script. The script is heavily commented and will output the exact integers and dollar amounts used in ANSWERS.md.
