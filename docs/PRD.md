# LiftLens PRD: Uplift-Based Ad Targeting

Oct 14, 2026 · @LJMU

## Overview

LiftLens shows ads only to users the ad will actually change, cutting spend by 76% while keeping about 93% of the campaign's extra visits (offline holdout, Criteo data). It replaces "target everyone" with a causal model that predicts each user's uplift: how much the ad raises their chance of visiting.

**Status:** draft. Offline validation is complete; the live test in the Launch plan is designed but not yet run. This is a portfolio PRD built on public datasets (Hillstrom, Criteo Uplift v2.1), so all money figures rest on stated assumptions.

**How to read it:** Problem, Goals and Success metrics say why and what "good" means. Solution and Requirements say what gets built. Evidence, Launch plan and Risks say why we believe it will work and how we will prove it.

## Problem

Most ad budget is spent on users the ad does not change. In a randomised Criteo experiment, the top 24% of users produced 93% of the campaign's extra visits, while the bottom 40% showed no detectable effect.

**Who has it:** performance marketing teams that target users by "likely to convert" scores. Those scores find people who would buy anyway (sure things), so the team pays for conversions it would have got for free.

**Why it matters:**

- **Wasted spend:** at ₹0.50 per user, targeting everyone earns ₹5,104 profit per 100,000 users. Targeting the right quarter earns ₹29,218.
- **Misleading metrics:** plain CAC counts sure things as wins. Incremental CAC, which counts only conversions the ad caused, is ₹462 when targeting everyone.
- **Costly channels lose money outright:** at ₹1.00 per user, targeting everyone loses ₹44,892 per 100,000 users.

**Why now:** randomised holdout data, which uplift models need, is increasingly standard in ad platforms, and open-source causal ML tools make the model cheap to build. The remaining gap is product: turning a model into decisions marketers trust.

## Goals and non-goals

The goal is more profit per ad rupee, proven live, without losing the campaign's reach where it counts.

**Goals**

1. Raise profit per user above "target everyone", confirmed by a pre-registered live test.
2. Cut wasted spend by targeting only users whose expected extra profit exceeds the cost of reaching them.
3. Keep at least 90% of the campaign's extra visits.
4. Give marketers plain-English explanations of each segment, with every number verified.
5. Detect drift before it degrades targeting decisions.

**Non-goals (this release)**

- Predicting conversions directly. The data has too few conversions in the control group (387) to learn individual effects reliably, so the model predicts visits.
- Choosing creative, bids or channels. LiftLens decides who to target, not what to show.
- Real-time retraining. The model is retrained from holdout data on a schedule.
- Explaining individual users. Features are anonymised, so explanations work at segment level.

## Users

The primary user is the performance marketer who decides who a campaign targets; three other roles must trust or maintain the decision. These personas are assumptions to validate in user interviews.

| Persona | Job to be done | What they need from LiftLens |
| --- | --- | --- |
| Performance marketer (primary) | Decide who each campaign targets within budget | A target/skip decision per user, and how much budget it saves |
| Marketing manager | Explain campaign results to leadership | Plain-English segment explanations with numbers they can repeat safely |
| CFO / finance | Approve budget changes | Profit per user and incremental CAC, proven by a live test |
| Data scientist | Keep the model accurate over time | Drift alerts, logged scores and fresh randomised data for retraining |

## Success metrics

Launch is decided by one metric, profit per user, with guardrails that block a launch that is profitable but harmful. Baselines are "target everyone" on the offline holdout, at ₹0.50 per user.

| Metric | Type | Baseline (target everyone) | Target | Offline result |
| --- | --- | --- | --- | --- |
| Profit per user (₹) | Primary | 0.05 | Significantly above baseline in the live test | 0.29 |
| Ad spend per user (₹) | Secondary | 0.50 | ≤ 0.15 | 0.12 |
| Incremental CAC (₹) | Secondary | 462 | ≤ 250 | 196 |
| Share of extra visits kept | Secondary | 100% | ≥ 90% | \~93% |
| Visit rate vs baseline arm | Guardrail | — | No more than 0.15 pp lower | not yet measured live |
| Feature drift (PSI) | Guardrail | — | No feature above 0.25 | — |
| Scoring service error rate | Guardrail | — | Below 0.1% | not yet measured |
| Explainer numbers verified | Guardrail | — | 100% of shown explanations | 100% in tests |

Profit per user = visits × ₹55.74 − ad spend. ₹55.74 is the value of one extra visit: 0.124 extra conversions per extra visit × an assumed ₹1,500 order value × an assumed 30% margin.

## Solution

A scoring service ranks each user by predicted uplift; only users above a profit-based cutoff are shown the ad. Three supporting parts keep the decisions trustworthy over time.

&#91;embedded content: LiftLens decision flow and learning loop\]

The top row is the decision made for every user; the shaded row is what keeps it honest: drift alerts, verified explanations, and a holdout that supplies fresh data to retrain.

**Marketer journey**

1. Set the campaign's cost per user and budget; LiftLens turns them into a cutoff.
2. Launch: the ad platform asks LiftLens about each user and serves ads only to those above the cutoff.
3. Read the segment explanations to see who is being targeted and why it pays.
4. Get alerted if incoming users drift, before targeting quality drops.

## Requirements

P0 items are needed for the live test; P1 items are needed before full rollout; P2 items follow later.

**Functional**

| ID | Requirement | Priority | Acceptance criteria |
| --- | --- | --- | --- |
| FR1 | Score a batch of users and return an uplift score plus a target/skip decision for each | P0 | Scores match the training notebook for the same inputs; invalid input is rejected with a clear error |
| FR2 | Health endpoint reporting model name, cutoff and library version | P0 | Returns status "ok" when the model is loaded |
| FR3 | Policy settings (cutoff, cost per user, value per visit) live in a config file, not in code | P0 | Changing the cutoff needs no retraining or code change |
| FR4 | Assign every user to an arm (policy, everyone, holdout) by hashed user ID | P0 | The same user always lands in the same arm; arm shares within 1 point of 45/45/10 |
| FR5 | Weekly drift check on all features (PSI and Evidently) | P0 | Alert when any feature's PSI exceeds 0.25; report saved for review |
| FR6 | Alert when the share of users above the cutoff moves outside 20–28% | P1 | Alert fires on the simulated new-traffic batch (15.4% targeted) |
| FR7 | Segment explainer: Python computes every number, the LLM writes the words, a verifier checks every number | P1 | No unverified number is ever shown; on failure, a template explanation is shown instead |
| FR8 | Log each score, decision, model version and explainer model name | P1 | Any decision can be traced to the model that made it |
| FR9 | Retrain from holdout and everyone-arm data on a schedule | P2 | New model beats the current one on Qini AUC on fresh data before it replaces it |

**Non-functional**

- **Reproducibility:** the service runs in Docker on Python 3.13 with XGBoost pinned to 3.4.1, matching training.
- **Security:** API keys live in a secrets store, never in code or notebooks.
- **Privacy:** no personal data in logs; features are already anonymised.
- **Resilience:** the explainer retries server errors with backoff and fails over across models; the template guarantees an answer.
- **Latency:** target to be set with the ad platform team before the live test (not yet measured).

## Evidence

Offline, targeting the top 24% earned 5.7x the profit of targeting everyone, and the result held on an untouched holdout and a leakage audit. Figures are per 100,000 users at ₹0.50 per user unless stated.

| Finding | Result | Why it matters |
| --- | --- | --- |
| Effect is concentrated | Top 24% of users produce 93% of extra visits; bottom 40% show no detectable effect | Most spend on the bottom 76% is wasted |
| Profit on untouched holdout | ₹29,218 vs ₹5,104 for targeting everyone | The core business case |
| Holdout vs in-sample profit | Within 3% (₹29,218 vs ₹30,097) | The result is not an artefact of choosing settings on test data |
| Model ranking quality | S-learner Qini AUC 0.081; beats T-learner in 96% and X-learner in 90% of 50 bootstrap resamples | Model choice is robust, not lucky |
| Overfitting check | Test Qini AUC is 89% of training | The model generalises |
| Randomisation check | Features predict treatment with AUC 0.51 (chance) | Features were recorded before treatment; no leakage |
| Leaky feature excluded | Using ad exposure would have overstated the effect \~38x | A known trap avoided |

**Earlier validation on Hillstrom (email):** targeting only paid off for the costly channel. For email at $0.05 per send, emailing everyone was optimal. This shows LiftLens adds most value where contact is costly or effects vary widely, which sets realistic expectations for each channel.

**Known limit:** the model's scores under-estimate the average effect by about 30%. Scores are used only to rank users; profit is always measured from real outcomes.

## Launch plan

No budget moves until a pre-registered 14-day live test shows higher profit per user with all guardrails holding.

&#91;embedded content: Launch phases and gates\]

Shadow mode proves the service works without risk; the live test proves the policy pays; rollout keeps a permanent holdout so the model never loses its baseline.

**Test sizing:** about 39,000 users per arm detects the full expected gain of ₹0.24 per user, and about 155,000 detects half of it (95% confidence, 80% power). Fourteen days at an assumed 200,000 eligible users a day gives about 1.26 million users per arm. That detects profit differences of about ₹0.04 per user and covers two weekly cycles.

**Decision rules at day 14**

- **Launch:** policy arm beats target-everyone on profit per user (z above 1.977) and all guardrails hold.
- **Stop early at day 7** only for a clear win (z above 2.797) or any guardrail showing harm.
- **Iterate:** profit improves but a guardrail fails, for example too many visits lost: adjust the cutoff and re-test.
- **Stop:** the policy arm is not better on profit.

Full detail: [online test plan](https://github.com/SKM1919/liftlens/blob/main/docs/online-test-plan.md).

## Risks and assumptions

The biggest risk is that offline gains don't hold live; the live test exists to catch that before any budget moves.

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Offline gains don't hold live | Medium | High | Launch only on the pre-registered live test result |
| Users drift and the model degrades | Medium | High | Weekly drift checks; prediction-drift alarm; retrain from holdout data |
| Drift is detected but we can't tell if the model is still right | Medium | Medium | The 10% holdout gives real outcomes to re-check ranking on new users |
| Scores read as exact effect sizes | Medium | Medium | Calibration warning returned with every score; profit measured from outcomes |
| LLM explanation attaches a real number to the wrong claim | Low | High | Verifier checks every number; next step is template slots; human review for budget decisions |
| Gemini model retired or overloaded | High | Low | Model failover, retries, template fallback |
| Training data is non-commercial (CC BY-NC-SA) | Certain | High for real use | A real deployment retrains on the company's own experiment data |

**Key assumptions (to confirm with finance and the ad platform team)**

- Average order value ₹1,500 and gross margin 30%, giving ₹55.74 per extra visit.
- Cost per targeted user ₹0.50.
- 200,000 eligible users per day for the live test; 10 million targeted users per year for annual value.

## Dependencies, open questions and roadmap

The live test depends on the ad platform calling the scoring service and honouring its decisions per arm.

**Dependencies**

- Ad platform team: call `/score` before serving, and respect target/skip per arm.
- Data engineering: daily feed of user features and visit outcomes, with arm labels.
- Finance: sign-off on order value, margin and cost assumptions.

**Open questions**

- [ ] What latency budget does the ad platform allow per scoring call?
- [ ] Should the 10% holdout be permanent, or shrink after launch?
- [ ] Who owns acting on drift alerts: marketing, data science or both?
- [ ] Do marketers want explanations in the ad tool, or a weekly summary?

**Roadmap (after launch)**

1. Put the explainer behind the API, with the key held as a deployment secret.
2. Template slots in explanations, so numbers can't attach to the wrong claim.
3. Fix the PSI blind spot for features dominated by one value.
4. Model conversions as well as visits once enough control-group conversions exist.
5. Move shared data-loading code into `src/` and add automated tests.

## Appendix

**Glossary**

| Term | Meaning |
| --- | --- |
| Uplift | How much the ad changes a user's chance of visiting: chance with ad minus chance without |
| Persuadables / sure things | Users who visit only because of the ad / users who would visit anyway |
| Incremental CAC | Ad spend divided by conversions the ad actually caused |
| Qini AUC | How well a model ranks users by uplift; zero means no better than random |
| PSI | Population Stability Index: how much a feature's distribution has shifted from training |
| Holdout | Users kept out of ads at random, to measure the true baseline |
| O'Brien–Fleming | A plan for checking a test early without inflating false positives |

**Links (repo)**

- [Business case](https://github.com/SKM1919/liftlens/blob/main/docs/business-case.md) · [Online test plan](https://github.com/SKM1919/liftlens/blob/main/docs/online-test-plan.md) · [Decision log](https://github.com/SKM1919/liftlens/blob/main/docs/decision-log.md)
- Notebooks: [Experiment analysis](https://github.com/SKM1919/liftlens/blob/main/notebooks/01_hillstrom_exploration.ipynb) · [Uplift models](https://github.com/SKM1919/liftlens/blob/main/notebooks/02_uplift_models.ipynb) · [Criteo at scale](https://github.com/SKM1919/liftlens/blob/main/notebooks/03_criteo_uplift.ipynb) · [Drift monitoring](https://github.com/SKM1919/liftlens/blob/main/notebooks/04_drift_monitoring.ipynb) · [LLM explainer](https://github.com/SKM1919/liftlens/blob/main/notebooks/05_llm_explainer.ipynb)
- Data: [Criteo Uplift dataset](https://huggingface.co/datasets/criteo/criteo-uplift) (CC BY-NC-SA 4.0); Hillstrom email dataset (MineThatData, 2008).
