import argparse

def main(filename):
    print(f"Received file: {filename}")

def parse_args():
    parser = argparse.ArgumentParser(
         description = "Image info CLI tool"
    )


parser.add_argument(
     "Image",
     help = "Path to the image file"
)

args = parser.parse_args()
return args

if __name__ == "__main__":
    args = parse_args()
    main(args.image)
