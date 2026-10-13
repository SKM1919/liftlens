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
