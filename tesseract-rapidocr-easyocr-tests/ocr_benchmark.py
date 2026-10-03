import sys
import time
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")


def banner(title):
    print("\n" + "─" * 60)
    print(f"  {title}")
    print("─" * 60)

def show(text, elapsed):
    text = text.strip()
    print(f"  time: {elapsed:.2f}s\n")
    if text:
        for line in text.splitlines():
            if line.strip():
                print(f"{line}")
    else:
        print("  [no text detected]")


# ── per-model preprocessing ───────────────────────────────────────────────────

def preprocess_for_tesseract(image_path):
    """Grayscale → upscale → contrast → sharpen → binarize."""
    from PIL import Image, ImageEnhance, ImageFilter
    img = Image.open(image_path).convert("L")
    # Tesseract accuracy degrades on small images; target ~2000px on the long side
    longest = max(img.size)
    if longest < 1500:
        scale = max(2, 2000 // longest)
        img = img.resize((img.width * scale, img.height * scale), Image.LANCZOS)
    img = ImageEnhance.Contrast(img).enhance(2.0)
    img = img.filter(ImageFilter.SHARPEN)
    img = img.point(lambda p: 255 if p > 150 else 0)
    return img

def preprocess_for_rapidocr(image_path):
    """Color image with mild contrast boost → numpy array."""
    import numpy as np
    from PIL import Image, ImageEnhance
    img = Image.open(image_path).convert("RGB")
    img = ImageEnhance.Contrast(img).enhance(1.5)
    return np.array(img)

def preprocess_for_easyocr(image_path):
    """Color image with contrast + sharpness boost → numpy array."""
    import numpy as np
    from PIL import Image, ImageEnhance
    img = Image.open(image_path).convert("RGB")
    img = ImageEnhance.Contrast(img).enhance(1.5)
    img = ImageEnhance.Sharpness(img).enhance(2.0)
    return np.array(img)


# ── runners ───────────────────────────────────────────────────────────────────

def run_tesseract(image_path):
    banner("1 · Tesseract 5")
    try:
        import pytesseract
        img = preprocess_for_tesseract(image_path)
        t0 = time.time()
        text = pytesseract.image_to_string(img)
        show(text, time.time() - t0)
    except ImportError:
        print("  [!] pip install pytesseract pillow")
    except Exception as e:
        print(f"  [!] {e}")


def run_rapidocr(image_path):
    banner("2 · RapidOCR")
    try:
        from rapidocr_onnxruntime import RapidOCR
        arr = preprocess_for_rapidocr(image_path)
        t0 = time.time()
        result, _ = RapidOCR()(arr)
        elapsed = time.time() - t0
        text = "\n".join(line[1] for line in result) if result else ""
        show(text, elapsed)
    except ImportError:
        print("  [!] pip install rapidocr-onnxruntime")
    except Exception as e:
        print(f"  [!] {e}")


def run_easyocr(image_path):
    banner("3 · EasyOCR")
    try:
        import easyocr
        arr = preprocess_for_easyocr(image_path)
        t0 = time.time()
        reader = easyocr.Reader(["en"], gpu=False, verbose=False)
        result = reader.readtext(arr, detail=0)
        elapsed = time.time() - t0
        show("\n".join(result), elapsed)
    except ImportError:
        print("  [!] pip install easyocr")
    except Exception as e:
        print(f"  [!] {e}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python ocr_benchmark.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    if not Path(image_path).exists():
        print(f"[!] File not found: {image_path}")
        sys.exit(1)

    print(f"\n{'═' * 60}")
    print(f"  OCR Benchmark  ·  {image_path}")
    print(f"{'═' * 60}")

    run_tesseract(image_path)
    run_rapidocr(image_path)
    run_easyocr(image_path)

    print("\n" + "═" * 60 + "\n")


if __name__ == "__main__":
    main()
