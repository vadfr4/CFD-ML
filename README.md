# CFD-ML

A 24-week plan to rebuild my computational fluid dynamics (CFD) skills and combine them with machine learning: from OpenFOAM basics through data-driven surrogates to physics-informed ML and neural operators.

## How this repo is organised

- One folder per week, grouped by phase (`phase-N-.../week-NN/`).
- Each week's `README.md` has three sections: **Notes**, **Saturday build** (the hands-on project for that week) and **Open questions**.
- Large OpenFOAM results and trained models are git-ignored; keep only case setups, scripts and small figures in git.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

OpenFOAM is installed separately (see https://openfoam.org or https://www.openfoam.com).

## Progress

### Phase 1 — CFD foundations

- [ ] [Week 01](phase-1-cfd-foundations/week-01/) — Governing equations: Navier–Stokes, continuity, non-dimensional numbers
- [ ] [Week 02](phase-1-cfd-foundations/week-02/) — Finite volume method basics and discretisation schemes
- [ ] [Week 03](phase-1-cfd-foundations/week-03/) — OpenFOAM setup and the lid-driven cavity tutorial
- [ ] [Week 04](phase-1-cfd-foundations/week-04/) — Meshing with blockMesh and snappyHexMesh
- [ ] [Week 05](phase-1-cfd-foundations/week-05/) — Boundary conditions, solvers (icoFoam, simpleFoam, pimpleFoam)
- [ ] [Week 06](phase-1-cfd-foundations/week-06/) — Turbulence modelling (RANS k-ε, k-ω SST) and post-processing in ParaView

### Phase 2 — ML foundations for scientific data

- [ ] [Week 07](phase-2-ml-foundations/week-07/) — NumPy / pandas refresher and reading OpenFOAM fields into Python
- [ ] [Week 08](phase-2-ml-foundations/week-08/) — Regression and model evaluation with scikit-learn
- [ ] [Week 09](phase-2-ml-foundations/week-09/) — Neural networks in PyTorch: MLPs, training loops, optimisers
- [ ] [Week 10](phase-2-ml-foundations/week-10/) — CNNs for gridded field data
- [ ] [Week 11](phase-2-ml-foundations/week-11/) — Dimensionality reduction: PCA / POD on flow snapshots
- [ ] [Week 12](phase-2-ml-foundations/week-12/) — Building a parametric CFD dataset (automated case sweeps)

### Phase 3 — Data-driven surrogate models

- [ ] [Week 13](phase-3-surrogate-models/week-13/) — MLP surrogate for scalar outputs (drag, lift, pressure drop)
- [ ] [Week 14](phase-3-surrogate-models/week-14/) — U-Net surrogate for full-field prediction
- [ ] [Week 15](phase-3-surrogate-models/week-15/) — POD + neural network reduced-order model
- [ ] [Week 16](phase-3-surrogate-models/week-16/) — Autoencoders and latent-space models
- [ ] [Week 17](phase-3-surrogate-models/week-17/) — Time-series surrogates for unsteady flow (LSTM / sequence models)
- [ ] [Week 18](phase-3-surrogate-models/week-18/) — Uncertainty, generalisation and error analysis vs. CFD

### Phase 4 — Physics-informed and operator learning

- [ ] [Week 19](phase-4-physics-informed-ml/week-19/) — Physics-informed neural networks (PINNs) fundamentals
- [ ] [Week 20](phase-4-physics-informed-ml/week-20/) — PINNs for Navier–Stokes problems
- [ ] [Week 21](phase-4-physics-informed-ml/week-21/) — Neural operators: Fourier Neural Operator (FNO)
- [ ] [Week 22](phase-4-physics-informed-ml/week-22/) — Graph neural networks on unstructured CFD meshes
- [ ] [Week 23](phase-4-physics-informed-ml/week-23/) — ML-augmented turbulence closures
- [ ] [Week 24](phase-4-physics-informed-ml/week-24/) — Capstone project and write-up
