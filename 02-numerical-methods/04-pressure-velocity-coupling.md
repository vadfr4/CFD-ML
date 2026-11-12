# Pressure–velocity coupling (SIMPLE / PISO)

**Subject:** Numerical methods for CFD · **Time:** ~2 h session

**Goal:** Understand how incompressible solvers handle pressure.

## Session plan

| Block | Time | What |
|---|---|---|
| Theory | ~30 min | Why pressure has no own equation in incompressible flow |
| Hands-on | ~75 min | SIMPLE algorithm step by step; PISO and PIMPLE — what OpenFOAM's solvers use |
| Wrap-up | ~15 min | Write notes and open questions below; commit |

## Topics

- [ ] Why pressure has no own equation in incompressible flow
- [ ] SIMPLE algorithm step by step
- [ ] PISO and PIMPLE — what OpenFOAM's solvers use

## Build

Flowchart of SIMPLE in your notes; optional: 2D lid-driven cavity in NumPy (2 sessions).

## Resources

- Versteeg & Malalasekera — *An Introduction to Computational Fluid Dynamics: The Finite Volume Method* (2nd ed.) — ch. 6: pressure–velocity coupling — The classic FVM book: diffusion, convection schemes, SIMPLE, turbulence.
- [Lorena Barba — *CFD Python: 12 steps to Navier–Stokes* (notebooks + video lessons)](https://github.com/barbagroup/CFDPython) — steps 11–12 (cavity, channel) — Build a 2D Navier–Stokes solver step by step in Python.
- [Fluid Mechanics 101 (Aidan Wimshurst) — YouTube CFD lectures](https://www.youtube.com/results?search_query=Fluid+Mechanics+101+Aidan+Wimshurst) — SIMPLE / PISO lectures — Excellent short lectures on FVM, SIMPLE, turbulence models, y+ and wall functions.
- More: [subject resources](README.md#resources)

## Notes

-

## Open questions

-
