# LiftLens: Uplift-Based Targeting Engine

Most marketing models predict **who will convert**. LiftLens predicts
**who converts because of the ad**, so budget goes only to customers
whose behaviour actually changes.

## Status
🚧 In progress: Hardest tier (scoring service ✅, monitoring, LLM explainer, business case)

## Roadmap
- [x] Easy: Experiment analysis on Hillstrom (ATE, z-tests, CIs, power/MDE)
- [x] Medium: T/S-learner uplift models, Qini/AUUC, targeting policy
- [x] Hard: Criteo Uplift (1.4M rows), T/S/X-learners, budget-constrained profit curve, leakage audit
- [ ] Hardest: FastAPI + Docker service, drift monitoring, LLM explainer, business case

## Key results so far

**Experiment (Easy tier, Hillstrom)**
- **Mens email** lifted conversion by **+0.68 pp** (95% CI: 0.50 to 0.86), more than doubling the 0.57% baseline.
- **Womens email** lifted conversion by **+0.31 pp** (95% CI: 0.15 to 0.47): real, but close to the experiment's detection limit (MDE 0.20 pp).

**Uplift targeting (Medium tier, Hillstrom)**
- The **S-learner** ranked customers better than the T-learner (Qini AUC 0.0097 vs 0.0055).
- **Targeting only paid off for the costly channel**: for direct mail, contacting everyone **loses ~$1,700** per 10,000 customers, while targeting the top 5% turns a small profit.

**Uplift at scale (Hard tier, Criteo)**
- **Strong heterogeneity:** targeting the top 20% of users captures ~75% of all extra visits; the top 30% respond **2.7x** more strongly than average.
- **Budget policy:** at ₹0.50 per user, targeting the top ~24% earns **₹29,200 profit per 100,000 users** on an untouched holdout, vs **₹5,100** for targeting everyone (~5.7x).
- **Incremental CAC roughly halves** with targeting (₹196 vs ₹462 at ₹0.50 per user).
- **Leakage audit passed:** features can't predict treatment (AUC 0.51); excluding `exposure` avoided overstating the effect ~38x; the honest holdout profit is within 3% of the in-sample estimate.

👉 Notebooks: [Experiment analysis](notebooks/01_hillstrom_exploration.ipynb) · [Uplift models](notebooks/02_uplift_models.ipynb) · [Criteo at scale](notebooks/03_criteo_uplift.ipynb)

## Run the scoring service

The trained S-learner is served by a FastAPI app packaged with Docker.

```bash
docker build -t liftlens-api .
docker run -d -p 8000:8000 --name liftlens liftlens-api

# Check it's alive
curl http://localhost:8000/health

# Score two example users
curl -X POST http://localhost:8000/score \
  -H "Content-Type: application/json" \
  -d @examples/sample_request.json
```

Each user gets an `uplift_score` and a `target` / `skip` decision (targets the top 24%, the profit-maximising share from the holdout analysis). Interactive API docs are available at `http://localhost:8000/docs`.

## Data
See [`data/README.md`](data/README.md).