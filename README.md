# LiftLens: Uplift-Based Targeting Engine

Most marketing models predict **who will convert**. LiftLens predicts
**who converts because of the ad**, so budget goes only to customers
whose behaviour actually changes.

## Headline result
On an untouched holdout of real advertising data, targeting the users LiftLens ranks highest cut ad spend by **76%**, kept **~93% of the campaign's extra visits**, and raised profit **~5.7x** compared with targeting everyone.

[Business case](docs/business-case.md) · [Online test plan](docs/online-test-plan.md) · [Decision log](docs/decision-log.md)

## Status
All four tiers complete. The live test is designed and pre-registered, not yet run.

## Roadmap
- [x] Easy: Experiment analysis on Hillstrom (ATE, z-tests, CIs, power/MDE)
- [x] Medium: T/S-learner uplift models, Qini/AUUC, targeting policy
- [x] Hard: Criteo Uplift (1.4M rows), T/S/X-learners, budget-constrained profit curve, leakage audit
- [x] Hardest: FastAPI + Docker service, drift monitoring, LLM explainer, online test design, business case

## Key results

**Experiment (Easy tier, Hillstrom)**
- **Mens email** lifted conversion by **+0.68 pp** (95% CI: 0.50 to 0.86), more than doubling the 0.57% baseline.
- **Womens email** lifted conversion by **+0.31 pp** (95% CI: 0.15 to 0.47): real, but close to the experiment's detection limit (MDE 0.20 pp).

**Uplift targeting (Medium tier, Hillstrom)**
- The **S-learner** ranked customers better than the T-learner (Qini AUC 0.0097 vs 0.0055).
- **Targeting only paid off for the costly channel**: for direct mail, contacting everyone **loses ~$1,700** per 10,000 customers, while targeting the top 5% turns a small profit.

**Uplift at scale (Hard tier, Criteo)**
- **Strong heterogeneity:** the top 24% of users produce **93% of all extra visits**; the bottom 40% show no detectable effect.
- **Budget policy:** at ₹0.50 per user, targeting the top ~24% earns **₹29,200 profit per 100,000 users** on an untouched holdout, vs **₹5,100** for targeting everyone.
- **Incremental CAC drops 58%** with targeting (₹196 vs ₹462).
- **Leakage audit passed:** features can't predict treatment (AUC 0.51); excluding `exposure` avoided overstating the effect ~38x; the honest holdout profit is within 3% of the in-sample estimate.

**Production (Hardest tier)**
- **Scoring service:** FastAPI + Docker, returning an uplift score and target/skip decision per user, with input validation and a calibration warning on every response.
- **Drift monitoring:** PSI plus Evidently correctly stayed quiet on a healthy batch and alerted on a simulated new traffic source; a business alarm tracks the share of users targeted.
- **LLM explainer:** Python computes every number, Gemini writes the words, and a verifier rejects any number not in the facts, with model failover and a safe template fallback.
- **Online test:** a pre-registered 14-day, three-arm test (policy / everyone / 10% holdout) with sequential looks.

Notebooks: [Experiment analysis](notebooks/01_hillstrom_exploration.ipynb) · [Uplift models](notebooks/02_uplift_models.ipynb) · [Criteo at scale](notebooks/03_criteo_uplift.ipynb) · [Drift monitoring](notebooks/04_drift_monitoring.ipynb) · [LLM explainer](notebooks/05_llm_explainer.ipynb) · [Online test and business case](notebooks/06_online_test_and_business_case.ipynb)

## Run the scoring service

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

Each user gets an `uplift_score` and a `target` / `skip` decision (targets the top 24%, the profit-maximising share from the holdout analysis). Interactive API docs are at `http://localhost:8000/docs`.

## Data
See [`data/README.md`](data/README.md).
