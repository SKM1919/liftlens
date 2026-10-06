# LiftLens: Uplift-Based Targeting Engine

Most marketing models predict **who will convert**. LiftLens predicts
**who converts because of the ad**, so budget goes only to customers
whose behaviour actually changes.

## Status
In progress: Hard tier (Criteo, advanced causal models)

## Roadmap
- [x] Easy: Experiment analysis on Hillstrom (ATE, z-tests, CIs, power/MDE)
- [x] Medium: T/S-learner uplift models, Qini/AUUC, targeting policy
- [ ] Hard: Criteo Uplift, X-learner/causal forest, profit curve, leakage audit
- [ ] Hardest: FastAPI + Docker service, drift monitoring, LLM explainer, business case

## Key results so far

**Experiment (Easy tier)**
- **Mens email** lifted conversion by **+0.68 pp** (95% CI: 0.50 to 0.86), more than doubling the 0.57% baseline.
- **Womens email** lifted conversion by **+0.31 pp** (95% CI: 0.15 to 0.47): real, but close to the experiment's detection limit (MDE 0.20 pp).

**Uplift models and targeting (Medium tier)**
- The **S-learner** ranked customers better than the T-learner (Qini AUC 0.0097 vs 0.0055).
- **Targeting only pays off when contact is costly.** For email ($0.05), contacting everyone is optimal (~$1,800 profit per 10,000 customers). For direct mail ($0.40), contacting everyone **loses ~$1,700** per 10,000, while targeting the model's top 5% turns that into a small profit.

Notebooks: [Experiment analysis](notebooks/01_hillstrom_exploration.ipynb) · [Uplift models](notebooks/02_uplift_models.ipynb)

## Data
See [`data/README.md`](data/README.md).
