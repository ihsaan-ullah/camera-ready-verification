import os
from .gemini_client import GeminiClient
from prompts.prompt_B import prompt as CAMERA_READY_PAPER_PROMPT
from settings.config import (
    GEMINI_MODEL,
    RESULT_DIRECTORY,
    FLAWS_JSON,
    FLAWS_ADDRESSED_JSON,
    SUBMITTED_PAPER_HTML,
    CAMERA_READY_PAPER_HTML,
)
from .utils import (
    read_html_file,
    read_json_file,
    fill_papers_and_flaws_in_prompt,
    save_json_to_file,
    convert_json_string_to_json
)
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")


if __name__ == "__main__":

    try:
        gemini = GeminiClient(api_key=API_KEY, model=GEMINI_MODEL)
        html_submitted = read_html_file(filepath=SUBMITTED_PAPER_HTML)
        html_camera_ready = read_html_file(filepath=CAMERA_READY_PAPER_HTML)
        flaws_json = read_json_file(directory=RESULT_DIRECTORY, filename=FLAWS_JSON)
        prompt = fill_papers_and_flaws_in_prompt(
            prompt=CAMERA_READY_PAPER_PROMPT,
            html_submitted=html_submitted,
            html_camera_ready=html_camera_ready,
            flaws_json=flaws_json
        )
        llm_response = gemini.generate_text(prompt)
        cleaned_llm_response = convert_json_string_to_json(llm_response)
        save_json_to_file(data=cleaned_llm_response, directory=RESULT_DIRECTORY, filename=FLAWS_ADDRESSED_JSON)

    except Exception as e:
        print(f"[-] Error: {e}")
