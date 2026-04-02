# PDF Table Extraction Pipeline

This project extracts tables from a PDF file by converting a selected page into an image and then detecting table regions using computer vision (OpenCV). The detected tables are saved as separate image files, which can later be used for OCR or LLM-based data extraction.


## What this does

- Takes a PDF file
- Converts a chosen page into an image
- Detects large table-like regions in that image
- Saves each detected table as a separate image
- Optionally generates debug images to help you understand what the model is seeing



## Requirements


```bash
pip install pdf2image opencv-python pyyaml
```

