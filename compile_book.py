#!/usr/bin/env python3
"""
Script de compilación para generar el PDF del libro de Teoría de Grafos

Requisitos:
- pandoc >= 2.0
- LaTeX (texlive-latex-base, texlive-latex-extra)

Uso:
    python compile_book.py
"""

import subprocess
import sys
from pathlib import Path


def check_dependencies():
    """Verifica que pandoc y pdflatex estén instalados"""
    dependencies = {
        "pandoc": "--version",
        "pdflatex": "--version",
        "xelatex": "--version",
    }

    missing = []
    for cmd, flag in dependencies.items():
        try:
            subprocess.run([cmd, flag], capture_output=True, check=True)
            print(f"✓ {cmd} encontrado")
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing.append(cmd)
            print(f"✗ {cmd} no encontrado")

    if missing:
        print(f"\nError: Dependencias faltantes: {', '.join(missing)}")
        print("\nInstala las dependencias:")
        print(
            "  Ubuntu/Debian: sudo apt-get install pandoc texlive-latex-base texlive-latex-extra"
        )
        print("  macOS: brew install pandoc && brew install --cask mactex")
        return False

    return True


def compile_book():
    """Compila todos los capítulos en un solo PDF"""

    # Directorio raíz del proyecto
    root_dir = Path(__file__).parent
    capitulos_dir = root_dir / "capitulos"
    output_dir = root_dir / "output"
    output_dir.mkdir(exist_ok=True)

    # Orden de los capítulos
    chapters = [
        "01_fundamentos.md",
        "02_recorridos.md",
        "03_caminos_minimos.md",
        "04_arboles_expansion.md",
        "05_dags.md",
        "06_conectividad.md",
        "07_flujo_matching.md",
        "08_grafos_especiales.md",
        "09_tecnicas_avanzadas.md",
        "10_aplicaciones.md",
    ]

    # Verifica que todos los capítulos existan
    chapter_paths = []
    for chapter in chapters:
        path = capitulos_dir / chapter
        if not path.exists():
            print(f"⚠ Advertencia: {chapter} no encontrado, omitiendo...")
        else:
            chapter_paths.append(str(path))
            print(f"✓ Incluido: {chapter}")

    if not chapter_paths:
        print("Error: No se encontraron capítulos para compilar")
        return False

    # Archivo de salida
    output_pdf = output_dir / "graph_theory_book.pdf"

    # Metadata file
    metadata_file = output_dir / "metadata.yaml"
    metadata_content = r"""---
title: "Teoría de Grafos y Algoritmos Fundamentales"
subtitle: "Un enfoque práctico para desarrolladores y matemáticos"
author:
- Alejandro Lazaro Alfonso Yero
- "Colaboración Técnica: Gemini 3 Pro (AI)"
date: "2025"
lang: es-ES
documentclass: book
papersize: a4
fontsize: 11pt
geometry:
- margin=1in
toc: true
toc-depth: 2
numbersections: true
colorlinks: true
linkcolor: blue
urlcolor: blue
header-includes: |
  \usepackage{amsmath}
  \usepackage{amssymb}
  \usepackage{xcolor}
  \usepackage{fancyhdr}
  \pagestyle{fancy}
  \fancyhead{}
  \fancyhead[LE,RO]{\thepage}
  \fancyhead[RE]{\nouppercase{\leftmark}}
  \fancyhead[LO]{\nouppercase{\rightmark}}
  \fancyfoot{}
  \usepackage{fvextra}
  \fvset{breaklines=true, breakanywhere=true}
  \usepackage{fontspec}
  \setmainfont{DejaVu Serif}
  \setsansfont{DejaVu Sans}
  \setmonofont{DejaVu Sans Mono}
---
"""

    metadata_file.write_text(metadata_content)

    # Comando de pandoc
    cmd = [
        "pandoc",
        str(metadata_file),
        *chapter_paths,
        "-o",
        str(output_pdf),
        "--pdf-engine=xelatex",
        "--highlight-style=tango",
        "-V",
        "geometry:margin=1in",
    ]

    print(f"\n{'=' * 60}")
    print("Compilando libro...")
    print(f"{'=' * 60}\n")

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"\n✓ Compilación exitosa!")
        print(f"✓ PDF generado: {output_pdf}")
        print(f"\nTamaño: {output_pdf.stat().st_size / 1024:.1f} KB")
        return True

    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error durante la compilación:")
        print(e.stderr)
        return False


def main():
    """Función principal"""
    print("=" * 60)
    print("Compilador del Libro de Teoría de Grafos")
    print("=" * 60)
    print()

    # Verificar dependencias
    if not check_dependencies():
        sys.exit(1)

    print()

    # Compilar
    if compile_book():
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
