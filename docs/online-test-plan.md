# Online Test Plan: LiftLens Targeting Policy

## Hypothesis
Targeting only users the LiftLens model scores above the cutoff (~top 24%) earns more profit per user than targeting everyone, while keeping most of the campaign's extra visits.

## Design
Users are randomly assigned (by hashed user ID, so each user stays in one arm) to:

| Arm | Share | Treatment |
|---|---|---|
| A: LiftLens policy | 45% | Ads only for users with uplift score ≥ cutoff |
| B: Target everyone | 45% | Ads for all users (current practice) |
| C: No-ad holdout | 10% | No ads; measures baseline and provides fresh randomised data for retraining |

## Metrics (fixed before launch)
- **Primary:** profit per user = visits × ₹55.74 − ad spend. Compare Arm A vs Arm B.
- **Guardrails:**
  - Visit rate in Arm A no more than 0.15 pp below Arm B
  - No PSI drift alert (> 0.25) on incoming features
  - Scoring service error rate below 0.1%; no timeouts affecting ad delivery

## Sample size and duration
- Expected gain: ₹0.24 per user (offline holdout estimate).
- ~39,000 users per arm detects the full gain; ~155,000 detects half of it (95% confidence, 80% power).
- **Duration: 14 days** (two full weekly cycles), giving ~1.26M users per arm at an assumed 200,000 eligible users/day. Detects profit differences of ~₹0.04 per user and visit-rate differences of ~0.08 pp.

## Interim looks (O'Brien–Fleming, two looks)
- **Day 7:** stop early for a clear win only if |z| > 2.797 (p < 0.005). Stop immediately for harm if any guardrail fails.
- **Day 14:** final decision if |z| > 1.977 (p < 0.048).

## Decision rules
- **Launch** if Arm A beats Arm B on profit per user at the planned threshold and all guardrails hold.
- **Iterate** if profit improves but a guardrail fails (e.g. too many visits lost): adjust the cutoff and re-test.
- **Stop** if Arm A is not better on profit, or any guardrail shows harm.

## After the test
Arms B and C form a fresh randomised experiment. Use them to re-check the model's ranking (Qini) on live users and to retrain the model on current customers.
