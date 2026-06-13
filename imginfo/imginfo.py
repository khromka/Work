import argparse
from pathlib import Path
from PIL import Image, UnidentifiedImageError

parser = argparse.ArgumentParser(
    description="Show information about an image file"
)

parser.add_argument(
    "image",
    help="Path to image file"
)

args = parser.parse_args()

image_path = Path(args.image)

print("Image path:", args.image)

if not image_path.exists():
   print("Error: file does not exists")
elif not image_path.is_file():
   print("Error: path is not a file")
else:
    try:
       with Image.open(image_path) as image:

           image.verify()
       with Image.open(image_path) as image:

           print("File exists")
           print("Format:", image.format)
           print("Mode:", image.mode)
           print("Size:", image.size)

    except UnidentifiedImageError:
       print("Error: file is not a valid image")

    except Exception as error:
       print(f"Unexpected error: {error}")
