from .html_annotator import HTMLAnnotator
from settings.config import (
    RESULT_DIRECTORY,
    SUBMITTED_PAPER_HTML,
    CAMERA_READY_PAPER_HTML,
    FLAWS_JSON,
    FLAWS_ADDRESSED_JSON,
    HTML_TEMPLATE_DIRECTORY,
    HTML_TEMPLATE_FILE_NAME,
    ANNOTATED_HTML_FILE,
    OPENREVIEW_PAPER_ID,
    REVIEWS_JSON
)

if __name__ == "__main__":
    annotator = HTMLAnnotator(
        template_directory=HTML_TEMPLATE_DIRECTORY,
        template_file=HTML_TEMPLATE_FILE_NAME,
        openreview_paper_id=OPENREVIEW_PAPER_ID

    )
    annotator.load_html_papers(
        submitted_filepath=SUBMITTED_PAPER_HTML,
        camera_ready_filepath=CAMERA_READY_PAPER_HTML
    )
    annotator.load_flaws(
        json_directory=RESULT_DIRECTORY,
        json_file=FLAWS_JSON
    )
    annotator.load_flaws_addressed(
        json_directory=RESULT_DIRECTORY,
        json_file=FLAWS_ADDRESSED_JSON
    )
    annotator.load_reviews(
        json_directory=RESULT_DIRECTORY,
        json_file=REVIEWS_JSON
    )

    annotator.annotate_html()
    annotator.save_annotated_html(
        html_directory=RESULT_DIRECTORY,
        html_file=ANNOTATED_HTML_FILE
    )
