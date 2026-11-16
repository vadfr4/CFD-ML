"""Check that your machine is ready for the CFD-ML lessons.

Run it with the same Python you will use for the notebooks:

    python tools/check_setup.py

It checks the Python version, the packages in requirements.txt, and where
OpenFOAM is installed (inside WSL, natively on Windows, or on Linux/macOS).
Nothing is installed or changed; it only reports.
"""
import importlib
import os
import platform
import shutil
import subprocess
import sys

# requirements.txt name -> import name, and which subjects need it
PACKAGES = [
    ("numpy", "numpy", "all"),
    ("scipy", "scipy", "all"),
    ("pandas", "pandas", "all"),
    ("matplotlib", "matplotlib", "all"),
    ("jupyterlab", "jupyterlab", "all"),
    ("scikit-learn", "sklearn", "06 onwards"),
    ("torch", "torch", "07 onwards"),
    ("pyvista", "pyvista", "03 onwards"),
    ("meshio", "meshio", "03 onwards"),
    ("tqdm", "tqdm", "05 onwards"),
]

OK, WARN, FAIL = "ok  ", "warn", "FAIL"
problems = []


def line(status, what, detail=""):
    print(f"  [{status}] {what}" + (f": {detail}" if detail else ""))
    if status != OK:
        problems.append(what)


def run(cmd, timeout=60):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout + r.stderr).replace("\x00", "").strip()
    except (OSError, subprocess.TimeoutExpired) as e:
        return 1, str(e)


def check_python():
    print("\nPython")
    v = sys.version_info
    detail = f"{v.major}.{v.minor}.{v.micro} at {sys.executable}"
    line(OK if v >= (3, 10) else FAIL, "Python 3.10 or newer", detail)


def check_packages():
    print("\nPackages (pip install -r requirements.txt)")
    for name, mod, needed in PACKAGES:
        try:
            m = importlib.import_module(mod)
            line(OK, name, getattr(m, "__version__", "installed"))
        except Exception:
            status = FAIL if needed == "all" else WARN
            when = "from the start" if needed == "all" else f"for subjects {needed}"
            line(status, name, f"missing, needed {when}")


# A login shell does not read ~/.bashrc, where OpenFOAM is usually sourced,
# so the probe uses an interactive shell and also tries the common install paths.
PROBE = (
    "for f in /opt/openfoam*/etc/bashrc /usr/lib/openfoam/openfoam*/etc/bashrc; do "
    "[ -z \"$WM_PROJECT_VERSION\" ] && [ -f \"$f\" ] && . \"$f\" >/dev/null 2>&1; done; "
    "if command -v simpleFoam >/dev/null; then "
    "echo \"FOUND $WM_PROJECT $WM_PROJECT_VERSION $(command -v simpleFoam)\"; else echo NOTFOUND; fi"
)


def probe_linux():
    if os.environ.get("WM_PROJECT_VERSION") and shutil.which("simpleFoam"):
        return f"{os.environ.get('WM_PROJECT', 'OpenFOAM')} {os.environ['WM_PROJECT_VERSION']} (already loaded)"
    code, out = run(["bash", "-ic", PROBE])
    for l in out.splitlines():
        if l.startswith("FOUND"):
            return l[6:]
    return None


def check_openfoam():
    print("\nOpenFOAM")
    system = platform.system()
    in_wsl = system == "Linux" and "microsoft" in platform.release().lower()

    if system == "Windows":
        found_any = False
        wsl = shutil.which("wsl")
        if wsl:
            code, out = run([wsl, "-e", "bash", "-ic", PROBE], timeout=120)
            hit = next((l for l in out.splitlines() if l.startswith("FOUND")), None)
            if hit:
                found_any = True
                line(OK, "OpenFOAM inside WSL", hit[6:])
            else:
                line(WARN, "OpenFOAM inside WSL", "WSL is installed but OpenFOAM was not found in it")
        else:
            line(WARN, "WSL", "not installed (run 'wsl --install' in an admin PowerShell)")

        # Native Windows builds: openfoam.com MSYS2 builds and blueCFD-Core
        candidates = []
        for base in filter(None, [os.environ.get("ProgramFiles"), "C:\\", os.path.expanduser("~")]):
            try:
                for name in os.listdir(base):
                    if "openfoam" in name.lower() or "bluecfd" in name.lower():
                        candidates.append(os.path.join(base, name))
            except OSError:
                pass
        if candidates:
            found_any = True
            line(OK, "OpenFOAM installed on Windows", "; ".join(candidates))
            print("         The lessons assume a Linux shell. A native Windows build works for")
            print("         running cases, but the tutorials and scripts are easiest inside WSL.")
        if not found_any:
            line(FAIL, "OpenFOAM", "not found in WSL or in the usual Windows folders")
            print("         Install it inside WSL: see lesson 03.1 (Installation and case structure).")
        return

    where = "inside WSL" if in_wsl else f"on {system}"
    found = probe_linux()
    if found:
        line(OK, f"OpenFOAM {where}", found)
    else:
        line(FAIL, f"OpenFOAM {where}", "simpleFoam not found; source OpenFOAM's etc/bashrc in ~/.bashrc")


def check_paraview():
    print("\nParaView (for looking at results)")
    exe = shutil.which("paraview") or shutil.which("paraFoam")
    if exe:
        line(OK, "ParaView", exe)
    elif platform.system() == "Windows" or "microsoft" in platform.release().lower():
        line(OK, "ParaView", "not on PATH here; installing it on Windows and opening WSL files works fine")
    else:
        line(WARN, "ParaView", "not found; pyvista can stand in until lesson 03.2")


def main():
    print("CFD-ML setup check")
    print(f"System: {platform.system()} {platform.release()}")
    check_python()
    check_packages()
    check_openfoam()
    check_paraview()
    print()
    if problems:
        print(f"{len(problems)} thing(s) to fix: " + ", ".join(problems))
        print("Subjects 01 and 02 only need numpy, matplotlib and Jupyter, so you can start those once they show ok.")
        return 1
    print("Everything is ready. Start with lesson 01.1.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
