#!/usr/bin/env python3
"""
Batch U3D to PDF Converter (LaTeX Method)

This script batch converts U3D files to 3D PDFs using LaTeX with the media9 package.
It processes all U3D files in a directory and creates PDFs that will work correctly
in Adobe Acrobat Reader.

Usage:
    python batch_convert_latex.py [--source-dir DIR] [--output-dir DIR] [--template FILE]

Example:
    python batch_convert_latex.py --source-dir ../obj_to_u3d/output --output-dir pdf
"""

import os
import sys
import argparse
import logging
import glob
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import the generate_3d_pdf function from our module
try:
    from latex_3d_pdf import generate_3d_pdf, check_media9_package, find_pdflatex
except ImportError:
    logger.error("Could not import latex_3d_pdf module. Make sure latex_3d_pdf.py is in the same directory.")
    sys.exit(1)

def find_u3d_files(source_dir):
    """Find all U3D files in the source directory"""
    if not os.path.exists(source_dir):
        logger.error(f"Source directory not found: {source_dir}")
        return []
    
    u3d_files = glob.glob(os.path.join(source_dir, "*.u3d"))
    logger.info(f"Found {len(u3d_files)} U3D files in {source_dir}")
    
    return u3d_files

def check_u3d_file(u3d_file):
    """Check if a U3D file appears to be valid"""
    # Verify file exists
    if not os.path.exists(u3d_file):
        logger.error(f"U3D file not found: {u3d_file}")
        return False
    
    # Check file size
    size = os.path.getsize(u3d_file)
    if size < 100:
        logger.warning(f"U3D file {os.path.basename(u3d_file)} is suspiciously small ({size} bytes), may not be valid")
        return False
    
    # Check file header
    try:
        with open(u3d_file, 'rb') as f:
            header = f.read(4)
            if header != b'U3D\x00':
                logger.warning(f"U3D file {os.path.basename(u3d_file)} has invalid header: {header} (should be 'U3D\\x00')")
                return False
    except Exception as e:
        logger.error(f"Error reading U3D file {u3d_file}: {str(e)}")
        return False
    
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    pdflatex = find_pdflatex()
    media9 = check_media9_package()
    
    if pdflatex and media9:
        logger.info("All required dependencies are installed")
        return True
    
    if not pdflatex:
        logger.error("pdflatex not found. Please install LaTeX (MacTeX, TeX Live, or MiKTeX)")
        logger.error("For macOS: brew install --cask mactex")
        logger.error("For Linux: sudo apt install texlive-full")
        logger.error("For Windows: Download and install MiKTeX or TeX Live")
    
    if not media9:
        logger.error("media9 LaTeX package not found.")
        logger.error("Please install it using your TeX package manager:")
        logger.error("  tlmgr install media9")
    
    return False

def process_u3d_files(u3d_files, output_dir, template=None):
    """Process a list of U3D files and convert them to 3D PDFs using LaTeX"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logger.info(f"Created output directory: {output_dir}")
    
    results = []
    
    for u3d_file in u3d_files:
        # First check if the U3D file is valid
        if not check_u3d_file(u3d_file):
            logger.warning(f"Skipping invalid U3D file: {u3d_file}")
            results.append({
                'u3d_file': u3d_file,
                'pdf_file': None,
                'success': False,
                'reason': 'Invalid U3D file'
            })
            continue
        
        # Get the base filename without extension
        base_name = os.path.splitext(os.path.basename(u3d_file))[0]
        
        # Create output PDF path
        pdf_file = os.path.join(output_dir, f"{base_name}.pdf")
        
        # Title for the PDF (use the base filename with spaces instead of underscores)
        title = base_name.replace('_', ' ').title()
        
        logger.info(f"Converting {u3d_file} to {pdf_file}")
        
        # Convert the U3D file to PDF using LaTeX
        success = generate_3d_pdf(u3d_file, pdf_file, title, template)
        
        results.append({
            'u3d_file': u3d_file,
            'pdf_file': pdf_file,
            'success': success,
            'reason': None if success else 'LaTeX compilation failed'
        })
    
    return results

def summarize_results(results):
    """Summarize the conversion results"""
    if not results:
        logger.warning("No files were processed")
        return
    
    success_count = sum(1 for r in results if r['success'])
    total_count = len(results)
    
    logger.info(f"Conversion complete: {success_count}/{total_count} files successfully converted")
    
    if success_count < total_count:
        logger.warning("Some conversions failed:")
        for r in results:
            if not r['success']:
                logger.warning(f"Failed: {r['u3d_file']} - {r['reason']}")
    
    if success_count > 0:
        logger.info("Successfully converted files:")
        for r in results:
            if r['success']:
                logger.info(f"Success: {r['pdf_file']}")

def main():
    parser = argparse.ArgumentParser(description="Batch convert U3D files to 3D PDFs using LaTeX")
    parser.add_argument("--source-dir", default="../obj_to_u3d/output", 
                        help="Directory containing U3D files (default: ../obj_to_u3d/output)")
    parser.add_argument("--output-dir", default="pdf", 
                        help="Directory for output PDF files (default: pdf)")
    parser.add_argument("--template", 
                        help="Custom LaTeX template file")
    parser.add_argument("--check-deps", action="store_true",
                        help="Check for required dependencies before running")
    
    args = parser.parse_args()
    
    # Check dependencies if requested
    if args.check_deps or True:  # Always check dependencies
        if not check_dependencies():
            logger.error("Missing required dependencies. Exiting.")
            sys.exit(1)
    
    # Find U3D files
    u3d_files = find_u3d_files(args.source_dir)
    
    if not u3d_files:
        logger.error("No U3D files found. Exiting.")
        sys.exit(1)
    
    # Process the files
    results = process_u3d_files(u3d_files, args.output_dir, args.template)
    
    # Summarize the results
    summarize_results(results)
    
    # Exit with error code if any conversion failed
    if not all(r['success'] for r in results):
        sys.exit(1)

if __name__ == "__main__":
    main() 