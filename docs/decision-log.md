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
