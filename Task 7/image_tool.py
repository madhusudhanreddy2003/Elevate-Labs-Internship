import os
import argparse

from PIL import Image

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False

VALID_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff")


def list_images(input_folder):
    """Return list of image file names inside the input folder."""
    if not os.path.isdir(input_folder):
        print(f"[ERROR] Input folder does not exist: {input_folder}")
        return []

    files = [
        f for f in os.listdir(input_folder)
        if f.lower().endswith(VALID_EXTENSIONS)
    ]
    return files


def compute_new_size(img, target_w, target_h, keep_aspect, auto_orientation):
    """Compute target size, with optional aspect ratio & orientation handling."""
    orig_w, orig_h = img.size

    # If we don't keep aspect ratio -> just force to width x height
    if not keep_aspect:
        return (target_w, target_h)

    # If auto_orientation is enabled:
    # - For landscape images, use (target_w, target_h)
    # - For portrait images, swap them -> (target_h, target_w)
    if auto_orientation:
        if orig_h > orig_w:  # portrait
            box_w, box_h = target_h, target_w
        else:  # landscape or square
            box_w, box_h = target_w, target_h
    else:
        box_w, box_h = target_w, target_h

    # Scale to fit inside box (box_w x box_h) while keeping aspect ratio
    scale_w = box_w / orig_w
    scale_h = box_h / orig_h
    scale = min(scale_w, scale_h)

    new_w = max(1, int(orig_w * scale))
    new_h = max(1, int(orig_h * scale))
    return (new_w, new_h)


def get_output_name(index, original_name, fmt_ext, rename_prefix):
    """Create output file name (either bulk renamed or based on original)."""
    if rename_prefix:
        # Example: photo_001.jpg, photo_002.jpg, ...
        return f"{rename_prefix}_{index:03d}.{fmt_ext}"
    else:
        base_name = os.path.splitext(original_name)[0]
        return f"{base_name}_resized.{fmt_ext}"


def process_images(
    input_folder,
    output_folder,
    width,
    height,
    keep_aspect,
    auto_orientation,
    output_format,
    quality,
    rename_prefix,
):
    os.makedirs(output_folder, exist_ok=True)

    images = list_images(input_folder)
    if not images:
        print("[INFO] No images found to process.")
        return

    output_format = output_format.upper()

    # Map format to extension
    ext_map = {
        "JPEG": "jpg",
        "JPG": "jpg",
        "PNG": "png",
        "WEBP": "webp",
        "BMP": "bmp",
    }
    fmt_ext = ext_map.get(output_format, output_format.lower())

    print(f"[INFO] Found {len(images)} images in '{input_folder}'.")
    print(f"[INFO] Output format: {output_format}, quality: {quality}")
    print(f"[INFO] Keep aspect ratio: {keep_aspect}, auto-orientation: {auto_orientation}")
    print(f"[INFO] Output folder: {output_folder}")
    print("-" * 50)

    iterator = images
    if TQDM_AVAILABLE:
        iterator = tqdm(images, desc="Processing images", unit="img")

    processed = 0
    errors = 0

    for idx, filename in enumerate(iterator, start=1):
        input_path = os.path.join(input_folder, filename)

        try:
            with Image.open(input_path) as img:
                # For JPEG: convert from RGBA/P to RGB to avoid errors
                if output_format in ("JPEG", "JPG") and img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")

                new_size = compute_new_size(
                    img,
                    width,
                    height,
                    keep_aspect=keep_aspect,
                    auto_orientation=auto_orientation,
                )

                resized = img.resize(new_size, Image.LANCZOS)

                output_name = get_output_name(
                    index=idx,
                    original_name=filename,
                    fmt_ext=fmt_ext,
                    rename_prefix=rename_prefix,
                )
                output_path = os.path.join(output_folder, output_name)

                save_kwargs = {}
                # quality relevant mainly for JPEG/WEBP
                if output_format in ("JPEG", "JPG", "WEBP"):
                    save_kwargs["quality"] = quality

                resized.save(output_path, output_format, **save_kwargs)
                processed += 1

        except Exception as e:
            errors += 1
            if TQDM_AVAILABLE:
                tqdm.write(f"[ERROR] Could not process {filename}: {e}")
            else:
                print(f"[ERROR] Could not process {filename}: {e}")

    print("-" * 50)
    print(f"[DONE] Processed: {processed}, Errors: {errors}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Batch Image Resizer & Converter (CLI) – with quality, aspect ratio, and auto-orientation."
    )
    parser.add_argument(
        "-i", "--input", default="input_images", help="Input folder with images"
    )
    parser.add_argument(
        "-o", "--output", default="output_images", help="Output folder for resized images"
    )
    parser.add_argument(
        "-W", "--width", type=int, default=800, help="Target width (pixels)"
    )
    parser.add_argument(
        "-H", "--height", type=int, default=800, help="Target height (pixels)"
    )
    parser.add_argument(
        "-f", "--format", default="JPEG", help="Output format (JPEG, PNG, WEBP, BMP)"
    )
    parser.add_argument(
        "-q", "--quality", type=int, default=85, help="Output quality (0-100) for JPEG/WEBP"
    )
    parser.add_argument(
        "--keep-aspect",
        action="store_true",
        help="Maintain aspect ratio (fit inside a box)",
    )
    parser.add_argument(
        "--auto-orientation",
        action="store_true",
        help="Auto-detect landscape/portrait and adjust box orientation",
    )
    parser.add_argument(
        "--rename-prefix",
        type=str,
        default=None,
        help="Bulk rename prefix (e.g., 'photo' → photo_001.jpg)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    process_images(
        input_folder=args.input,
        output_folder=args.output,
        width=args.width,
        height=args.height,
        keep_aspect=args.keep_aspect,
        auto_orientation=args.auto_orientation,
        output_format=args.format,
        quality=args.quality,
        rename_prefix=args.rename_prefix,
    )


if __name__ == "__main__":
    main()
