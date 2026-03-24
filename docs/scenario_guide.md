# Scenario Guide

How to run and interpret the scenario analysis module.

## Running scenarios

Run a named scenario from the config:
```bash
python -m src.scenario --scenario conservative
```

Run a custom scenario with specific factors:
```bash
python -m src.scenario --volume 0.9 --price 1.05
```

Run all named scenarios at once:
```bash
python -m src.scenario
```

Output is saved to `data/scenario_output.csv`.

## Predefined scenarios

| Scenario | Volume Factor | Price Factor | What it models |
|---|---|---|---|
| base | 1.00 | 1.00 | No shocks. The raw forecast. |
| conservative | 0.92 | 0.98 | Mild demand softening with slight price erosion. |
| optimistic | 1.08 | 1.03 | Demand recovery with modest price increases. |
| price_increase | 1.00 | 1.05 | 5% price hike, no volume change. Tests price elasticity assumption. |
| volume_decline | 0.85 | 1.00 | 15% volume drop, price unchanged. Models a market contraction. |
| recession | 0.80 | 0.95 | Stress test. 20% volume drop plus 5% price erosion. |

## Interpreting results

Each scenario produces a forecast with adjusted revenue, plus the original confidence intervals scaled by the same factors. Compare scenarios to the base to quantify the revenue impact of each assumption.

The FP&A team typically presents three scenarios to the CFO: base, conservative, and optimistic. The range between conservative and optimistic becomes the "forecast band" for quarterly guidance.

## Adding new scenarios

Edit `config/scenarios.yaml`. Add a new entry with a volume_factor and price_factor. Run the scenario module and the new scenario will appear in the output.

Factors are multiplicative. A volume_factor of 0.9 means 90% of the base forecast volume. A price_factor of 1.1 means 110% of the base forecast price. The revenue impact is the product of both factors.

## Limitations

The scenario module applies uniform shocks across all divisions and product lines. In practice, a volume decline may hit some divisions harder than others. For division-specific scenarios, filter the forecast to a single division before applying the shock, or modify the scenario module to accept division-level factors.

Mix scenarios (shifting revenue from one product line to another) are not currently supported in the simple factor model. Implementing them requires modifying the mix_share feature in the forecast and re-predicting. This is on the backlog.
