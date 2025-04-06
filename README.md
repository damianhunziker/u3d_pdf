# LaTeX-based 3D PDF Generator

This tool creates interactive 3D PDFs from U3D files using LaTeX with the media9 package. This method consistently produces PDFs that work correctly in Adobe Acrobat Reader, unlike some Python-only solutions.

## Why Use LaTeX?

LaTeX with the media9 package is the most reliable way to create 3D PDFs that:
- Work consistently in Adobe Acrobat Reader
- Display security prompts properly
- Support all 3D model interaction features
- Can be customized extensively

## Requirements

- **LaTeX Distribution**: TeX Live or MiKTeX
  - For macOS: MacTeX (`brew install --cask mactex`)
  - For Windows: MiKTeX or TeX Live
  - For Linux: TeX Live (`sudo apt install texlive-full`)
  
- **media9 Package**: Modern LaTeX package for embedding 3D content
  - For TeX Live: `tlmgr install media9`
  - For MiKTeX: Use the MiKTeX Console to install the media9 package
  
- **Python 3.6+**: For running the helper scripts
  - Required packages: None (uses standard library only)

- **U3D Files**: 3D models in Universal 3D format 
  - Can be created using our PyMeshLab script (see `../obj_to_u3d/`)

## Installation

1. **Install a TeX distribution**:
   ```bash
   # For macOS
   brew install --cask mactex
   
   # For Linux
   sudo apt install texlive-full
   
   # For Windows: Download and install MiKTeX or TeX Live
   ```

2. **Install the media9 package** (if not already included in your TeX distribution):
   ```bash
   # For TeX Live
   tlmgr update --self
   tlmgr install media9
   
   # For MiKTeX: Use the MiKTeX Console
   ```

3. **Add LaTeX to your PATH** (if not automatically added):
   ```bash
   # For macOS
   export PATH=$PATH:/Library/TeX/texbin
   
   # For Linux/Windows: The installation usually adds it to PATH
   ```

4. **Verify the installation**:
   ```bash
   # Check if pdflatex is available
   pdflatex --version
   
   # Check if the media9 package is installed
   kpsewhich media9.sty
   ```

## Usage

### Option 1: Using the Python Helper Scripts

1. **Single File Conversion**:
   ```bash
   python latex_3d_pdf.py ../obj_to_u3d/output/Skittle_3d.u3d pdf/skittle_model.pdf --title "Skittle 3D Model"
   ```

2. **Batch Conversion**:
   ```bash
   python batch_convert_latex.py --source-dir ../obj_to_u3d/output --output-dir pdf
   ```

3. **Check Dependencies**:
   ```bash
   python latex_3d_pdf.py --check-deps
   ```

### Option 2: Direct LaTeX Usage

1. Edit the provided `example.tex` file:
   - Replace the U3D file path
   - Adjust the title and other parameters as needed

2. Compile the LaTeX file:
   ```bash
   pdflatex example.tex
   ```

3. The resulting PDF will contain your 3D model.

## Customizing the 3D View

You can adjust various parameters in the LaTeX file to customize how the 3D model appears:

- **3Droo**: Initial distance from the camera to the model (zoom level)
- **3Dcoo**: Center of orbit coordinates (target point of camera)
- **3Dc2c**: Camera-to-center vector (initial view direction)
- **3Dlights**: Lighting model (CAD, Headlamp, Hard, Red, etc.)
- **3Drender**: Rendering mode (Solid, Wireframe, Points, etc.)
- **3Dbg**: Background color (R G B values between 0-1)

For example:
```latex
\includemedia[
    label=model,
    width=0.9\textwidth,
    height=0.7\textheight,
    activate=pageopen,
    3Dtoolbar,
    3Dmenu,
    3Droo=200,         % Initial distance to model
    3Dcoo=0 0 0,       % Target point of camera
    3Dc2c=0 0 1,       % Camera direction
    3Dlights=CAD,      % Lighting model
    3Drender=Solid,    % Rendering style
    3Dbg=1 1 1,        % Background color (white)
]{\textcolor{blue}{Click to activate the 3D model}}{path/to/model.u3d}
```

## Viewing 3D PDFs

The generated PDFs require Adobe Acrobat Reader to view the 3D content. Most other PDF viewers (including browsers, Preview on macOS, etc.) will not display the interactive 3D model.

When opening the PDF in Acrobat Reader:
1. You'll see a security prompt asking to "Enable 3D content" - click to allow it
2. Click on the framed area to activate the 3D view
3. Use your mouse to rotate the model, scroll to zoom, and right-click for additional view options

## Troubleshooting

- **LaTeX Not Found**: Ensure pdflatex is in your PATH
  ```bash
  export PATH=$PATH:/Library/TeX/texbin  # For macOS
  ```

- **media9 Package Missing**: Install it using your package manager
  ```bash
  tlmgr install media9
  ```

- **Compilation Errors**: Check the LaTeX log file for detailed error messages
  ```bash
  cat example.log
  ```

- **3D Model Not Showing**: Verify that:
  - You're using Adobe Acrobat Reader (not Preview or other PDF viewers)
  - The U3D file is valid (try a different U3D file if unsure)
  - You've allowed the security prompt to enable 3D content # u3d_pdf
