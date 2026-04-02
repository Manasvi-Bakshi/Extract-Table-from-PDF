import os
import yaml
import cv2
from pdf2image import convert_from_path


# ==============================
# CONFIG LOADER
# ==============================
def load_config(config_path="config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


# ==============================
# PDF → IMAGE
# ==============================
def pdf_to_image(config):
    pdf_cfg = config["pdf"]

    pages = convert_from_path(
        pdf_cfg["file_path"],
        dpi=pdf_cfg["dpi"],
        poppler_path=pdf_cfg["poppler_path"]
    )

    page_index = pdf_cfg["page_number"] - 1
    page_image = pages[page_index]

    return page_image


# ==============================
# IMAGE → TABLE DETECTION
# ==============================
def detect_tables(image, config):
    proc_cfg = config["processing"]

    img = cv2.cvtColor(
        cv2.imread(image) if isinstance(image, str) else cv2.cvtColor(
            cv2.imdecode(
                cv2.imencode('.png', image)[1], cv2.IMREAD_COLOR
            ), cv2.COLOR_BGR2RGB
        ),
        cv2.COLOR_BGR2RGB
    )

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV,
        proc_cfg["adaptive_block_size"],
        proc_cfg["adaptive_C"]
    )

    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    tables = []
    debug_img = img.copy()

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = w * h

        if area > proc_cfg["min_table_area"]:
            roi = img[y:y+h, x:x+w]
            tables.append((roi, (x, y, w, h)))

            # Draw debug box
            cv2.rectangle(debug_img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    return tables, thresh, debug_img


# ==============================
# SAVE OUTPUTS
# ==============================
def save_outputs(tables, thresh, debug_img, config):
    out_cfg = config["output"]
    save_dir = out_cfg["save_dir"]

    os.makedirs(save_dir, exist_ok=True)

    # Save tables
    for i, (roi, _) in enumerate(tables):
        cv2.imwrite(os.path.join(save_dir, f"table_{i+1}.png"), roi)

    # Debug outputs
    if out_cfg["debug"]:
        cv2.imwrite(os.path.join(save_dir, "debug_threshold.png"), thresh)
        cv2.imwrite(os.path.join(save_dir, "debug_boxes.png"), debug_img)


# ==============================
# MAIN PIPELINE
# ==============================
def main(config_path="config.yaml"):
    config = load_config(config_path)

    # Step 1: PDF → image
    page_image = pdf_to_image(config)

    # Save temp image for OpenCV
    temp_path = "temp_page.png"
    page_image.save(temp_path, "PNG")

    # Step 2: Detect tables
    tables, thresh, debug_img = detect_tables(temp_path, config)

    # Step 3: Save outputs
    save_outputs(tables, thresh, debug_img, config)

    print(f"Detected {len(tables)} table(s). Saved in '{config['output']['save_dir']}'.")


if __name__ == "__main__":
    main()