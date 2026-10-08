import sys
import subprocess
from pathlib import Path

EDGE_PATHS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
]

def find_browser():
    for p in EDGE_PATHS:
        if Path(p).exists():
            return p
    return None

def export_pdf(output_filename="Gonzalo_Bartual_CV.pdf", compact=False):
    browser_exe = find_browser()
    if not browser_exe:
        print("Error: No se encontró Microsoft Edge ni Google Chrome.")
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

    cmd = [
        browser_exe,
        "--headless=new",
        "--disable-gpu",
        f"--print-to-pdf={str(output_path)}",
        "--no-pdf-header-footer",
        html_file.as_uri()
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"¡Éxito! PDF generado en: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error al generar el PDF: {e}")
    finally:
        if original_content is not None:
            html_file.write_text(original_content, encoding="utf-8")

if __name__ == "__main__":
    compact_mode = "--compact" in sys.argv or "--1page" in sys.argv
    out_name = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "Gonzalo_Bartual_CV.pdf"
    export_pdf(out_name, compact=compact_mode)
