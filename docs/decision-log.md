# Decision Log

| Date | Decision | Why |
|------|----------|-----|
| 2026-10-05 | Don't commit raw data; download in code | Hillstrom has no stated licence |
| 2026-10-05 | Start with Hillstrom before Criteo | Small, clean, randomised: learn the method first |
| 2026-10-05 | Use 95% confidence (alpha 0.05) and 80% power | Industry-standard thresholds; keeps results comparable |
| 2026-10-05 | Check results with Bonferroni correction | 4 tests run at once; all still significant at 0.0125 |
| 2026-10-06 | Model Mens E-Mail vs No E-Mail only | Uplift models need one treatment vs control; Mens had the strongest effect |
| 2026-10-06 | Use visit (not conversion) as the model target | Only ~0.9% convert, too few events to learn individual effects reliably (see MDE analysis) |
