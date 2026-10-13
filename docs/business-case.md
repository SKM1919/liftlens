# Business Case: LiftLens Uplift Targeting

## The problem
Standard targeting pays to show ads to customers who would have converted anyway. In the Criteo experiment, a quarter of users produced **93% of the campaign's extra visits**, while the bottom 40% showed **no detectable effect**. Every rupee spent on those users is wasted.

## The solution
LiftLens predicts each user's **uplift**: how much the ad changes their behaviour. It targets only users whose expected extra profit exceeds the cost of reaching them.

## Evidence (offline, on an untouched holdout)
Per 100,000 users at ₹0.50 per user:

| | Target everyone | LiftLens (top ~24%) | Change |
|---|---|---|---|
| Ad spend | ₹50,000 | ₹12,000 | **−76%** |
| Share of extra visits captured | 100% | ~93% | −7% |
| Profit | ₹5,104 | ₹29,218 | **+₹24,114 (~5.7x)** |
| Incremental CAC | ₹462 | ₹196 | **−58%** |

The result passed a leakage audit: features can't predict treatment (AUC 0.51), and the holdout profit is within 3% of the in-sample estimate.

## What it could be worth
At an assumed **10 million targeted users a year**, the offline gain of ₹24,114 per 100,000 users is about **₹24 lakh in extra annual profit**, alongside roughly **₹38 lakh less ad spend**. These figures must be confirmed by the online test before any budget decision.

## What's built
- Scoring service (FastAPI + Docker) returning an uplift score and target/skip decision per user
- Drift monitoring (PSI + Evidently), plus a business alarm on the share of users targeted
- LLM explainer for marketers, with every number verified against model outputs and a safe template fallback
- A pre-registered 14-day online test (see `online-test-plan.md`)

## Risks and mitigations
| Risk | Mitigation |
|---|---|
| Customers change and the model degrades | Weekly drift monitoring; 10% holdout provides fresh data to retrain |
| Predicted scores run ~30% low | Scores used only to rank users; profit always measured from real outcomes |
| LLM explanations mislead | Numbers verified automatically; known limit on claim-level accuracy; human review for budget decisions |
| Offline results are optimistic | Launch decision made only on the live test result |
| Training data licence | Criteo data is CC BY-NC-SA (non-commercial); a real deployment would retrain on the company's own experiment data |

## The ask
Approve a **14-day live test** on eligible traffic (45% / 45% / 10% split). Launch decision at day 14 based on the pre-registered rules.
