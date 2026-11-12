# Numerical methods for CFD

How the equations become something a computer can solve. Write small solvers yourself before using OpenFOAM.

## Lessons

1. [Finite differences and the 1D diffusion equation](01-finite-differences-and-the-1d-diffusion-equation.md)
2. [Convection: upwind, central schemes and the CFL condition](02-convection-upwind-central-schemes-and-the-cfl-condition.md)
3. [The finite volume method](03-the-finite-volume-method.md)
4. [Pressure–velocity coupling (SIMPLE / PISO)](04-pressure-velocity-coupling.md)

## Resources

**Books**

- Versteeg & Malalasekera — *An Introduction to Computational Fluid Dynamics: The Finite Volume Method* (2nd ed.) — The classic FVM book: diffusion, convection schemes, SIMPLE, turbulence.
- Anderson — *Computational Fluid Dynamics: The Basics with Applications* (McGraw-Hill) — Gentlest introduction to CFD; great for equations and finite differences.
- Moukalled, Mangani & Darwish — *The Finite Volume Method in Computational Fluid Dynamics* (Springer) — FVM in depth, with OpenFOAM implementation examples.
- Ferziger, Perić & Street — *Computational Methods for Fluid Dynamics* (4th ed., Springer) — Rigorous reference for numerical methods.
- [Greenshields & Weller — *Notes on CFD: General Principles* (free online)](https://doc.cfd.direct/notes/cfd-general-principles/) — Written by OpenFOAM's developers; explains the methods OpenFOAM uses.

**Videos & courses**

- [Lorena Barba — *CFD Python: 12 steps to Navier–Stokes* (notebooks + video lessons)](https://github.com/barbagroup/CFDPython) — Build a 2D Navier–Stokes solver step by step in Python.
- [Lorena Barba — CFD video lessons on YouTube](https://www.youtube.com/results?search_query=Lorena+Barba+CFD+video+lesson)
- [Fluid Mechanics 101 (Aidan Wimshurst) — YouTube CFD lectures](https://www.youtube.com/results?search_query=Fluid+Mechanics+101+Aidan+Wimshurst) — Excellent short lectures on FVM, SIMPLE, turbulence models, y+ and wall functions.

