from PIL import Image
import os

# Gradient of characters from dark to light
ASCII_CHARS = "@%#*+=-:. "

def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width / 1.65  # Adjust height for terminal aspect ratio
    new_height = int(new_width * ratio)
    return image.resize((new_width, new_height))

def grayify(image):
    return image.convert("L")  # Convert to grayscale

def pixels_to_ascii(image):
    pixels = image.getdata()
    ascii_str = "".join([ASCII_CHARS[min(pixel // 25, len(ASCII_CHARS) - 1)] for pixel in pixels])
    return ascii_str

def run(args, commands):
    if "-d" not in args or "-w" not in args:
        print("Usage: assci -d <image_path> -w <width>")
        return

    try:
        img_index = args.index("-d") + 1
        width_index = args.index("-w") + 1
        path = args[img_index]
        width = int(args[width_index])
    except (ValueError, IndexError):
        print("[assci] Invalid arguments.")
        return

    if not os.path.exists(path):
        print(f"[assci] File not found: {path}")
        return

    try:
        image = Image.open(path)
    except Exception as e:
        print(f"[assci] Failed to open image: {e}")
        return

    # Process image and generate ASCII
    image = resize_image(grayify(image), width)
    ascii_str = pixels_to_ascii(image)

    # Format string into lines
    pixel_count = len(ascii_str)
    ascii_image = "\n".join(
        [ascii_str[index:(index + width)] for index in range(0, pixel_count, width)]
    )

    print(ascii_image)
