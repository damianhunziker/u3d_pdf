# Command Line Interface for 3D PDF Generation

This document provides instructions for using the command line tools to convert U3D files to 3D PDFs using LaTeX.

## Single File Conversion

To convert a single U3D file to a 3D PDF:

```bash
python latex_3d_pdf.py path/to/input.u3d path/to/output.pdf [--title "PDF Title"]
```

Example:
```bash
python latex_3d_pdf.py ../obj_to_u3d/output/Skittle_3d.u3d pdf/skittle_3d.pdf --title "Skittle 3D Model"
```

## Batch Conversion

To convert multiple U3D files at once:

```bash
python batch_convert_latex.py --source-dir DIR --output-dir DIR [--template FILE]
```

Example:
```bash
python batch_convert_latex.py --source-dir ../obj_to_u3d/output --output-dir pdf
```

## Check Dependencies

To verify that your LaTeX installation has all required packages:

```bash
python verify_latex.py
```

This will check for:
- LaTeX (pdflatex) installation
- media9 package
- ocgx2 package
- Ability to compile a test document

## Viewing 3D PDFs

To open a PDF in Adobe Acrobat Reader (recommended for 3D content):

```bash
python view_pdf.py path/to/file.pdf
```

Example:
```bash
python view_pdf.py pdf/skittle_3d.pdf
```

## Direct LaTeX Usage

You can also use LaTeX directly to create 3D PDFs:

1. Edit the `example.tex` file to customize the appearance and path to your U3D file
2. Compile with:
```bash
pdflatex example.tex
```

## Common Issues

### Missing LaTeX

If LaTeX is not installed or not in your PATH:

```bash
# For macOS
brew install --cask basictex

# Add to PATH
export PATH=$PATH:/Library/TeX/texbin
```

### Missing Packages

If the media9 or ocgx2 packages are missing:

```bash
sudo tlmgr update --self
sudo tlmgr install media9 ocgx2
```

### PDF Doesn't Show 3D Content

Make sure you:
1. Open the PDF in Adobe Acrobat Reader (not Preview, Chrome, etc.)
2. Click "Enable 3D content" when prompted
3. Click on the 3D viewport area to activate the model 