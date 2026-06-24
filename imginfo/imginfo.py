import argparse
import os
from math import gcd
from pathlib import Path
from PIL import Image, UnidentifiedImageError
from PIL import __version__ as pillow_version
from rich.console import Console
from rich.table import Table

console = Console()

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

           #added file size
           file_size = os.path.getsize(image_path)

           if file_size < 1024:
              file_size_str = f"{file_size} B"
           elif file_size < 1024 ** 2:
              file_size_str = f"{file_size / 1024:.2f} KB"
           else:
               file_size_str = f"{file_size / (1024 ** 2):.2f} MB"

           #added aspect ratio
           ratio = gcd(image.width, image.height)
           aspect_ratio = f"{image.width // ratio}:{image.height // ratio}"

           #added pixel count
           pixel_count = image.width * image.height

           #added animated image
           is_animated = getattr(image, "is_animated", False)

           if is_animated:
               frames = getattr(image, "n_frames", 1)
           else:
               frames = 1

           #added colored format
           format_colors = {
                "PNG": "[green]PNG[/green]",
                "JPEG": "[yellow]JPEG[/yellow]",
                "JPG": "[blue]JPG[/blue]",
                "GIF": "[cyan]GIF[/cyan]",
                "WEBP": "[magenta]WEBP[/magenta]",
                "BMP": "[blue]BMP[/blue]"
           }

           format_name = format_colors.get(image.format, str(image.format))


           table = Table(
               title="Image Information",
               header_style="magenta",
               border_style="blue"
           )

           table.add_column("Property", style="cyan")
           table.add_column("Value", style="green")

           table.add_row("File name", image_path.name)
           table.add_row("File size", file_size_str)
           table.add_row("Absolute path", str(image_path.resolve()))
           table.add_row("Format", format_name)
           table.add_row("Size", f"{image.width} × {image.height}")
           table.add_row("Aspect ratio", aspect_ratio)
           table.add_row("Width", str(image.width))
           table.add_row("Height", str(image.height))
           table.add_row("Pixels", f"{pixel_count:,}")
           table.add_row("Color mode", image.mode)
           table.add_row("Channels", ", ".join(image.getbands()))
           table.add_row("DPI", str(image.info.get("dpi", "Unknown")))
           table.add_row("Animated", "Yes" if is_animated else "No")
           table.add_row("Frames", str(frames))
           table.add_row("Processed by", f"Pillow {pillow_version}")

           console.print(table)

    except UnidentifiedImageError:
       print("Error: file is not a valid image")

    except Exception as error:
       print(f"Unexpected error: {error}")
