from datetime import datetime
from pathlib import Path
from PIL import Image, ImageFilter
import time

# Directories for input and output images
SOURCE_DIR = Path("../img")
RESULT_DIR = Path("../result")


# Separator for console
def print_separator():
    print("-" * 80)


# Save image to a file
def save_file(name, pixels, width, height, dir):
    if isinstance(pixels, Image.Image):
        result_image = pixels
    else:
        result_image = Image.new("L", (width, height))
        result_pixels = result_image.load()

        for y in range(height):
            for x in range(width):
                result_pixels[x, y] = pixels[y][x]

    result_path = dir / f"{name}.png"
    result_image.save(result_path)

    print(f"Saved to: {result_path}")


# Check whether a pixel remains white after erosion
def check_pixel(x, y, pixels, width, height):
    for delta_x in range(x - 1, x + 2):
        for delta_y in range(y - 1, y + 2):
            if delta_x < 0 or delta_x >= width or delta_y < 0 or delta_y >= height:
                return 0

            if pixels[delta_y][delta_x] == 0:
                return 0

    return 255


# Create directory for results
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
result_dir = RESULT_DIR / timestamp
result_dir.mkdir(parents=True, exist_ok=True)

# Input image
while True:
    try:
        print("Input file name:")
        image_name = input()

        source_path = SOURCE_DIR / image_name

        image = Image.open(source_path).convert("L")
        width, height = image.size
    except FileNotFoundError:
        print("File not found")
        continue

    break

# Binarize the image
binary_image = image.point(
    lambda pixel: 255 if pixel >= 128 else 0
)
image_pixels = binary_image.load()

pixels = [
    [image_pixels[x, y] for x in range(width)]
    for y in range(height)
]
print("Binary image")
save_file("binary", pixels, width, height, result_dir)

# Native erosion
start = time.perf_counter()

result = [[0] * width for _ in range(height)]
for y in range(height):
    for x in range(width):
        result[y][x] = check_pixel(x, y, pixels, width, height)

end = time.perf_counter()

print_separator()
print(f"Native erosion: {end - start:.6f} seconds")
save_file('native', result, width, height, result_dir)

# Library erosion
start = time.perf_counter()

library_result = binary_image.filter(ImageFilter.MinFilter(3))

end = time.perf_counter()

print_separator()
print(f"Library erosion: {end - start:.6f} seconds")
save_file('library', library_result, width, height, result_dir)
