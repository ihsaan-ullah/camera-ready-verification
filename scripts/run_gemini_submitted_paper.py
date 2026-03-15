import os
from .gemini_client import GeminiClient
from prompts.prompt_A import prompt as SUBMITTED_PAPER_PROMPT
from settings.config import (
    GEMINI_MODEL,
    RESULT_DIRECTORY,
    FLAWS_JSON,
    SUBMITTED_PAPER_HTML,
    REVIEWS_JSON
)
from .utils import (
    read_html_file,
    read_json_file,
    fill_paper_and_reviews_in_prompt,
    save_json_to_file,
    convert_json_string_to_json
)
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")


if __name__ == "__main__":

    try:
        gemini = GeminiClient(api_key=API_KEY, model=GEMINI_MODEL)
        html_content = read_html_file(filepath=SUBMITTED_PAPER_HTML)
        reviews_json = read_json_file(directory=RESULT_DIRECTORY, filename=REVIEWS_JSON)
        prompt = fill_paper_and_reviews_in_prompt(
            prompt=SUBMITTED_PAPER_PROMPT,
            html_submitted=html_content,
            reviews_json=reviews_json
        )
        llm_response = gemini.generate_text(prompt)
        cleaned_llm_response = convert_json_string_to_json(llm_response)
        save_json_to_file(data=cleaned_llm_response, directory=RESULT_DIRECTORY, filename=FLAWS_JSON)

    except Exception as e:
        print(f"[-] Error: {e}")
