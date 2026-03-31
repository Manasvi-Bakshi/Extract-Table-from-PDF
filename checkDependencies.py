import importlib

REQUIRED_PACKAGES = [
    "pdfplumber",     # for table extraction from text-based PDFs
    "pdfminer",       # or "pdfminer.six" depending on how it's installed
    "docling",        # document understanding (if allowed/installed)
    "pandas",
]

OPTIONAL_PACKAGES = [
    "pytesseract",
    "opencv",         # sometimes "cv2" module name is under "opencv-python"
    "cv2",
    "pdf2image",
]

def check_package(name):
    try:
        importlib.import_module(name)
        print(f"[OK]    {name} is installed")
        return True
    except ModuleNotFoundError:
        print(f"[MISS]  {name} is NOT installed")
        return False
    except Exception as e:
        print(f"[ERR]   {name} import error: {e}")
        return False

def main():
    print("=== Required packages ===")
    for pkg in REQUIRED_PACKAGES:
        check_package(pkg)

    print("\n=== Optional OCR-related packages ===")
    for pkg in OPTIONAL_PACKAGES:
        check_package(pkg)

    print("\nIf any required packages show as [MISS], they still need to be installed.")
    print("If OCR-related packages are missing, scanned PDFs will not be handled automatically.")

if __name__ == "__main__":
    main()