import argparse
from pathlib import Path

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
    print("File exists")
