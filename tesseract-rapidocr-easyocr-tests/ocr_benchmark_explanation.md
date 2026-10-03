# ocr_benchmark.py — Line-by-Line Explanation

## Summary

The script is an OCR comparison tool. You give it one image path; it runs **Tesseract 5**, **RapidOCR**, and **EasyOCR** on that image (each with its own tailored preprocessing), prints what text each engine extracted, and shows how long each took. The goal is to compare accuracy and speed across the three engines.

**Usage:**
```bash
python ocr_benchmark.py <image_path>
```

---

## Top-level setup (lines 1–16)

**Line 1** — Shebang line; tells Unix-like systems to run this with `python3` when executed directly.

**Lines 2–9** — Module docstring: documents the script's purpose (benchmark 3 OCR engines), how to run it, and what to install.

**Lines 11–14** — Standard library imports:
- `sys` — to read command-line arguments and exit
- `time` — to measure how long each OCR run takes
- `warnings` — to suppress noisy library warnings
- `Path` (from `pathlib`) — to check if the input file exists

**Line 16** — Suppresses all Python warnings globally (e.g., deprecation warnings from OCR libraries).

---

## Helper functions (lines 19–32)

**Lines 19–22 — `banner(title)`**
Prints a visual section header: a 60-dash line, the title indented, then another 60-dash line. Used to separate the output of each OCR engine.

**Lines 24–32 — `show(text, elapsed)`**
Prints the OCR result:
- Strips leading/trailing whitespace from the text.
- Always prints elapsed time formatted to 2 decimal places.
- If text was found: prints each non-empty line, indented with 2 spaces.
- If no text was found: prints `[no text detected]`.

---

## Per-model preprocessing (lines 37–66)

Each function opens the image and prepares it differently based on what each engine works best with.

**Lines 37–49 — `preprocess_for_tesseract(image_path)`**
- Opens the image and converts it to **grayscale** (`"L"` mode).
- If the longest side is under 1500px, it **upscales** to at least 2000px using LANCZOS (high-quality) resampling — Tesseract performs poorly on small images.
- **Doubles the contrast** (factor 2.0).
- Applies a **sharpen filter**.
- **Binarizes** the image: every pixel above brightness 150 becomes white (255), everything else black (0). This gives Tesseract clean black-on-white text.

**Lines 51–57 — `preprocess_for_rapidocr(image_path)`**
- Opens the image in **color** (RGB).
- Applies a **mild contrast boost** (1.5×).
- Returns it as a **NumPy array** — RapidOCR's expected input format.

**Lines 59–66 — `preprocess_for_easyocr(image_path)`**
- Opens the image in **color** (RGB).
- Applies contrast boost (1.5×) and **sharpness boost** (2.0×) — slightly more aggressive than RapidOCR's preprocessing.
- Returns it as a **NumPy array**.

---

## OCR runners (lines 71–114)

**Lines 71–82 — `run_tesseract(image_path)`**
- Prints the `"1 · Tesseract 5"` banner.
- Imports `pytesseract` (deferred import so the script doesn't crash if it's missing).
- Preprocesses the image.
- Starts a timer, runs `image_to_string()`, stops the timer.
- Calls `show()` to print the result and time.
- Catches `ImportError` (library not installed) and any other exception separately, printing a user-friendly message in both cases.

**Lines 85–98 — `run_rapidocr(image_path)`**
- Prints the `"2 · RapidOCR"` banner.
- Imports and instantiates `RapidOCR()`, then immediately calls it on the array (`RapidOCR()(arr)` — creates the engine and runs it in one line).
- The result is a list of detected text lines; each element is `[bounding_box, text, confidence]`. Line 93 joins just the text part (`line[1]`) into a single string.
- Calls `show()` with the joined text and elapsed time.

**Lines 101–114 — `run_easyocr(image_path)`**
- Prints the `"3 · EasyOCR"` banner.
- Creates an `easyocr.Reader` for English, CPU-only (`gpu=False`), with verbose logging off.
- Runs `readtext()` with `detail=0` — returns just the text strings, no bounding boxes or confidence scores.
- Joins the result list into a newline-separated string and calls `show()`.

---

## Entry point (lines 117–139)

**Lines 117–125 — argument validation in `main()`**
- If no argument is passed, prints usage and exits with code 1.
- Reads `sys.argv[1]` as the image path.
- If the file doesn't exist, prints an error and exits with code 1.

**Lines 127–129** — Prints a top-level header showing the image path being benchmarked.

**Lines 131–133** — Runs all three OCR engines sequentially on the same image path.

**Line 135** — Prints a closing separator line.

**Lines 138–139** — Standard Python idiom: only calls `main()` when the script is run directly (not when imported as a module).
