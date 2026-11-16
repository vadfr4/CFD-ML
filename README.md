# CFD-ML

**Website:** https://vadfr4.github.io/CFD-ML/ (built from these files by `site/build.py` on every push to `main`)

A study plan to rebuild my computational fluid dynamics (CFD) skills and combine them with machine learning: from the physics and OpenFOAM through data-driven surrogates to physics-informed ML and neural operators.

## How this repo is organised

- The plan is split into **subjects** (numbered folders, in a sensible order).
- Each subject has **lessons**, each sized for **one ~2-hour study session** (≈30 min theory, ≈75 min hands-on, ≈15 min notes). Bigger topics are split into parts.
- Every lesson file has a session plan, a topic checklist, a hands-on build, and space for **Notes** and **Open questions**.
- Put code for a lesson next to it (e.g. a notebook with the same number). Large OpenFOAM results and trained models are git-ignored.

43 lessons in total (~86 hours). Each lesson links its best books, videos and papers; the full list is in [RESOURCES.md](RESOURCES.md).

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

OpenFOAM is installed separately (see https://openfoam.org or https://www.openfoam.com).

## Progress

### [Fluid dynamics fundamentals](01-fluid-dynamics-fundamentals/)

- [ ] [Conservation laws and the Navier–Stokes equations](01-fluid-dynamics-fundamentals/01-conservation-laws-and-the-navier-stokes-equations.md)
- [ ] [Non-dimensional numbers and flow regimes](01-fluid-dynamics-fundamentals/02-non-dimensional-numbers-and-flow-regimes.md)
- [ ] [Analytical solutions: Couette, Poiseuille and boundary layers](01-fluid-dynamics-fundamentals/03-analytical-solutions-couette-poiseuille-and-boundary-layers.md)

### [Numerical methods for CFD](02-numerical-methods/)

- [ ] [Finite differences and the 1D diffusion equation](02-numerical-methods/01-finite-differences-and-the-1d-diffusion-equation.md)
- [ ] [Convection: upwind, central schemes and the CFL condition](02-numerical-methods/02-convection-upwind-central-schemes-and-the-cfl-condition.md)
- [ ] [The finite volume method](02-numerical-methods/03-the-finite-volume-method.md)
- [ ] [Pressure–velocity coupling (SIMPLE / PISO)](02-numerical-methods/04-pressure-velocity-coupling.md)

### [OpenFOAM in practice](03-openfoam/)

- [ ] [Installation and case structure](03-openfoam/01-installation-and-case-structure.md)
- [ ] [Post-processing with ParaView and Python](03-openfoam/02-post-processing-with-paraview-and-python.md)
- [ ] [Meshing with blockMesh](03-openfoam/03-meshing-with-blockmesh.md)
- [ ] [Meshing with snappyHexMesh](03-openfoam/04-meshing-with-snappyhexmesh.md)
- [ ] [Boundary conditions and solver choice](03-openfoam/05-boundary-conditions-and-solver-choice.md)
- [ ] [Automating case sweeps](03-openfoam/06-automating-case-sweeps.md)

### [Turbulence modelling](04-turbulence-modelling/)

- [ ] [Turbulence basics and Reynolds averaging](04-turbulence-modelling/01-turbulence-basics-and-reynolds-averaging.md)
- [ ] [RANS models: k-ε and k-ω SST](04-turbulence-modelling/02-rans-models-k-ε-and-k-ω-sst.md)
- [ ] [Wall treatment, y+ and validation](04-turbulence-modelling/03-wall-treatment-y-and-validation.md)

### [Python for scientific data](05-python-for-scientific-data/)

- [ ] [NumPy and pandas refresher for field data](05-python-for-scientific-data/01-numpy-and-pandas-refresher-for-field-data.md)
- [ ] [Building a CFD dataset](05-python-for-scientific-data/02-building-a-cfd-dataset.md)

### [Machine learning fundamentals](06-machine-learning-fundamentals/)

- [ ] [Regression, loss functions and overfitting](06-machine-learning-fundamentals/01-regression-loss-functions-and-overfitting.md)
- [ ] [Model evaluation and Gaussian processes](06-machine-learning-fundamentals/02-model-evaluation-and-gaussian-processes.md)

### [Deep learning with PyTorch](07-deep-learning-with-pytorch/)

- [ ] [Tensors, autograd and the training loop](07-deep-learning-with-pytorch/01-tensors-autograd-and-the-training-loop.md)
- [ ] [MLPs: architecture and training tricks](07-deep-learning-with-pytorch/02-mlps-architecture-and-training-tricks.md)
- [ ] [CNNs for gridded field data](07-deep-learning-with-pytorch/03-cnns-for-gridded-field-data.md)

### [Reduced-order modelling](08-reduced-order-modelling/)

- [ ] [POD / PCA on flow snapshots](08-reduced-order-modelling/01-pod-pca-on-flow-snapshots.md)
- [ ] [Dynamic mode decomposition (DMD)](08-reduced-order-modelling/02-dynamic-mode-decomposition.md)
- [ ] [Autoencoders as nonlinear POD](08-reduced-order-modelling/03-autoencoders-as-nonlinear-pod.md)

### [Data-driven surrogate models](09-surrogate-models/)

- [ ] [Scalar-output surrogates](09-surrogate-models/01-scalar-output-surrogates.md)
- [ ] [Full-field prediction with U-Net (part 1: model)](09-surrogate-models/02-full-field-prediction-with-u-net.md)
- [ ] [Full-field prediction with U-Net (part 2: evaluation)](09-surrogate-models/03-full-field-prediction-with-u-net.md)
- [ ] [POD + neural network reduced-order model](09-surrogate-models/04-pod-neural-network-reduced-order-model.md)
- [ ] [Time-series surrogates for unsteady flow](09-surrogate-models/05-time-series-surrogates-for-unsteady-flow.md)

### [Physics-informed neural networks (PINNs)](10-physics-informed-neural-networks/)

- [ ] [PINN fundamentals](10-physics-informed-neural-networks/01-pinn-fundamentals.md)
- [ ] [PINNs for Navier–Stokes](10-physics-informed-neural-networks/02-pinns-for-navier-stokes.md)
- [ ] [Inverse problems and data assimilation](10-physics-informed-neural-networks/03-inverse-problems-and-data-assimilation.md)

### [Neural operators](11-neural-operators/)

- [ ] [Operator learning and DeepONet](11-neural-operators/01-operator-learning-and-deeponet.md)
- [ ] [Fourier Neural Operator (FNO)](11-neural-operators/02-fourier-neural-operator.md)

### [Graph neural networks on meshes](12-graph-neural-networks/)

- [ ] [Graphs from meshes and message passing](12-graph-neural-networks/01-graphs-from-meshes-and-message-passing.md)
- [ ] [MeshGraphNets-style models for unsteady flow](12-graph-neural-networks/02-meshgraphnets-style-models-for-unsteady-flow.md)

### [ML for turbulence modelling](13-ml-for-turbulence-modelling/)

- [ ] [Data-driven turbulence closures](13-ml-for-turbulence-modelling/01-data-driven-turbulence-closures.md)
- [ ] [Coupling an ML model into OpenFOAM](13-ml-for-turbulence-modelling/02-coupling-an-ml-model-into-openfoam.md)

### [Capstone project](14-capstone/)

- [ ] [Project scoping](14-capstone/01-project-scoping.md)
- [ ] [Build sessions (repeat as needed)](14-capstone/02-build-sessions.md)
- [ ] [Write-up](14-capstone/03-write-up.md)
