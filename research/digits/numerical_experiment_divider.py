import cv2
import os

input_folder = "" # Path to the folder containing the scanned sheets of the numerical experiment
output_base_folder  = "output_windows_american_en"

input_folder_lines = "output_windows_american_en" # Path to the folder containing the individual lines
output_folder_lines  = "output_windows_american_en_after"

os.makedirs(output_base_folder, exist_ok=True)
def create_output_folder_structure(input_folder, output_folder):
    for root, dirs, files in os.walk(input_folder):
        for dir in dirs:
            path_structure = os.path.join(output_folder, os.path.relpath(os.path.join(root, dir), input_folder))
            os.makedirs(path_structure, exist_ok=True)

def ensure_line_folders(output_base_folder, page_num, num_lines):
    for line_num in range(1, num_lines + 1):
        line_folder = os.path.join(output_base_folder, f"page{page_num}_{line_num}")
        if not os.path.exists(line_folder):
            os.makedirs(line_folder)

# A function that divides the scanned sheets of a numerical experiment into individual lines, which
# are saved in separate folders

def process_pages(input_folder, output_base_folder, min_width=100, min_ratio=2, margin=15, min_height = 100): #
    num_pages = 5
    image_files = [f for f in os.listdir(input_folder) if f.endswith('.jpg') or f.endswith('.png')]

    for i in range(0, len(image_files)):
        page_number = (i % num_pages) + 1

        if page_number == 1:
            num_lines = 6  # Number of lines on the first page
        elif page_number == 2:
            num_lines = 14  # Number of lines on the second page
        elif page_number == 3:
            num_lines = 19  # Number of lines on the third page
        elif page_number == 4:
            num_lines = 25  # Number of lines on the fourth page
        elif page_number == 5:
            num_lines = 22  # Number of lines on page five
        else:
            continue

        ensure_line_folders(output_base_folder, page_number, num_lines)

        image_path = os.path.join(input_folder, image_files[i])
        img = cv2.imread(image_path)

        if img is None:
            print(f"Failed to load image: {image_path}")
            continue

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        _, thresh = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY_INV)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        line_count = 1

        contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[1])

        for idx, contour in enumerate(contours):
            x, y, w, h = cv2.boundingRect(contour)

            if w > min_width and w / h > min_ratio and min_height < h:
                if line_count > num_lines:
                    break

                x_margin = max(x - margin, 0)
                y_margin = max(y - margin, 0)
                w_margin = min(x + w + margin, img.shape[1]) - x_margin
                h_margin = min(y + h + margin, img.shape[0]) - y_margin

                window = img[y_margin:y_margin + h_margin, x_margin:x_margin + w_margin]

                line_folder = os.path.join(output_base_folder, f"page{page_number}_{line_count}")
                output_path = os.path.join(line_folder, f"window_{i + 1}_line_{line_count}.png")
                cv2.imwrite(output_path, window)

                line_count += 1

    cv2.destroyAllWindows()

# A function that divides the lines into individual windows (single digit)
def process_images(input_folder, output_folder):
    print(os.path.basename(input_folder))
    if os.path.basename(input_folder).endswith('_1'):
        window_size = 55
        margin = 5
    else:
        window_size = 80
        margin = 10
    print(f"Window size : {window_size}")
    image_files = [f for f in os.listdir(input_folder) if f.endswith('.jpg') or f.endswith('.png')]
    person_number = 0
    for i in range(0, len(image_files)):

        image_path = os.path.join(input_folder, image_files[i])
        img = cv2.imread(image_path)

        if img is None:
            print(f"Failed to load image: {image_path}")
            continue

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        _, thresh = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY_INV)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 10))
        morphed = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

        contours, _ = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])

        for idx, contour in enumerate(contours):
            x, y, w, h = cv2.boundingRect(contour)

            if h > 80 and w < h:
                x_margin = max(x + margin, 0)
                y_margin = max(y + margin, 0)
                w_margin = min(x + w + margin + window_size, img.shape[1]) - x_margin
                h_margin = min(y + h, img.shape[0]) - y_margin - margin

                if w_margin > 30:
                    window = img[y_margin:y_margin + h_margin, x_margin:x_margin + w_margin]
                    output_path = os.path.join(output_folder, f"american_window_pl_{person_number}_{idx}.png")
                    cv2.imwrite(output_path, window)
                    print(f"Saved: {output_path}")
        person_number = person_number + 1
    cv2.destroyAllWindows()

def process_all_folders(input_folder, output_folder):
    create_output_folder_structure(input_folder, output_folder)

    for root, dirs, files in os.walk(input_folder):
        relative_path = os.path.relpath(root, input_folder)
        current_output_folder = os.path.join(output_folder, relative_path)

        process_images(root, current_output_folder)

process_all_folders(input_folder_lines, output_folder_lines)

# process_pages(input_folder, output_base_folder, min_width=200, min_ratio=2, margin=15, min_height = 100)
# process_lines(input_folder_lines, output_folder_lines, min_height=20, margin=5)
