import cv2
from PIL import Image
from PIL import ExifTags
import argparse
import numpy as np
from pathlib import Path

parser = argparse.ArgumentParser(
    description="Show image in a window"
)

parser.add_argument(
    "image",
    help="Path to image file"
)

args = parser.parse_args()

image_path = Path(args.image)

if not image_path.exists():
    print("File does not exist")

elif not image_path.is_file():
    print("Path is not a file")

else:
    print("File exists")

    image = cv2.imread(str(image_path))

    pil_image = Image.open(image_path)

    if image is None:
        print("File is not a valid image")

    else:
        print("Image loaded successfully")

        height, width = image.shape[:2]

        if image.ndim == 3:
            channels = image.shape[2]
        else:
            channels = 1

        aspect_ratio = width / height

        bytes_per_channel = image.itemsize
        bytes_per_pixel = bytes_per_channel * channels

        is_color = image.ndim == 3

        min_value = image.min()
        max_value = image.max()
        mean_value = image.mean()

        image_format = pil_image.format
        image_mode = pil_image.mode

        file_size = image_path.stat().st_size

        if file_size < 1024:
            file_size_text = f"{file_size} B"
        elif file_size < 1024 * 1024:
            file_size_text = f"{file_size / 1024:.2f} KB"
        else:
            file_size_text = f"{file_size / (1024 * 1024):.2f} MB"
        
        extension = image_path.suffix

        absolute_path = image_path.resolve()

        frame_count = getattr(pil_image, "n_frames", 1)
        
        exif = pil_image.getexif()

        camera_model = "Unknown"
        capture_date = "Unknown"

        if exif:

            for tag_id, value in exif.items():

                tag = ExifTags.TAGS.get(tag_id, tag_id)

                if tag == "Model":
                    camera_model = value

                elif tag == "DateTime":
                    capture_date = value

        max_image_width = 900
        max_image_height = 700

        scale = min(
            max_image_width / width,
            max_image_height / height,
            1.0
        )

        display_image = cv2.resize(
            image,
            None,
            fx=scale,
            fy=scale
        )

        display_height, display_width = display_image.shape[:2]

        info_width = 420

        line_height = 30
        info_lines = 16

        required_height = 80 + info_lines * line_height

        canvas_height = max(
            display_height,
            required_height
        )

        canvas = np.zeros(
            (
                canvas_height,
                display_width + info_width,
                3
            ),
            dtype=np.uint8
        )

        canvas[
            0:display_height,
            info_width:info_width + display_width
        ] = display_image

        cv2.line(
            canvas,
            (info_width, 0),
            (info_width, canvas_height),
            (120, 120, 120),
            2
        )

        text_x = 20
        text_y = 40
        
        label_x = 20
        value_x = 240
        
        cv2.putText(
            canvas,
            "Image Information",
            (text_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        cv2.line(
            canvas,
            (10, 55),
            (info_width - 10, 55),
            (120, 120, 120),
            1
        )

        text_y += line_height * 2

        cv2.putText(
            canvas,
            "IMAGE",
            (20, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )

        text_y += 12

        cv2.line(
            canvas,
            (20, text_y),
            (info_width - 20, text_y),
            (80, 80, 80),
            1
        )

        text_y += line_height

        cv2.putText(
            canvas,
            "Shape",
            (label_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            1
        )

        cv2.putText(
            canvas,
            str(image.shape),
            (value_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 0),
            1
        )

        text_y += line_height

        cv2.putText(
            canvas,
            "Height",
            (label_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            1
        )

        cv2.putText(
            canvas,
            str(height),
            (value_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 0),
            1
        )

        text_y += line_height

        cv2.putText(
            canvas,
            "Width",
            (label_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            1
        )

        cv2.putText(
            canvas,
            str(width),
            (value_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 0),
            1
        )

        text_y += line_height

        cv2.putText(
            canvas,
            "Channels",
            (label_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            1
        )

        cv2.putText(
            canvas,
            str(channels),
            (value_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 0),
            1
        )

        text_y += line_height

        cv2.putText(
            canvas,
            "Dimensions",
            (label_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            1
        )

        cv2.putText(
            canvas,
            str(image.ndim),
            (value_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 0),
            1
        )

        text_y += line_height

        cv2.putText(
            canvas,
            "MEMORY",
            (20, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 0),
            2
        )

        text_y += 12

        cv2.line(
            canvas,
            (20, text_y),
            (info_width - 20, text_y),
            (80, 80, 80),
            1
        )

        text_y += line_height

        cv2.putText(
            canvas,
            "Data type",
            (label_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            1
        )

        cv2.putText(
            canvas,
            str(image.dtype),
            (value_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 0),
            1
        )

        text_y += line_height

        cv2.putText(
            canvas,
            "Elements",
            (label_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            1
        )

        cv2.putText(
            canvas,
            str(image.size),
            (value_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 0),
            1
        )

        text_y += line_height

        cv2.putText(
            canvas,
            "Memory",
            (label_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            1
        )

        cv2.putText(
            canvas,
            f"{image.nbytes} bytes",
            (value_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 0),
            1
        )

        text_y += line_height

        cv2.putText(
            canvas,
            "File size",
            (label_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            1
        )

        cv2.putText(
            canvas,
            file_size_text,
            (value_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 0),
            1
        )

        text_y += line_height

        cv2.putText(
            canvas,
            "Aspect ratio",
            (label_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            1
        )

        cv2.putText(
            canvas,
            f"{aspect_ratio:.2f}",
            (value_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 0),
            1
        )

        text_y += line_height

        cv2.putText(
            canvas,
            "Bytes/pixel",
            (label_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            1
        )

        cv2.putText(
            canvas,
            str(bytes_per_pixel),
            (value_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 0),
            1
        )
        
        text_y += line_height

        cv2.putText(
            canvas,
            "STATISTICS",
            (20, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        text_y += 12

        cv2.line(
            canvas,
            (20, text_y),
            (info_width - 20, text_y),
            (80, 80, 80),
            1
        )

        text_y += line_height

        cv2.putText(
            canvas,
            "Color image",
            (label_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            1
        )

        cv2.putText(
            canvas,
            str(is_color),
            (value_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 0),
            1
        )

        text_y += line_height

        cv2.putText(
            canvas,
            "Min value",
            (label_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            1
        )

        cv2.putText(
            canvas,
            str(min_value),
            (value_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 0),
            1
        )

        text_y += line_height

        cv2.putText(
            canvas,
            "Max value",
            (label_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            1
        )

        cv2.putText(
            canvas,
            str(max_value),
            (value_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 0),
            1
        )

        text_y += line_height

        cv2.putText(
            canvas,
            "Mean value",
            (label_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            1
        )

        cv2.putText(
            canvas,
            f"{mean_value:.2f}",
            (value_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 0),
            1
        )

        text_y += line_height

        cv2.putText(
            canvas,
            "PILLOW",
            (20, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 0, 255),
            2
        )

        text_y += 12

        cv2.line(
            canvas,
            (20, text_y),
            (info_width - 20, text_y),
            (80, 80, 80),
            1
        )

        text_y += line_height

        cv2.putText(
            canvas,
            "Format",
            (label_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            1
        )

        cv2.putText(
            canvas,
            str(image_format),
            (value_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 0),
            1
        )

        text_y += line_height

        cv2.putText(
            canvas,
            "Mode",
            (label_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            1
        )

        cv2.putText(
            canvas,
            str(image_mode),
            (value_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 0),
            1
        )

        text_y += line_height

        cv2.putText(
            canvas,
            "Extension",
            (label_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            1
        )

        cv2.putText(
            canvas,
            extension,
            (value_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 0),
            1
        )

        text_y += line_height

        cv2.putText(
            canvas,
            "Frames",
            (label_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            1
        )

        cv2.putText(
            canvas,
            str(frame_count),
            (value_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 0),
            1
        )

        text_y += line_height

        cv2.putText(
            canvas,
            "Camera",
            (label_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            1
        )

        cv2.putText(
            canvas,
            str(camera_model),
            (value_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 0),
            1
        )

        text_y += line_height

        cv2.putText(
            canvas,
            "Date",
            (label_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            1
        )

        cv2.putText(
            canvas,
            str(capture_date),
            (value_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 0),
            1
        )

        text_y += line_height

        cv2.putText(
            canvas,
            "PIXEL",
            (20, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 128, 0),
            2
        )

        text_y += 12

        cv2.line(
            canvas,
            (20, text_y),
            (info_width - 20, text_y),
            (80, 80, 80),
            1
        )

        text_y += line_height

        cv2.putText(
            canvas,
            "Array type",
            (label_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            1
        )

        cv2.putText(
            canvas,
            type(image).__name__,
            (value_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 0),
            1
        )

        text_y += line_height

        b, g, r = image[0, 0]

        cv2.putText(
            canvas,
            "Pixel [0,0]",
            (label_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            1
        )

        cv2.putText(
            canvas,
            f"B={b} G={g} R={r}",
            (value_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 0),
            1
        )

        cv2.putText(
            canvas,
            "Press any key to exit",
            (20, canvas_height - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (180, 180, 180),
            1
        )
        
        cv2.namedWindow(
            "Show Image",
            cv2.WINDOW_NORMAL
        )

        cv2.imshow(
            "Show Image",
            canvas
        )

        cv2.waitKey(0)

        cv2.destroyAllWindows()
