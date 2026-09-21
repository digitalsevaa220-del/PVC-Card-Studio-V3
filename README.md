# PVC Card Studio V3

Windows desktop PVC-card layout and printing preparation application.

## Features
- CR80 PVC card preset (85.60 × 53.98 mm)
- Custom card size and DPI
- Front/back design
- Text, photo, rectangle, QR and barcode elements
- Import PDF, JPG/JPEG, PNG, BMP, WEBP, TIFF
- Import CSV/TXT/JSON and DOCX
- Batch records from CSV/Excel-compatible data
- Export PNG/JPG/PDF
- Print-ready PDF generation
- Printer X/Y calibration offsets
- Save/load `.pcstudio` projects

This build is intended for authorized documents and user-provided content.

## Run on Windows
Python 3.11+ is recommended.

```bat
python -m pip install -r requirements.txt
python main.py
```

## Build Windows EXE
Use `build\build_windows.bat`.

## Cloud build
The `.github/workflows/build-windows.yml` workflow builds the Windows installer on a GitHub-hosted Windows machine.
