# Data

Raw data is not stored in this repo. It is downloaded in code.

- **Hillstrom Email Dataset** (64,000 customers, randomised email trial).
  Source: Kevin Hillstrom, MineThatData (2008). No stated licence, so it is linked rather than redistributed.
  Loaded via `sklift.datasets.fetch_hillstrom()`.

- **Criteo Uplift Dataset v2.1** (~14M users, randomised display-ad incrementality test).
  Source: Criteo AI Lab, via the official [Hugging Face repo](https://huggingface.co/datasets/criteo/criteo-uplift).
  Licence: CC BY-NC-SA 4.0 (non-commercial, attribution required).
  Citation: Diemert, Betlei, Renaudin & Amini, *A Large Scale Benchmark for Uplift Modeling*, AdKDD 2018.
  This project uses a seeded 10% random sample (~1.4M rows), drawn in chunks during loading.
