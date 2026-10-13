# Decision Log

| Date | Decision | Why |
|------|----------|-----|
| 2026-10-05 | Don't commit raw data; download in code | Hillstrom has no stated licence |
| 2026-10-05 | Start with Hillstrom before Criteo | Small, clean, randomised: learn the method first |
| 2026-10-05 | Use 95% confidence (alpha 0.05) and 80% power | Industry-standard thresholds; keeps results comparable |
| 2026-10-05 | Check results with Bonferroni correction | 4 tests run at once; all still significant at 0.0125 |
| 2026-10-06 | Model Mens E-Mail vs No E-Mail only | Uplift models need one treatment vs control; Mens had the strongest effect |
| 2026-10-06 | Use visit (not conversion) as the model target | Only ~0.9% convert, too few events to learn individual effects reliably (see MDE analysis) |
| 2026-10-06 | Choose S-learner over T-learner | ~1.8x higher Qini AUC; T-learner badly misranked its lowest decile |
| 2026-10-06 | Treat decile-level differences under ~4 pp as noise | ~640 customers per arm per decile gives about ±4 pp margin of error |
| 2026-10-06 | Value a visit at $3.02 profit | Derived from experiment ($10.05 extra revenue per extra visit) × assumed 30% margin |
| 2026-10-06 | Compare three channel costs ($0.05 / $0.20 / $0.40) | Shows when targeting pays: only the costly channel benefits |
| 2026-10-06 | Recommend direct-mail targeting as a pilot only | Top-5% segment is ~640 test customers, so the profit estimate is noisy |
| 2026-10-13 | Load Criteo from Criteo's official Hugging Face repo | scikit-uplift's built-in download link returns 404 |
| 2026-10-13 | Use a seeded 10% sample (~1.4M rows), read in chunks | Keeps memory low in free Colab while staying 33x larger than Hillstrom |
| 2026-10-13 | Use visit as the Criteo model target | Control group has only 387 conversions vs ~8,100 visits |
| 2026-10-13 | Exclude `exposure` from features and analysis | Post-assignment and behaviour-driven: would leak information and break randomisation |
| 2026-10-13 | Don't reweight rare outcomes | Reweighting distorts probabilities, and uplift is a difference of probabilities |
| 2026-10-13 | Draw Qini curves with our own code | sklift's plotting module is incompatible with current scikit-learn |
| 2026-10-13 | Choose S-learner on Criteo | Highest Qini AUC (0.081 vs 0.071 X-learner, 0.067 T-learner) |
| 2026-10-13 | Compute profit from real test-set outcomes, not predicted uplift | All models under-predict the average effect by ~30% |
| 2026-10-13 | Value an extra Criteo visit at ₹55.74 | 0.124 extra conversions per extra visit × assumed ₹1,500 AOV × 30% margin |
| 2026-10-13 | Report incremental CAC (iCAC), not CAC | Counts only conversions the ad caused; plain CAC flatters campaigns by counting sure things |
| 2026-10-13 | Recommend top 20–40% at ₹0.50 per user | Profit peaks at 40%; beyond that every extra rupee loses money |
| 2026-10-13 | Features pass the randomisation check | AUC 0.510 when predicting treatment from features |
| 2026-10-13 | Choose target % on a validation half; report profit on an untouched holdout | Removes in-sample optimism: honest ₹29,218 vs ₹30,097 in-sample |
| 2026-10-13 | Keep S-learner; note X-learner as close second | S beats T in 96% and X in 90% of 50 bootstrap resamples |
| 2026-10-13 | Serve the model with FastAPI inside Docker, on Python 3.13 | Matches Colab's training environment exactly; the Codespace runs Python 3.14 |
| 2026-10-13 | Pin xgboost==3.4.1 and include scikit-learn | Same version that saved the model; XGBClassifier needs scikit-learn |
| 2026-10-13 | Turn the "top 24%" policy into a score cutoff (0.00316) | A live service scores users one at a time; cutoff computed on the validation half |
| 2026-10-13 | Return the calibration note with every response | Scores run ~30% low, so consumers must not treat them as exact effect sizes |
| 2026-10-13 | Monitor drift with two methods: our own PSI plus Evidently | PSI gives transparent alarm thresholds; Evidently's Wasserstein test is more sensitive and covers PSI's blind spot |
| 2026-10-13 | Track prediction drift (share above cutoff) as the business alarm | Shows budget impact directly: Week B would cut targeting from ~24% to 15% |
| 2026-10-13 | Known gap: our PSI returns 0 for features dominated by one value | Affects f1, f4, f5, f7, f10, f11; fix by giving the dominant value its own bucket |
| 2026-10-14 | Python computes every number; the LLM writes only the words; a verifier checks every number | Stops invented figures reaching marketers |
| 2026-10-14 | Calculate recommendations from economics, never by hand | A hand-typed recommendation for Moderate responders was wrong (₹0.09 profit vs ₹0.50 cost) |
| 2026-10-14 | Verifier checks fact values only, with an explicit allow-list (95, 100) | Fact labels like "per_100" were silently approving numbers |
| 2026-10-14 | Retry server errors with backoff, fail over across Gemini models, fall back to a template | 2.5-flash retired for new users; flash-latest overloaded; the template guarantees an answer |
| 2026-10-14 | Store the Gemini API key in Colab Secrets, never in code | Notebooks are public on GitHub |
| 2026-10-14 | Known limit: the verifier checks numbers, not the claims they're attached to | "93% of users" would pass; mitigate with template slots, a claim check, or human review |
| 2026-10-14 | Validate with a live three-arm test: policy / everyone / 10% no-ad holdout | Offline results can be optimistic; the holdout also keeps randomised data for retraining |
| 2026-10-14 | Primary metric: profit per user; guardrails on visits, drift and service health | Matches the business goal; guardrails stop "profitable but harmful" launches |
| 2026-10-14 | Run 14 days even though ~1 day gives enough power | Covers two weekly cycles and gives power for the visit guardrail |
| 2026-10-14 | Two planned looks with O'Brien–Fleming thresholds | Allows a safe early stop without inflating false positives |
| 2026-10-14 | Present annual value as an estimate pending the live test | Offline gains must be confirmed before any budget decision |
