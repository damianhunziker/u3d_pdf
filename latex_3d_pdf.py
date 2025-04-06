#!/usr/bin/env python3
"""
LaTeX 3D PDF Generator

This script creates 3D PDFs from U3D files using LaTeX with the media9 package.
It generates a LaTeX file, compiles it with pdflatex, and produces a PDF with
an embedded interactive 3D model.

Requirements:
- Python 3.6+
- A LaTeX distribution with the media9 package (MacTeX, TeX Live, or MiKTeX)
- U3D files to embed

Usage:
    python latex_3d_pdf.py input.u3d [output.pdf] [--title "PDF Title"] [--template TEMPLATE]

Example:
    python latex_3d_pdf.py ../obj_to_u3d/output/Skittle_3d.u3d pdf/skittle_model.pdf --title "Skittle 3D Model"
"""

import os
import sys
import argparse
import logging
import tempfile
import subprocess
import shutil
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Default LaTeX template for embedding U3D models
DEFAULT_TEMPLATE = r"""
\documentclass{article}
\usepackage[margin=1in]{geometry}
\usepackage{media9}
\usepackage{hyperref}
\usepackage{color}

\title{__TITLE__}
\author{3D PDF Generator}
\date{\today}

\begin{document}

\maketitle

\begin{center}
\fbox{
    \includemedia[
        label=model,
        width=0.9\textwidth,
        height=0.7\textheight,
        activate=pageopen,
        3Dtoolbar,
        3Dmenu,
        3Droo=200,
        3Dcoo=0 0 0,
        3Dlights=CAD,
        3Drender=Solid,
    ]{\textcolor{blue}{Click to activate the 3D model}}{__MODEL_PATH__}
}
\end{center}

\vspace{1cm}
\begin{center}
\textit{This interactive 3D PDF was created using media9 and \LaTeX.\\
Use your mouse to rotate, scroll to zoom, and right-click for more options.}
\end{center}

\end{document}
"""

def find_pdflatex():
    """Find the pdflatex executable on the system"""
    # Try to find pdflatex in common locations
    possible_paths = [
        "pdflatex",  # If it's in PATH
        "/Library/TeX/texbin/pdflatex",  # Standard MacTeX location
        "/usr/local/texlive/20*/bin/*/pdflatex",  # TeX Live on Unix/Linux
        "/usr/bin/pdflatex",  # Linux
        "C:/texlive/20*/bin/win32/pdflatex.exe",  # TeX Live on Windows
        "C:/Program Files/MiKTeX*/miktex/bin/pdflatex.exe"  # MiKTeX on Windows
    ]
    
    # Try executing pdflatex and see if it works
    for path in possible_paths:
        if '*' in path:
            # Handle wildcards using glob
            import glob
            for matched_path in sorted(glob.glob(path), reverse=True):
                try:
                    version = subprocess.check_output([matched_path, "--version"], 
                                                    stderr=subprocess.STDOUT, 
                                                    universal_newlines=True)
                    logger.info(f"Found pdflatex at {matched_path}")
                    return matched_path
                except (subprocess.SubprocessError, FileNotFoundError):
                    continue
        else:
            try:
                version = subprocess.check_output([path, "--version"], 
                                                stderr=subprocess.STDOUT, 
                                                universal_newlines=True)
                logger.info(f"Found pdflatex at {path}")
                return path
            except (subprocess.SubprocessError, FileNotFoundError):
                continue
    
    logger.error("pdflatex not found. Please install LaTeX (MacTeX, TeX Live, or MiKTeX)")
    return None

def check_media9_package():
    """Check if the media9 LaTeX package is installed"""
    try:
        # Use kpsewhich to check if media9.sty exists
        result = subprocess.run(["kpsewhich", "media9.sty"], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE, 
                               universal_newlines=True)
        
        if result.stdout.strip():
            logger.info(f"Found media9 package at: {result.stdout.strip()}")
            return True
        else:
            logger.warning("media9 LaTeX package not found.")
            logger.warning("Please install it using your TeX package manager:")
            logger.warning("  tlmgr install media9")
            return False
    except (subprocess.SubprocessError, FileNotFoundError):
        logger.warning("Could not check for media9 package. It may not be installed.")
        return False

def create_latex_file(u3d_path, template=DEFAULT_TEMPLATE, title="3D Model"):
    """Create a LaTeX file with the embedded U3D model"""
    # Get absolute path for the U3D file (LaTeX needs this)
    u3d_abs_path = os.path.abspath(u3d_path)
    
    # Replace placeholders in the template
    latex_content = template.replace("__TITLE__", title)
    latex_content = latex_content.replace("__MODEL_PATH__", u3d_abs_path)
    
    # Create a temporary directory for LaTeX compilation
    temp_dir = tempfile.mkdtemp()
    latex_file = os.path.join(temp_dir, "model.tex")
    
    # Write the LaTeX file
    with open(latex_file, "w") as f:
        f.write(latex_content)
    
    logger.info(f"Created LaTeX file: {latex_file}")
    return latex_file, temp_dir

def compile_latex(latex_file, output_pdf):
    """Compile the LaTeX file to create a PDF"""
    # Find pdflatex
    pdflatex = find_pdflatex()
    if not pdflatex:
        return False
    
    # Get the directory containing the LaTeX file
    latex_dir = os.path.dirname(latex_file)
    
    try:
        # Run pdflatex twice to ensure all references are resolved
        for i in range(2):
            logger.info(f"Running pdflatex (pass {i+1}/2)...")
            result = subprocess.run([pdflatex, 
                                   "-interaction=nonstopmode", 
                                   "-output-directory=" + latex_dir,
                                   latex_file], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.STDOUT, 
                                   universal_newlines=True)
            
            # Check if compilation was successful
            if result.returncode != 0:
                logger.error("LaTeX compilation failed")
                logger.error(result.stdout)
                return False
        
        # Get the output PDF path from the LaTeX compilation
        compiled_pdf = os.path.splitext(latex_file)[0] + ".pdf"
        
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_pdf)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Copy the compiled PDF to the desired output location
        shutil.copy2(compiled_pdf, output_pdf)
        logger.info(f"Successfully created 3D PDF: {output_pdf}")
        
        return True
    
    except Exception as e:
        logger.error(f"Error during LaTeX compilation: {str(e)}")
        return False
    finally:
        # Clean up LaTeX auxiliary files but keep the temp directory
        for ext in ['.aux', '.log', '.out']:
            aux_file = os.path.splitext(latex_file)[0] + ext
            if os.path.exists(aux_file):
                os.unlink(aux_file)

def generate_3d_pdf(u3d_file, output_pdf, title=None, template=None):
    """Generate a 3D PDF from a U3D file using LaTeX"""
    # Verify the U3D file exists
    if not os.path.exists(u3d_file):
        logger.error(f"U3D file not found: {u3d_file}")
        return False
    
    # Check if media9 package is available
    check_media9_package()
    
    # Use default title if not provided
    if not title:
        title = os.path.splitext(os.path.basename(u3d_file))[0].replace('_', ' ').title()
    
    # Use default template if not provided
    if not template:
        template_content = DEFAULT_TEMPLATE
    else:
        # Read template from file
        try:
            with open(template, 'r') as f:
                template_content = f.read()
        except Exception as e:
            logger.error(f"Error reading template file: {str(e)}")
            logger.info("Using default template instead")
            template_content = DEFAULT_TEMPLATE
    
    # Create LaTeX file
    latex_file, temp_dir = create_latex_file(u3d_file, template_content, title)
    
    try:
        # Compile LaTeX file
        success = compile_latex(latex_file, output_pdf)
        
        if success:
            logger.info(f"3D PDF successfully created: {output_pdf}")
            logger.info("View the PDF in Adobe Acrobat Reader to see the 3D model")
        else:
            logger.error("Failed to create 3D PDF")
        
        return success
    
    finally:
        # Clean up temporary directory after we're done
        try:
            shutil.rmtree(temp_dir)
        except Exception as e:
            logger.warning(f"Failed to clean up temporary directory: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Create 3D PDFs from U3D files using LaTeX")
    parser.add_argument("u3d_file", nargs='?', help="Input U3D file")
    parser.add_argument("output_pdf", nargs='?', help="Output PDF file (optional)")
    parser.add_argument("--title", help="Title for the PDF document")
    parser.add_argument("--template", help="Custom LaTeX template file")
    parser.add_argument("--check-deps", action="store_true", 
                       help="Check for required dependencies (pdflatex and media9)")
    
    args = parser.parse_args()
    
    # Just check dependencies if requested
    if args.check_deps:
        pdflatex = find_pdflatex()
        has_media9 = check_media9_package()
        if pdflatex and has_media9:
            logger.info("All dependencies are satisfied")
            return True
        else:
            logger.error("Missing dependencies")
            return False
    
    # Require u3d_file if we're not just checking dependencies
    if not args.u3d_file:
        parser.error("the following arguments are required: u3d_file")
    
    # Handle paths
    u3d_path = args.u3d_file
    
    # If output_pdf is not specified, create it from the input name
    if not args.output_pdf:
        u3d_base = os.path.splitext(os.path.basename(u3d_path))[0]
        pdf_path = os.path.join("pdf", f"{u3d_base}.pdf")
    else:
        pdf_path = args.output_pdf
    
    # Generate the 3D PDF
    success = generate_3d_pdf(u3d_path, pdf_path, args.title, args.template)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main() 