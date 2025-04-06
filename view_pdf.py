#!/usr/bin/env python3
"""
PDF Viewer Script

This script attempts to open a PDF file in Adobe Acrobat Reader.
If Acrobat Reader is not found, it will try to open the PDF with the default PDF viewer.

Usage:
    python view_pdf.py path/to/file.pdf

Example:
    python view_pdf.py pdf/Skittle_3d.pdf
"""

import os
import sys
import subprocess
import platform
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def find_acrobat_reader():
    """Try to find Adobe Acrobat Reader on the system"""
    system = platform.system()
    
    if system == 'Darwin':  # macOS
        # Common Acrobat Reader locations on macOS
        possible_paths = [
            '/Applications/Adobe Acrobat Reader.app/Contents/MacOS/AdobeReader',
            '/Applications/Adobe Acrobat Reader DC.app/Contents/MacOS/AdobeReader',
            '/Applications/Adobe Acrobat Reader.app/Contents/MacOS/Adobe Acrobat Reader',
            '/Applications/Adobe Acrobat Reader DC.app/Contents/MacOS/Adobe Acrobat Reader DC'
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                logger.info(f"Found Acrobat Reader at: {path}")
                return path
                
        # Try using the 'open' command with the specific app
        return 'open -a "Adobe Acrobat Reader"'
        
    elif system == 'Windows':
        # Common Acrobat Reader locations on Windows
        possible_paths = [
            r'C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe',
            r'C:\Program Files\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe',
            r'C:\Program Files (x86)\Adobe\Acrobat Reader\Reader\AcroRd32.exe',
            r'C:\Program Files\Adobe\Acrobat Reader\Reader\AcroRd32.exe'
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                logger.info(f"Found Acrobat Reader at: {path}")
                return path
                
        return None
        
    elif system == 'Linux':
        # Try to find acroread on Linux
        try:
            result = subprocess.run(['which', 'acroread'], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE, 
                                  text=True)
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except Exception:
            pass
            
        return None
    
    return None

def open_pdf(pdf_path):
    """Open a PDF file with Adobe Acrobat Reader if available"""
    if not os.path.exists(pdf_path):
        logger.error(f"PDF file not found: {pdf_path}")
        return False
    
    # First try to find Adobe Acrobat Reader
    acrobat = find_acrobat_reader()
    
    if acrobat:
        try:
            if platform.system() == 'Darwin' and acrobat.startswith('open'):
                # Special case for macOS using 'open -a'
                command = f'{acrobat} "{pdf_path}"'
                logger.info(f"Opening PDF with command: {command}")
                os.system(command)
            else:
                # Normal case - direct path to executable
                logger.info(f"Opening PDF with Acrobat Reader: {pdf_path}")
                subprocess.Popen([acrobat, pdf_path])
            return True
        except Exception as e:
            logger.error(f"Error opening PDF with Acrobat Reader: {str(e)}")
    
    # Fall back to system default PDF viewer
    try:
        logger.info("Acrobat Reader not found, trying system default PDF viewer")
        
        if platform.system() == 'Darwin':  # macOS
            subprocess.Popen(['open', pdf_path])
        elif platform.system() == 'Windows':  # Windows
            os.startfile(pdf_path)
        else:  # Linux
            subprocess.Popen(['xdg-open', pdf_path])
            
        logger.warning("Note: 3D content may not display correctly in non-Acrobat PDF viewers")
        return True
    except Exception as e:
        logger.error(f"Error opening PDF with default viewer: {str(e)}")
        return False

def main():
    if len(sys.argv) < 2:
        logger.error("Please provide a PDF file path")
        logger.info("Usage: python view_pdf.py path/to/file.pdf")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    success = open_pdf(pdf_path)
    
    if not success:
        logger.error("Failed to open the PDF file")
        sys.exit(1)
    
    logger.info("Remember: 3D content requires Adobe Acrobat Reader to view properly")

if __name__ == "__main__":
    main() 