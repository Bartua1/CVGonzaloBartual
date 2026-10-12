import os
import re
import shutil
import sys
import subprocess
from pathlib import Path

# Rutas candidatas por plataforma. Se puede forzar un binario concreto con la
# variable de entorno CV_BROWSER=/ruta/al/binario
BROWSER_CANDIDATES = {
    "win32": [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ],
    "darwin": [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ],
    "linux": [
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/usr/bin/microsoft-edge",
        "/usr/bin/microsoft-edge-stable",
        "/snap/bin/chromium",
        "/var/lib/flatpak/exports/bin/com.google.Chrome",
    ],
}

# Binarios que podemos encontrar en el PATH (Linux/macOS con instalaciones no
# estándar o gestores de paquetes que no enlazan en /usr/bin).
PATH_BINARIES = (
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
    "microsoft-edge",
    "microsoft-edge-stable",
    "msedge",
)


def _playwright_chromium():
    """Chromium descargado por Playwright (no requiere navegador del sistema).

    Playwright las guarda en ~/.cache/ms-playwright/chromium-<build>/chrome-linux*/
    """
    if not sys.platform.startswith("linux"):
        return None
    base = Path.home() / ".cache" / "ms-playwright"
    if not base.is_dir():
        return None

    def build_number(path):
        match = re.search(r"chromium-(\d+)", str(path))
        return int(match.group(1)) if match else 0

    candidates = sorted(
        base.glob("chromium-*/chrome-linux*/chrome"),
        key=build_number,
        reverse=True,  # el build más reciente primero
    )
    for candidate in candidates:
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate)
    return None


def find_browser():
    override = os.environ.get("CV_BROWSER")
    if override:
        if Path(override).is_file() and os.access(override, os.X_OK):
            return override
        print(f"Error: CV_BROWSER apunta a un binario no ejecutable: {override}")
        sys.exit(1)

    for path in BROWSER_CANDIDATES.get(sys.platform, []):
        if Path(path).is_file() and os.access(path, os.X_OK):
            return path

    for name in PATH_BINARIES:
        found = shutil.which(name)
        if found:
            return found

    return _playwright_chromium()


def _run_browser(browser_exe, html_file, output_path, extra_args=()):
    cmd = [
        browser_exe,
        "--headless=new",
        "--disable-gpu",
        f"--print-to-pdf={str(output_path)}",
        "--no-pdf-header-footer",
        *extra_args,
        html_file.as_uri()
    ]
    return subprocess.run(cmd, capture_output=True, text=True)


def _sandbox_blocked(stderr):
    text = (stderr or "").lower()
    return "sandbox" in text and ("no usable sandbox" in text or "suid sandbox" in text)


def export_pdf(output_filename="Gonzalo_Bartual_CV.pdf", compact=False):
    browser_exe = find_browser()
    if not browser_exe:
        print("Error: No se encontró ningún navegador compatible (Edge, Chrome o Chromium).")
        print("Puedes indicar uno manualmente con la variable de entorno CV_BROWSER.")
        sys.exit(1)

    html_file = Path("index.html").resolve()
    if not html_file.exists():
        print("Error: index.html no encontrado.")
        sys.exit(1)

    original_content = None
    if compact:
        original_content = html_file.read_text(encoding="utf-8")
        compact_content = original_content.replace('<body', '<body class="layout-compact"')
        html_file.write_text(compact_content, encoding="utf-8")
        if output_filename == "Gonzalo_Bartual_CV.pdf":
            output_filename = "Gonzalo_Bartual_CV_1Page.pdf"

    output_path = Path(output_filename).resolve()
    print(f"Exportando {html_file.name} a {output_path.name} usando {Path(browser_exe).name}...")

    try:
        result = _run_browser(browser_exe, html_file, output_path)

        # Ubuntu 23.10+ (y otras distros con AppArmor) restringen los user
        # namespaces sin privilegios, lo que rompe el sandbox de Chromium.
        # Solo en ese caso reintentamos sin sandbox.
        if result.returncode != 0 and _sandbox_blocked(result.stderr):
            print("Aviso: sandbox del navegador no disponible; reintentando con --no-sandbox.")
            output_path.unlink(missing_ok=True)
            result = _run_browser(browser_exe, html_file, output_path, ("--no-sandbox",))

        if result.returncode != 0:
            print(f"Error al generar el PDF (código {result.returncode}).")
            if result.stderr:
                print(result.stderr.strip())
            sys.exit(1)

        if not output_path.is_file():
            print("Error: el navegador terminó sin generar el PDF.")
            sys.exit(1)

        print(f"¡Éxito! PDF generado en: {output_path}")
    finally:
        if original_content is not None:
            html_file.write_text(original_content, encoding="utf-8")


if __name__ == "__main__":
    args = sys.argv[1:]
    compact_mode = any(arg in ("--compact", "--1page") for arg in args)
    # El nombre de salida es cualquier argumento que no sea un flag, sin importar
    # su posición (antes se ignoraba si el flag iba primero: `--1page out.pdf`).
    positional = [arg for arg in args if not arg.startswith("--")]
    out_name = positional[0] if positional else "Gonzalo_Bartual_CV.pdf"
    export_pdf(out_name, compact=compact_mode)
