# Camere-Ready Verification

This repository provides complete code for creating camera-ready verification tool.

To create an annotated HTML that allows reviewers/meta-reviewers to verify if flaws identified in a submitted paper are addressed in the camera-ready version of the paper, the following steps needs to be followed

### Step 1: Configure `.env`
Copy the `.env_sample` as `.env` and place your Gemini API Key at the right place in this file
```
cp .env_sample .env
```

### Step 2: Configure `settings/config.py`
Configure the `config.py` file for naming the result directory and files, open-review paper id, html file names, gemini model name etc.

### Step 3: Collect reviews from OpenReview `scripts/run_review_collector.py`
This script collect reviews for the paper whose id you have configured in the config.py. It saves the reviews in `result/` directory.
```
python3 -m scripts.run_review_collector
```

### Step 4: Run submitted paper to get flaws `scripts/run_gemini_submitted_paper.py`
This scripts uses `Prompt_A`, submitted_paper HTML, and reviews to get flaws. These flaws are stored in `result/` directory.
```
python3 -m scripts.run_gemini_submitted_paper
```

### Step 5: Run camera-ready paper to get addressed flaws `scripts/run_gemini_camera_ready_paper.py`
This scripts uses `Prompt_B`, flaws, submitted_paper HTML, camera-ready paper HTML to get addressed flaws. These addressed flaws are stored in `result/` directory.
```
python3 -m scripts.run_gemini_camera_ready_paper
```

### Step 6: Run HTML Annotator `run_html_annotator.py`
This script uses everything that has been generated (flaws, addressed_flaws, reviews, submitted_paper, camera_ready_paper) and uses a template from `html/template.html` to create an annotated html. Tha annotated HTML is stored in `result/` directory.
```
python3 -m scripts.run_html_annotator
```
