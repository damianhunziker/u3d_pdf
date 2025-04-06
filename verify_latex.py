#!/usr/bin/env python3
"""
LaTeX 3D PDF Verification Script

This script verifies that your LaTeX installation is correctly set up
for generating 3D PDFs with media9 package.
"""

import os
import sys
import subprocess
import logging
import tempfile

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_latex_installation():
    """Check if LaTeX is properly installed"""
    try:
        result = subprocess.run(['pdflatex', '--version'], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE,
                               text=True)
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            logger.info(f"LaTeX is installed: {version}")
            return True
        else:
            logger.error("LaTeX is not properly installed")
            return False
    except FileNotFoundError:
        logger.error("LaTeX (pdflatex) not found in PATH")
        return False

def check_media9_package():
    """Check if the media9 package is installed"""
    try:
        result = subprocess.run(['kpsewhich', 'media9.sty'], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE,
                               text=True)
        if result.returncode == 0 and result.stdout.strip():
            logger.info(f"media9 package found at: {result.stdout.strip()}")
            return True
        else:
            logger.error("media9 package not found")
            return False
    except FileNotFoundError:
        logger.error("kpsewhich command not found")
        return False

def check_ocgx2_package():
    """Check if the ocgx2 package is installed"""
    try:
        result = subprocess.run(['kpsewhich', 'ocgbase.sty'], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE,
                               text=True)
        if result.returncode == 0 and result.stdout.strip():
            logger.info(f"ocgx2 package found at: {result.stdout.strip()}")
            return True
        else:
            logger.error("ocgx2 package not found")
            return False
    except FileNotFoundError:
        logger.error("kpsewhich command not found")
        return False

def create_test_latex():
    """Create a minimal test LaTeX file"""
    with tempfile.TemporaryDirectory() as temp_dir:
        tex_file = os.path.join(temp_dir, "test.tex")
        
        with open(tex_file, 'w') as f:
            f.write(r"""\documentclass{article}
\usepackage{geometry}
\usepackage{media9}
\usepackage{hyperref}

\begin{document}
\title{LaTeX Media9 Test}
\author{Verification Script}
\maketitle

This is a test document to verify that LaTeX with media9 is working correctly.

\end{document}
""")
        
        logger.info(f"Created test LaTeX file: {tex_file}")
        
        # Try to compile it
        logger.info("Attempting to compile test LaTeX file...")
        result = subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_file], 
                               cwd=temp_dir,
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE,
                               text=True)
        
        if result.returncode == 0:
            pdf_file = os.path.join(temp_dir, "test.pdf")
            if os.path.exists(pdf_file):
                logger.info("Successfully compiled test LaTeX file")
                return True
            else:
                logger.error("Compilation did not produce a PDF file")
                return False
        else:
            logger.error("Failed to compile test LaTeX file")
            logger.error(f"Error: {result.stderr}")
            return False

def main():
    logger.info("Verifying LaTeX installation for 3D PDF generation...")
    
    # Check if LaTeX is installed
    if not check_latex_installation():
        logger.error("LaTeX is not properly installed. Please install LaTeX first.")
        return False
    
    # Check for required packages
    media9_ok = check_media9_package()
    ocgx2_ok = check_ocgx2_package()
    
    if not media9_ok or not ocgx2_ok:
        logger.error("Required LaTeX packages are missing.")
        if not media9_ok:
            logger.error("Please install media9 package: sudo tlmgr install media9")
        if not ocgx2_ok:
            logger.error("Please install ocgx2 package: sudo tlmgr install ocgx2")
        return False
    
    # Try to compile a test document
    if create_test_latex():
        logger.info("ALL CHECKS PASSED! Your LaTeX installation is correctly set up for 3D PDFs.")
        logger.info("You can now run:")
        logger.info("  python latex_3d_pdf.py ../obj_to_u3d/output/Skittle_3d.u3d pdf/skittle_3d.pdf")
        return True
    else:
        logger.error("There was a problem compiling a test LaTeX document.")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 