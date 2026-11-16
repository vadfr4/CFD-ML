"""Write the exercise and solution notebooks for subjects 01 and 02.

Each notebook is written once from the source below. Code between
`### BEGIN SOLUTION` and `### END SOLUTION` is kept in the solution notebook
and replaced by a TODO in the exercise notebook.

    python tools/make_notebooks.py           # write both versions
    python tools/make_notebooks.py --run     # also execute the solutions (needs nbclient, ipykernel)
"""
import argparse
import re
from pathlib import Path

import nbformat as nbf

ROOT = Path(__file__).resolve().parent.parent
SOL = re.compile(r"^([ \t]*)### BEGIN SOLUTION\n.*?^[ \t]*### END SOLUTION\n", re.S | re.M)


def exercise(code):
    return SOL.sub(lambda m: f"{m.group(1)}# YOUR CODE HERE\n{m.group(1)}raise NotImplementedError\n", code)


def solution(code):
    return re.sub(r"^[ \t]*### (BEGIN|END) SOLUTION\n", "", code, flags=re.M)


SETUP = """import numpy as np
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (7, 4)"""

NOTEBOOKS = {}

# --------------------------------------------------------------------------
NOTEBOOKS["01-fluid-dynamics-fundamentals/02-non-dimensional-numbers-and-flow-regimes"] = [
    ("md", """# Non-dimensional numbers and flow regimes

Estimate the Reynolds number for everyday flows and predict whether each one is laminar or turbulent.

$$Re = \\frac{\\rho U L}{\\mu} = \\frac{U L}{\\nu}$$

For pipe flow, transition starts around $Re_D \\approx 2300$. Over a flat plate it starts around $Re_x \\approx 5 \\times 10^5$."""),
    ("code", SETUP + "\nimport pandas as pd"),
    ("md", "Kinematic viscosities at about 20 °C, in m²/s."),
    ("code", """nu = {"air": 1.5e-5, "water": 1.0e-6, "honey": 7e-3}"""),
    ("md", "**Exercise 1.** Write `reynolds(U, L, fluid)`."),
    ("code", """def reynolds(U, L, fluid):
    ### BEGIN SOLUTION
    return U * L / nu[fluid]
    ### END SOLUTION

assert abs(reynolds(1.0, 1.0, "water") - 1e6) < 1"""),
    ("md", """**Exercise 2.** Fill in the table: compute $Re$ for each flow and label it laminar or turbulent with the given threshold."""),
    ("code", """flows = pd.DataFrame([
    # name,                        U [m/s], L [m],  fluid,   threshold
    ("Water in a 15 mm tap pipe",   1.0,     0.015, "water", 2300),
    ("Honey poured from a spoon",   0.05,    0.01,  "honey", 2300),
    ("Car at 100 km/h, 4 m long",   27.8,    4.0,   "air",   5e5),
    ("Cyclist, 1.7 m tall, 8 m/s",  8.0,     1.7,   "air",   5e5),
    ("Blood in a capillary",        1e-3,    8e-6,  "water", 2300),
], columns=["flow", "U", "L", "fluid", "threshold"])

### BEGIN SOLUTION
flows["Re"] = [reynolds(r.U, r.L, r.fluid) for r in flows.itertuples()]
flows["regime"] = np.where(flows["Re"] > flows["threshold"], "turbulent", "laminar")
### END SOLUTION
flows"""),
    ("md", """**Question.** Which of these flows could you simulate without a turbulence model? Write your answer in the lesson's Notes section."""),
]

# --------------------------------------------------------------------------
NOTEBOOKS["01-fluid-dynamics-fundamentals/03-analytical-solutions-couette-poiseuille-and-boundary-layers"] = [
    ("md", """# Analytical solutions: Couette, Poiseuille and the Blasius boundary layer

These exact solutions are your reference for checking CFD and ML results later.

* **Couette flow** (top plate moves at $U$, gap $h$): $u(y) = U\\,y/h$
* **Plane Poiseuille flow** (pressure gradient $G = -\\mathrm{d}p/\\mathrm{d}x$): $u(y) = \\frac{G}{2\\mu}\\,y\\,(h - y)$
* **Blasius boundary layer**: thickness $\\delta_{99}(x) \\approx 5.0\\,x / \\sqrt{Re_x}$"""),
    ("code", SETUP),
    ("md", "**Exercise 1.** Implement both velocity profiles."),
    ("code", """def couette(y, U, h):
    ### BEGIN SOLUTION
    return U * y / h
    ### END SOLUTION


def poiseuille(y, G, mu, h):
    ### BEGIN SOLUTION
    return G / (2 * mu) * y * (h - y)
    ### END SOLUTION

h, mu = 0.01, 1e-3            # 1 cm gap, water
y = np.linspace(0, h, 201)
u_c = couette(y, U=0.1, h=h)
u_p = poiseuille(y, G=8.0, mu=mu, h=h)

fig, ax = plt.subplots()
ax.plot(u_c, y * 1e3, label="Couette")
ax.plot(u_p, y * 1e3, label="Poiseuille")
ax.set_xlabel("u [m/s]"); ax.set_ylabel("y [mm]"); ax.legend();"""),
    ("md", """**Exercise 2.** For Poiseuille flow the mean velocity is exactly 2/3 of the maximum. Check it numerically with `np.trapezoid`."""),
    ("code", """### BEGIN SOLUTION
u_mean = np.trapezoid(u_p, y) / h
ratio = u_mean / u_p.max()
### END SOLUTION
print(f"mean / max = {ratio:.4f}")
assert abs(ratio - 2 / 3) < 1e-3"""),
    ("md", """**Exercise 3.** Air ($\\nu = 1.5\\times10^{-5}$ m²/s) flows at 5 m/s over a 1 m flat plate. Plot $\\delta_{99}(x)$ and find the thickness at $x = 0.5$ m. Is the flow still laminar there?"""),
    ("code", """nu, U = 1.5e-5, 5.0
x = np.linspace(1e-3, 1.0, 400)
### BEGIN SOLUTION
Re_x = U * x / nu
delta = 5.0 * x / np.sqrt(Re_x)
delta_half = 5.0 * 0.5 / np.sqrt(U * 0.5 / nu)
### END SOLUTION
print(f"delta_99 at x = 0.5 m: {delta_half * 1e3:.2f} mm, Re_x = {U * 0.5 / nu:.3g}")

fig, ax = plt.subplots()
ax.plot(x, delta * 1e3)
ax.set_xlabel("x [m]"); ax.set_ylabel("delta_99 [mm]");"""),
    ("md", "Keep this notebook. You will reuse these functions to check simulation and ML results against exact answers."),
]

# --------------------------------------------------------------------------
NOTEBOOKS["02-numerical-methods/01-finite-differences-and-the-1d-diffusion-equation"] = [
    ("md", """# Finite differences and the 1D diffusion equation

Solve $\\partial u/\\partial t = \\alpha\\,\\partial^2 u/\\partial x^2$ on $0 \\le x \\le 1$ with $u = 0$ at both ends and $u(x, 0) = \\sin(\\pi x)$.

The exact solution is $u(x,t) = \\sin(\\pi x)\\,e^{-\\alpha \\pi^2 t}$.

The explicit (FTCS) scheme is stable only when $r = \\alpha\\,\\Delta t/\\Delta x^2 \\le 1/2$."""),
    ("code", SETUP),
    ("code", """alpha, nx, t_end = 0.01, 51, 5.0
x = np.linspace(0, 1, nx)
dx = x[1] - x[0]

def exact(x, t):
    return np.sin(np.pi * x) * np.exp(-alpha * np.pi**2 * t)"""),
    ("md", """**Exercise 1.** Write one explicit time step:
$u_i^{n+1} = u_i^n + r\\,(u_{i+1}^n - 2u_i^n + u_{i-1}^n)$. Keep the boundary values at zero."""),
    ("code", """def ftcs_step(u, r):
    ### BEGIN SOLUTION
    un = u.copy()
    un[1:-1] = u[1:-1] + r * (u[2:] - 2 * u[1:-1] + u[:-2])
    return un
    ### END SOLUTION


def solve_explicit(r):
    dt = r * dx**2 / alpha
    u = np.sin(np.pi * x)
    for _ in range(int(round(t_end / dt))):
        u = ftcs_step(u, r)
    return u

for r in (0.25, 0.5, 0.6):
    u = solve_explicit(r)
    print(f"r = {r:4}: max error = {np.abs(u - exact(x, t_end)).max():.2e}")"""),
    ("md", """At $r = 0.6$ the error explodes. Round-off errors in the shortest wavelength are multiplied by $|1 - 4r| = 1.4$ every step.

**Exercise 2.** Write an implicit (backward Euler) step. It is stable for any $r$. You need to solve $A\\,u^{n+1} = u^n$ with $A$ tridiagonal: $1 + 2r$ on the diagonal and $-r$ next to it. Use `np.linalg.solve`."""),
    ("code", """def implicit_matrix(n, r):
    ### BEGIN SOLUTION
    A = np.eye(n) * (1 + 2 * r) - r * np.eye(n, k=1) - r * np.eye(n, k=-1)
    A[0, :] = 0; A[0, 0] = 1        # boundary rows keep u = 0
    A[-1, :] = 0; A[-1, -1] = 1
    return A
    ### END SOLUTION


def solve_implicit(r):
    dt = r * dx**2 / alpha
    A = implicit_matrix(nx, r)
    u = np.sin(np.pi * x)
    for _ in range(int(round(t_end / dt))):
        u = np.linalg.solve(A, u)
    return u

fig, ax = plt.subplots()
ax.plot(x, exact(x, t_end), "k", lw=3, alpha=0.3, label="exact")
for r in (0.5, 5.0):
    ax.plot(x, solve_implicit(r), "--", label=f"implicit, r = {r}")
ax.plot(x, solve_explicit(0.25), ":", label="explicit, r = 0.25")
ax.set_xlabel("x"); ax.set_ylabel("u"); ax.legend();"""),
    ("md", """**Question.** The implicit scheme is stable at $r = 5$. Is it also accurate there? Compare the error with $r = 0.5$, and note why in the lesson file."""),
]

# --------------------------------------------------------------------------
NOTEBOOKS["02-numerical-methods/02-convection-upwind-central-schemes-and-the-cfl-condition"] = [
    ("md", """# Convection: upwind, central and the CFL condition

Linear advection: $\\partial u/\\partial t + c\\,\\partial u/\\partial x = 0$, on a periodic domain. A square wave should move without changing shape.

The Courant number is $C = c\\,\\Delta t/\\Delta x$."""),
    ("code", SETUP),
    ("code", """c, nx = 1.0, 200
x = np.linspace(0, 2, nx, endpoint=False)
dx = x[1] - x[0]
u0 = np.where((x > 0.25) & (x < 0.75), 1.0, 0.0)

def run(step, C, t_end=1.0):
    dt = C * dx / c
    u = u0.copy()
    for _ in range(int(round(t_end / dt))):
        u = step(u, C)
    return u

exact = np.roll(u0, int(round(1.0 / dx)))   # shifted by c * t_end = 1"""),
    ("md", """**Exercise 1.** Write the first-order upwind step for $c > 0$: $u_i^{n+1} = u_i^n - C\\,(u_i^n - u_{i-1}^n)$. Use `np.roll` for the periodic neighbour."""),
    ("code", """def upwind(u, C):
    ### BEGIN SOLUTION
    return u - C * (u - np.roll(u, 1))
    ### END SOLUTION"""),
    ("md", """**Exercise 2.** Write the central (FTCS) step: $u_i^{n+1} = u_i^n - \\tfrac{C}{2}\\,(u_{i+1}^n - u_{i-1}^n)$."""),
    ("code", """def central(u, C):
    ### BEGIN SOLUTION
    return u - 0.5 * C * (np.roll(u, -1) - np.roll(u, 1))
    ### END SOLUTION"""),
    ("md", """**Exercise 3.** Lax–Wendroff is second order and stable for $C \\le 1$:
$u_i^{n+1} = u_i^n - \\tfrac{C}{2}(u_{i+1}-u_{i-1}) + \\tfrac{C^2}{2}(u_{i+1} - 2u_i + u_{i-1})$."""),
    ("code", """def lax_wendroff(u, C):
    ### BEGIN SOLUTION
    up, um = np.roll(u, -1), np.roll(u, 1)
    return u - 0.5 * C * (up - um) + 0.5 * C**2 * (up - 2 * u + um)
    ### END SOLUTION

fig, axes = plt.subplots(1, 3, figsize=(13, 3.5), sharey=True)
for ax, (name, step) in zip(axes, [("upwind", upwind), ("central", central), ("Lax-Wendroff", lax_wendroff)]):
    ax.plot(x, exact, "k", lw=3, alpha=0.3, label="exact")
    ax.plot(x, run(step, C=0.5), label="C = 0.5")
    ax.set_title(name); ax.set_ylim(-0.5, 1.5); ax.set_xlabel("x")
axes[0].legend();"""),
    ("md", """What you should see:

* **Upwind** smears the edges. This is numerical diffusion.
* **Central** oscillates and blows up. FTCS is unconditionally unstable for pure advection.
* **Lax–Wendroff** keeps the edges sharper but wiggles next to them.

**Exercise 4.** Run upwind with $C = 1.0$ and $C = 1.1$. Explain both results in your notes."""),
    ("code", """### BEGIN SOLUTION
for C in (1.0, 1.1):
    err = np.abs(run(upwind, C) - exact).max()
    print(f"upwind, C = {C}: max error = {err:.3g}")
### END SOLUTION"""),
]

# --------------------------------------------------------------------------
NOTEBOOKS["02-numerical-methods/03-the-finite-volume-method"] = [
    ("md", """# The finite volume method: 1D steady convection–diffusion

$$\\frac{\\mathrm{d}}{\\mathrm{d}x}(\\rho u \\phi) = \\frac{\\mathrm{d}}{\\mathrm{d}x}\\left(\\Gamma \\frac{\\mathrm{d}\\phi}{\\mathrm{d}x}\\right), \\qquad \\phi(0) = 1,\\ \\phi(L) = 0$$

This is the classic example from Versteeg & Malalasekera, chapter 5: $L = 1$ m, $\\rho = 1$, $\\Gamma = 0.1$. The exact solution is

$$\\phi(x) = 1 - \\frac{e^{\\rho u x/\\Gamma} - 1}{e^{\\rho u L/\\Gamma} - 1}$$

Split the domain into $N$ cells. For each cell P with neighbours W and E: $a_P\\phi_P = a_W\\phi_W + a_E\\phi_E + S_u$, where $F = \\rho u$ is the convective flux and $D = \\Gamma/\\Delta x$ is the diffusive conductance."""),
    ("code", SETUP),
    ("code", """L, rho, Gamma = 1.0, 1.0, 0.1
phi_A, phi_B = 1.0, 0.0

def exact(x, u):
    return 1 - (np.exp(rho * u * x / Gamma) - 1) / (np.exp(rho * u * L / Gamma) - 1)"""),
    ("md", """**Exercise.** Build and solve the system for the central and the upwind scheme. Boundary cells use a half-cell distance to the wall, so their diffusive conductance is $2D$.

| scheme | $a_W$ | $a_E$ |
|---|---|---|
| central | $D + F/2$ | $D - F/2$ |
| upwind ($F>0$) | $D + F$ | $D$ |

Interior cells have $a_P = a_W + a_E$. In the first cell, the west link becomes a source: $S_P = -(2D + F)$ and $S_u = (2D + F)\\phi_A$. At the east boundary the link to $\\phi_B$ is $2D - F$ for central and $2D$ for upwind."""),
    ("code", """def fvm(N, u, scheme):
    dx = L / N
    F, D = rho * u, Gamma / dx
    A = np.zeros((N, N)); b = np.zeros(N)
    ### BEGIN SOLUTION
    for i in range(N):
        if scheme == "central":
            aW, aE = D + F / 2, D - F / 2
        else:
            aW, aE = D + F, D
        Sp = 0.0
        if i == 0:                       # west boundary, phi_A
            aW = 0.0
            coef = 2 * D + F
            Sp -= coef; b[i] += coef * phi_A
        if i == N - 1:                   # east boundary, phi_B
            aE = 0.0
            coef = 2 * D - F if scheme == "central" else 2 * D
            Sp -= coef; b[i] += coef * phi_B
        aP = aW + aE - Sp               # F_e - F_w = 0 for constant u
        A[i, i] = aP
        if i > 0: A[i, i - 1] = -aW
        if i < N - 1: A[i, i + 1] = -aE
    ### END SOLUTION
    xc = (np.arange(N) + 0.5) * dx
    return xc, np.linalg.solve(A, b)

xf = np.linspace(0, L, 200)
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
for ax, u in zip(axes, (0.1, 2.5)):
    ax.plot(xf, exact(xf, u), "k", lw=3, alpha=0.3, label="exact")
    for scheme in ("central", "upwind"):
        xc, phi = fvm(5, u, scheme)
        ax.plot(xc, phi, "o--", label=scheme)
    ax.set_title(f"u = {u} m/s, cell Peclet = {rho * u * 0.2 / Gamma:.1f}"); ax.legend()"""),
    ("md", """What you should see: at $u = 0.1$ both schemes match the exact curve. At $u = 2.5$ the cell Péclet number is 5 and central differencing oscillates, while upwind stays bounded but smeared.

**Question.** How many cells does central need at $u = 2.5$ to stop oscillating? (Hint: keep the cell Péclet number below 2.)"""),
]


def build(run=False):
    for stem, cells in NOTEBOOKS.items():
        folder = ROOT / Path(stem).parent
        name = Path(stem).name
        for kind in ("exercise", "solution"):
            nb = nbf.v4.new_notebook()
            nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
            for t, src in cells:
                if t == "md":
                    nb.cells.append(nbf.v4.new_markdown_cell(src))
                else:
                    nb.cells.append(nbf.v4.new_code_cell(exercise(src) if kind == "exercise" else solution(src)))
            if kind == "exercise":
                path = folder / f"{name}.ipynb"
            else:
                path = folder / "solutions" / f"{name}.ipynb"
                path.parent.mkdir(exist_ok=True)
                if run:
                    from nbclient import NotebookClient
                    NotebookClient(nb, timeout=300, kernel_name="python3",
                                   resources={"metadata": {"path": str(path.parent)}}).execute()
            nbf.write(nb, path)
            print("wrote", path.relative_to(ROOT))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    build(ap.parse_args().run)
