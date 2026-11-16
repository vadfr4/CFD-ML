# Conservation laws and the Navier–Stokes equations

**Subject:** Fluid dynamics fundamentals · **Time:** ~2 h session

**Goal:** Derive (or re-derive) continuity and momentum equations and know what every term means.

## Session plan

| Block | Time | What |
|---|---|---|
| Theory | ~30 min | Read the theory below and follow every step on paper |
| Hands-on | ~75 min | Work the example, then build your one-page sheet |
| Wrap-up | ~15 min | Answer the check questions, write notes and open questions |

## Topics

- [ ] Review control-volume form of mass and momentum conservation
- [ ] Write the incompressible Navier–Stokes equations in vector and index notation
- [ ] Identify convection, pressure, diffusion and source terms

## Theory

Every CFD solver and every flow model in this course starts from two statements: mass is conserved, and Newton's second law holds for every piece of fluid. Write them for a small region of space, let the region shrink, and you get the Navier–Stokes equations.

### The control volume

Pick a fixed region of space $V$ with surface $S$ and outward unit normal $\mathbf{n}$. Fluid with density $\rho$ and velocity $\mathbf{u}$ flows through it. Two things can change the amount of a quantity inside $V$: it can flow in or out through $S$, and it can be created or destroyed inside. Conservation laws are just bookkeeping of those two effects.

This is also exactly what a finite volume solver like OpenFOAM does: each mesh cell is a small control volume, and the solver balances fluxes through its faces.

### Mass: the continuity equation

The mass inside $V$ changes only because of the net flow through the surface:

$$
\frac{\mathrm{d}}{\mathrm{d}t}\int_V \rho \,\mathrm{d}V \;+\; \oint_S \rho\,\mathbf{u}\cdot\mathbf{n}\,\mathrm{d}S = 0
$$

The divergence theorem turns the surface integral into a volume integral, $\oint_S \rho\,\mathbf{u}\cdot\mathbf{n}\,\mathrm{d}S = \int_V \nabla\cdot(\rho\mathbf{u})\,\mathrm{d}V$. Because $V$ is fixed, the time derivative moves inside the integral. The result holds for every $V$, however small, so the integrand itself must be zero:

$$
\frac{\partial \rho}{\partial t} + \nabla\cdot(\rho\,\mathbf{u}) = 0
$$

For water, and for air well below the speed of sound (Mach number below about 0.3), density is effectively constant. Then the equation reduces to

$$
\nabla\cdot\mathbf{u} = 0 \qquad\text{or, in index notation,}\qquad \frac{\partial u_j}{\partial x_j} = 0
$$

In index notation a repeated index is summed over $j = 1, 2, 3$. So $\partial u_j/\partial x_j = \partial u/\partial x + \partial v/\partial y + \partial w/\partial z$.

### Momentum

Newton's second law for the fluid in $V$: the rate of change of momentum inside, plus the momentum carried out through $S$, equals the forces on the fluid.

$$
\frac{\mathrm{d}}{\mathrm{d}t}\int_V \rho\,\mathbf{u}\,\mathrm{d}V \;+\; \oint_S \rho\,\mathbf{u}\,(\mathbf{u}\cdot\mathbf{n})\,\mathrm{d}S
= \oint_S \boldsymbol{\sigma}\cdot\mathbf{n}\,\mathrm{d}S \;+\; \int_V \rho\,\mathbf{g}\,\mathrm{d}V
$$

There are two kinds of force:

* **Surface forces**, through the stress tensor $\boldsymbol{\sigma}$. It splits into pressure, which pushes equally in all directions, and viscous stress: $\boldsymbol{\sigma} = -p\,\mathbf{I} + \boldsymbol{\tau}$.
* **Body forces** acting on the whole volume, here gravity $\mathbf{g}$.

Applying the divergence theorem again gives the differential form:

$$
\frac{\partial (\rho\mathbf{u})}{\partial t} + \nabla\cdot(\rho\,\mathbf{u}\mathbf{u}) = -\nabla p + \nabla\cdot\boldsymbol{\tau} + \rho\,\mathbf{g}
$$

### The viscous term for a Newtonian fluid

For water, air and most fluids in engineering, viscous stress is proportional to the rate of deformation. With constant viscosity $\mu$ in an incompressible flow:

$$
\tau_{ij} = \mu\left(\frac{\partial u_i}{\partial x_j} + \frac{\partial u_j}{\partial x_i}\right)
$$

Its divergence simplifies nicely. The second part vanishes because of continuity:

$$
\frac{\partial \tau_{ij}}{\partial x_j}
= \mu\frac{\partial^2 u_i}{\partial x_j \partial x_j} + \mu\frac{\partial}{\partial x_i}\underbrace{\left(\frac{\partial u_j}{\partial x_j}\right)}_{=\,0}
= \mu\,\nabla^2 u_i
$$

### The result: incompressible Navier–Stokes

Divide by the constant density and write $\nu = \mu/\rho$ for the kinematic viscosity:

$$
\underbrace{\frac{\partial \mathbf{u}}{\partial t}}_{\text{unsteady}}
+ \underbrace{(\mathbf{u}\cdot\nabla)\,\mathbf{u}}_{\text{convection}}
= \underbrace{-\frac{1}{\rho}\nabla p}_{\text{pressure gradient}}
+ \underbrace{\nu\,\nabla^2\mathbf{u}}_{\text{diffusion}}
+ \underbrace{\mathbf{g}}_{\text{body force}},
\qquad \nabla\cdot\mathbf{u} = 0
$$

In index notation:

$$
\frac{\partial u_i}{\partial t} + u_j\frac{\partial u_i}{\partial x_j}
= -\frac{1}{\rho}\frac{\partial p}{\partial x_i} + \nu\frac{\partial^2 u_i}{\partial x_j\partial x_j} + g_i,
\qquad \frac{\partial u_j}{\partial x_j} = 0
$$

That is four equations (three momentum components plus continuity) for four unknowns ($u$, $v$, $w$, $p$).

### What each term does

* **Unsteady** $\partial\mathbf{u}/\partial t$: how fast the velocity changes at a fixed point. Zero in a steady flow.
* **Convection** $(\mathbf{u}\cdot\nabla)\mathbf{u}$: the flow carrying its own momentum along. It is *nonlinear* (velocity times a velocity gradient), which is why turbulence exists, why solvers must iterate, and why Lesson 02.2 is about the schemes used for it.
* **Pressure gradient** $-\nabla p/\rho$: fluid is pushed from high to low pressure.
* **Diffusion** $\nu\nabla^2\mathbf{u}$: viscosity smooths out velocity differences, the way heat conduction smooths temperature.
* **Body force** $\mathbf{g}$: gravity, or any other force acting on the volume.

The Reynolds number (next lesson) measures convection against diffusion.

### Where pressure comes from in incompressible flow

There is no equation of the form "$\partial p/\partial t = \ldots$". In incompressible flow, pressure takes whatever value makes the velocity field satisfy $\nabla\cdot\mathbf{u} = 0$. Taking the divergence of the momentum equation gives a Poisson equation for it:

$$
\nabla^2 p = -\rho\,\frac{\partial u_i}{\partial x_j}\frac{\partial u_j}{\partial x_i}
$$

This coupling between pressure and velocity is the central difficulty in incompressible CFD. Lesson 02.4 (SIMPLE and PISO) is about how solvers handle it.

### Conservative form, and how it looks in OpenFOAM

Using $\nabla\cdot\mathbf{u} = 0$, the convection term can also be written as $\nabla\cdot(\mathbf{u}\mathbf{u})$. This *conservative* form is the one finite volume methods discretise, because the divergence becomes a sum of fluxes over cell faces.

OpenFOAM's `icoFoam` solver (laminar, incompressible) writes the momentum equation almost exactly like the maths:

```cpp
fvVectorMatrix UEqn
(
    fvm::ddt(U)                 // unsteady
  + fvm::div(phi, U)            // convection, phi = face flux of u
  - fvm::laplacian(nu, U)       // diffusion
);
solve(UEqn == -fvc::grad(p));  // pressure gradient
```

One detail to remember: in OpenFOAM's incompressible solvers, `p` is the *kinematic* pressure $p/\rho$, in m²/s², not pascals.

## Worked example

**Show that plane Couette flow and plane Poiseuille flow are exact solutions, and find the pressure gradient each one needs.**

Both flows lie between two parallel plates at $y = 0$ and $y = h$, are steady, and have velocity only in $x$: $\mathbf{u} = (u(y),\,0,\,0)$. Ignore gravity.

**Continuity.** $\partial u/\partial x + \partial v/\partial y = 0 + 0 = 0$. Satisfied for any $u(y)$.

**$x$-momentum.** The unsteady term is zero (steady). Convection is $u\,\partial u/\partial x + v\,\partial u/\partial y = u\cdot 0 + 0\cdot u' = 0$. What remains is

$$
0 = -\frac{1}{\rho}\frac{\mathrm{d}p}{\mathrm{d}x} + \nu\,\frac{\mathrm{d}^2 u}{\mathrm{d}y^2}
$$

**$y$-momentum.** Every velocity term is zero, so $\partial p/\partial y = 0$: pressure varies only with $x$.

The left part, $\mathrm{d}p/\mathrm{d}x$, can depend only on $x$, and the right part only on $y$. So both must equal the same constant. Write $G = -\mathrm{d}p/\mathrm{d}x$.

* **Couette** (top plate moves at speed $U$, no pressure gradient, $G = 0$): $u'' = 0$, so $u = a y + b$. The no-slip conditions $u(0) = 0$ and $u(h) = U$ give $u = U\,y/h$.
* **Poiseuille** (both plates still, driven by $G > 0$): $u'' = -G/\mu$. Integrating twice with $u(0) = u(h) = 0$ gives

$$
u(y) = \frac{G}{2\mu}\,y\,(h - y)
$$

The nonlinear convection term vanished on its own, which is why these flows have exact solutions. You will plot both in Lesson 01.3.

## Build

One-page cheat sheet of the equations with every term labelled.

Step by step, on paper or in a Markdown file in this folder:

1. Write the integral mass balance for a fixed control volume. Then derive the differential form, naming the divergence theorem where you use it.
2. Do the same for momentum. Split the stress into pressure and viscous parts.
3. Derive $\nabla\cdot\boldsymbol{\tau} = \mu\nabla^2\mathbf{u}$ yourself in index notation, and mark where continuity is used.
4. Write the final incompressible equations in both vector and index notation. Label each term (unsteady, convection, pressure, diffusion, body force).
5. Give the SI units of every term in the kinematic form. They should all come out as m/s².
6. Next to it, copy the four lines of `icoFoam`'s momentum equation and draw a line from each term to its maths.

## Check yourself

1. In the incompressible momentum equation divided by $\rho$, what are the units of every term?

   <details markdown="1"><summary>Answer</summary>

   All are accelerations, m/s². For example $\nu\nabla^2\mathbf{u}$: m²/s × (m/s)/m² = m/s².

   </details>

2. Show that $\nabla\cdot(\mathbf{u}\mathbf{u}) = (\mathbf{u}\cdot\nabla)\mathbf{u}$ when $\nabla\cdot\mathbf{u} = 0$.

   <details markdown="1"><summary>Answer</summary>

   $\dfrac{\partial (u_i u_j)}{\partial x_j} = u_j\dfrac{\partial u_i}{\partial x_j} + u_i\dfrac{\partial u_j}{\partial x_j}$. The last term is $u_i$ times the divergence, which is zero.

   </details>

3. Which term makes the Navier–Stokes equations nonlinear, and why does that matter for a solver?

   <details markdown="1"><summary>Answer</summary>

   Convection, $(\mathbf{u}\cdot\nabla)\mathbf{u}$. A solver cannot solve for $\mathbf{u}$ in one linear step. It linearises, using the latest velocity (in OpenFOAM, the face flux `phi`) to carry the new one, and iterates.

   </details>

4. An incompressible OpenFOAM case reports `p` = 50 at the inlet of a water flow. What is the pressure in pascals?

   <details markdown="1"><summary>Answer</summary>

   It is kinematic pressure in m²/s². Multiply by density: 50 × 1000 = 50 000 Pa above the reference pressure.

   </details>

## Common mistakes

* **Forgetting the transpose part of the viscous stress.** It only drops out because $\nabla\cdot\mathbf{u} = 0$. In compressible flow it stays.
* **Treating pressure like temperature.** In incompressible flow pressure has no equation of its own. It is set by the continuity constraint.
* **Mixing up kinematic and real pressure** when reading OpenFOAM results.
* **Writing $\nabla^2\mathbf{u}$ component by component in cylindrical coordinates.** The vector Laplacian picks up extra terms there.

## Resources

- Kundu, Cohen & Dowling — *Fluid Mechanics* (6th ed., Academic Press) — conservation laws chapter — The standard graduate fluid mechanics text.
- Anderson — *Computational Fluid Dynamics: The Basics with Applications* (McGraw-Hill) — ch. 2: governing equations — Gentlest introduction to CFD; great for equations and finite differences.
- [MIT / NCFMF — *Fluid Mechanics Films* (1960s classics, still the best visual intuition)](http://web.mit.edu/hml/ncfmf.html)
- More: [subject resources](README.md#resources)

## Notes

-

## Open questions

-
