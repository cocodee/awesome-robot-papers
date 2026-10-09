#!/usr/bin/env python3
"""
Higher-quality (less aggressive) compression for PNG + JPG/JPEG.

Requires:
  pip install pillow
"""

import os
from pathlib import Path
from PIL import Image, ImageFile

# -------------------------
# Parameters (edit these)
# -------------------------
ROOT_DIR = "/Users/tiangexiang/Desktop/publications/QuantiPhy/arxiv/nbrrbwkqrctgrqbjkvkwnyvxmrvgqwjx/sec/images/"
RECURSIVE = False
IN_PLACE = True
SUFFIX = "_c50hq"          # used only if IN_PLACE=False
KEEP_SMALLER_ONLY = True

TARGET_RATIO = 0.50        # best-effort target (may not be reached with higher quality)

# JPEG (raise quality)
JPEG_QUALITY = 92
JPEG_SUBSAMPLING = 0       # 0 = 4:4:4 (best quality)
JPEG_OPTIMIZE = True
JPEG_PROGRESSIVE = True
FLATTEN_ALPHA_BG = (255, 255, 255)

# PNG (more conservative): lossless optimize; quantize only if still *far* from target
PNG_OPTIMIZE = True
PNG_COMPRESS_LEVEL = 9
PNG_TRY_MILD_QUANTIZE_IF_TOO_BIG = True
PNG_QUANTIZE_COLORS = 256          # mildest
PNG_DITHER = Image.Dither.NONE

# Quantize PNG only if lossless result is still above (target * this factor).
# Increase this to quantize less often (i.e., preserve quality more).
PNG_QUANTIZE_TRIGGER_FACTOR = 1.60  # was 1.25; now more conservative

# -------------------------

ImageFile.LOAD_TRUNCATED_IMAGES = True


def human_bytes(n: int) -> str:
    units = ["B", "KB", "MB", "GB"]
    f = float(n)
    for u in units:
        if f < 1024 or u == units[-1]:
            return f"{f:.2f}{u}"
        f /= 1024
    return f"{f:.2f}B"


def iter_images(root: Path, recursive: bool):
    patterns = ["*.png", "*.PNG", "*.jpg", "*.JPG", "*.jpeg", "*.JPEG"]
    if recursive:
        for pat in patterns:
            yield from root.rglob(pat)
    else:
        for pat in patterns:
            yield from root.glob(pat)


def get_tmp_and_final_paths(in_path: Path):
    if IN_PLACE:
        tmp_out = in_path.with_suffix(in_path.suffix + ".tmp")
        final_out = in_path
    else:
        final_out = in_path.with_name(in_path.stem + SUFFIX + in_path.suffix)
        tmp_out = final_out.with_suffix(final_out.suffix + ".tmp")
    return tmp_out, final_out


def compress_jpeg(img: Image.Image, out_path: Path):
    # Flatten alpha if present
    if img.mode in ("RGBA", "LA"):
        bg = Image.new("RGB", img.size, FLATTEN_ALPHA_BG)
        bg.paste(img, mask=img.split()[-1])
        img = bg
    elif img.mode != "RGB":
        img = img.convert("RGB")

    img.save(
        out_path,
        format="JPEG",
        quality=JPEG_QUALITY,
        subsampling=JPEG_SUBSAMPLING,
        optimize=JPEG_OPTIMIZE,
        progressive=JPEG_PROGRESSIVE,
    )


def save_png_lossless(img: Image.Image, out_path: Path):
    img.save(
        out_path,
        format="PNG",
        optimize=PNG_OPTIMIZE,
        compress_level=PNG_COMPRESS_LEVEL,
    )


def save_png_mild_quantized(img: Image.Image, out_path: Path):
    # Mild quantization (usually safe for plots/icons; can affect photos/gradients)
    has_alpha = ("A" in img.getbands()) or (img.mode == "P" and "transparency" in img.info)
    base = img.convert("RGBA") if has_alpha else img.convert("RGB")
    q = base.quantize(colors=PNG_QUANTIZE_COLORS, dither=PNG_DITHER)
    q.save(out_path, format="PNG", optimize=PNG_OPTIMIZE, compress_level=PNG_COMPRESS_LEVEL)


def process_one(path: Path):
    old_size = path.stat().st_size
    target_bytes = int(old_size * TARGET_RATIO)
    ext = path.suffix.lower()

    tmp_out, final_out = get_tmp_and_final_paths(path)
    final_out.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(path) as img:
        img.load()

        if ext in (".jpg", ".jpeg"):
            compress_jpeg(img, tmp_out)

        elif ext == ".png":
            # 1) Lossless optimize
            save_png_lossless(img, tmp_out)

            # 2) Quantize only if still far from target (more conservative now)
            if PNG_TRY_MILD_QUANTIZE_IF_TOO_BIG:
                try:
                    lossless_size = tmp_out.stat().st_size
                    if lossless_size > int(target_bytes * PNG_QUANTIZE_TRIGGER_FACTOR):
                        save_png_mild_quantized(img, tmp_out)
                except Exception:
                    pass
        else:
            raise ValueError(f"Unsupported extension: {ext}")

    new_size = tmp_out.stat().st_size

    if KEEP_SMALLER_ONLY and new_size >= old_size:
        tmp_out.unlink(missing_ok=True)
        return False, old_size, old_size, path

    os.replace(tmp_out, final_out)
    return True, old_size, final_out.stat().st_size, final_out


def main():
    root = Path(ROOT_DIR).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"ROOT_DIR not found or not a directory: {root}")

    total_old = 0
    total_new = 0
    seen = 0
    changed = 0

    for p in iter_images(root, RECURSIVE):
        if not p.is_file():
            continue
        seen += 1
        try:
            did, old_b, new_b, outp = process_one(p)
            total_old += old_b
            total_new += new_b
            ratio = (new_b / old_b) if old_b else 1.0

            if did:
                changed += 1
                print(f"[OK]   {p} -> {outp}  {human_bytes(old_b)} -> {human_bytes(new_b)}  (ratio {ratio:.2f})")
            else:
                print(f"[SKIP] {p}  {human_bytes(old_b)} (no improvement)")
        except Exception as e:
            print(f"[ERR]  {p}: {e}")

    if seen == 0:
        print("No PNG/JPG/JPEG files found.")
        return

    overall_ratio = (total_new / total_old) if total_old else 1.0
    print("\n==== Summary ====")
    print(f"Files seen:     {seen}")
    print(f"Files changed:  {changed}")
    print(f"Total before:   {human_bytes(total_old)}")
    print(f"Total after:    {human_bytes(total_new)}")
    print(f"Total saved:    {human_bytes(total_old - total_new)}")
    print(f"Overall ratio:  {overall_ratio:.2f}  (target {TARGET_RATIO:.2f})")


if __name__ == "__main__":
    main()
