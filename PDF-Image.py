from pdf2image import convert_from_path

# Replace with the actual path where you unzipped Poppler
poppler_path = r"C:\poppler-25.12.0\Library\bin"

pages = convert_from_path(
    "AG300DYNA27C Certificato del 02-02-2026 1.pdf",
    dpi=300,
    poppler_path=poppler_path
)

page_image = pages[1]  # second page
page_image.save("page2.png", "PNG")
