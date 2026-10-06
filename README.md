# LiftLens: Uplift-Based Targeting Engine

Most marketing models predict **who will convert**. LiftLens predicts
**who converts because of the ad**, so budget goes only to customers
whose behaviour actually changes.

## Status
🚧 In progress: Medium tier (uplift models)

## Roadmap
- [x] Easy: Experiment analysis on Hillstrom (ATE, z-tests, CIs, power/MDE)
- [ ] Medium: T/S-learner uplift models, Qini/AUUC, targeting policy
- [ ] Hard: Criteo Uplift, X-learner/causal forest, profit curve, leakage audit
- [ ] Hardest: FastAPI + Docker service, drift monitoring, LLM explainer, business case

## Key results so far
- **Mens email** lifted conversion by **+0.68 pp** (95% CI: 0.50 to 0.86), more than doubling the 0.57% baseline.
- **Womens email** lifted conversion by **+0.31 pp** (95% CI: 0.15 to 0.47): real, but close to the experiment's detection limit (MDE 0.20 pp).
- 10.6% of customers visited without any email, so "email everyone" spends budget on people who would have come anyway. This is the problem the uplift models solve.

👉 Full analysis: [`notebooks/01_hillstrom_exploration.ipynb`](notebooks/01_hillstrom_exploration.ipynb)

## Data
See [`data/README.md`](data/README.md).
