# Models

| File | What it is |
|------|------------|
| `liftlens_s_learner.json` | Trained S-learner (XGBoost) that predicts visit uplift from features f0–f11 plus a treatment flag |
| `model_config.json` | Feature list, targeting cutoff (top 24%), cost/value assumptions, and the XGBoost version needed to load the model |

**Training data:** a seeded 10% sample of the Criteo Uplift Dataset v2.1 (Criteo AI Lab, CC BY-NC-SA 4.0). See `notebooks/03_criteo_uplift.ipynb`.

**Important:** predicted uplift under-estimates the true average effect by ~30%. Use scores to rank users, not as exact effect sizes.
