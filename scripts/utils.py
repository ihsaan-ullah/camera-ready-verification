import os
import json
import re


def read_html_file(filepath=None, directory=None, filename=None):

    if filepath is None:
        filepath = os.path.join(directory, filename)

    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()

    return content


def read_json_file(filepath=None, directory=None, filename=None):

    if filepath is None:
        filepath = os.path.join(directory, filename)

    with open(filepath, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"[-] Invalid JSON format in {filepath}: {e}")

    return data


def fill_paper_and_reviews_in_prompt(prompt, html_submitted, reviews_json):

    return prompt.replace("{paper}", html_submitted).replace("{reviews}", str(reviews_json))


def fill_papers_and_flaws_in_prompt(prompt, html_submitted, html_camera_ready, flaws_json):

    return prompt.replace("{submitted_paper}", html_submitted).replace("{camera_ready_paper}", str(html_camera_ready)).replace("{flaws}", str(flaws_json))


def save_html_to_file(html_content, filepath=None, directory=None, filename=None):
    if filepath is None:
        filepath = os.path.join(directory, filename)

    # Write the HTML content to the file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)

    return filepath


def save_json_to_file(data, filepath=None, directory=None, filename=None):
   
    if filepath is None:
        filepath = os.path.join(directory, filename)

    # Write the JSON data to the file with pretty formatting
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return filepath


def convert_json_string_to_json(json_string):
    # Remove ```json ... ``` or ``` ... ``` markers
    cleaned_string = re.sub(r"^```(?:json)?\s*|\s*```$", "", json_string.strip(), flags=re.MULTILINE)

    # Convert to JSON object
    try:
        json_obj = json.loads(cleaned_string)
        return json_obj
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON string provided. Error: {e}")
