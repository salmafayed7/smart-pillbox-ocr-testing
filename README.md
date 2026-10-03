# Smart Pillbox – OCR Testing

Experiments for extracting medication info (name, dose, frequency, duration, schedule, notes) from prescription images.

## Images

The [images/](images/) folder contains sample prescriptions, sorted into two subfolders:

- [images/electronic/](images/electronic/) – typed/printed prescriptions
- [images/handwritten/](images/handwritten/) – handwritten prescriptions

## Qwen test

[qwen_test.py](qwen_test.py) sends a prescription image to `qwen/qwen2.5-vl-72b-instruct` via the [OpenRouter](https://openrouter.ai) API and prints the extracted medications as JSON.

**You need:**
- Python 3 and `requests` (`pip install requests`)
- An OpenRouter API key
- To edit two placeholders in the script: `<PATH_TO_IMAGE>` (e.g. `images/electronic/1.png`) and `YOUR_API_KEY`

**Run:**
```bash
python qwen_test.py
```

Don't commit your API key.

## Other OCR tests

[tesseract-rapidocr-easyocr-tests/](tesseract-rapidocr-easyocr-tests/) compares three traditional OCR engines (**Tesseract 5**, **RapidOCR**, **EasyOCR**). [ocr_benchmark.py](tesseract-rapidocr-easyocr-tests/ocr_benchmark.py) preprocesses the image separately for each engine, then prints the extracted text and the time each took. Sample outputs are saved as `.txt` files in the same folder, and [ocr_benchmark_explanation.md](tesseract-rapidocr-easyocr-tests/ocr_benchmark_explanation.md) walks through the script line by line.

**You need:**
```bash
pip install pytesseract pillow rapidocr-onnxruntime easyocr numpy
```
Tesseract also requires the Tesseract 5 binary installed and on your `PATH`. If an engine is missing, it is skipped with an install hint.

**Run:**
```bash
python tesseract-rapidocr-easyocr-tests/ocr_benchmark.py images/handwritten/17.jpg
```

## Comparison

See [OCR approaches comparison.pdf](<OCR approaches comparison.pdf>) for the final comparison of the approaches.
