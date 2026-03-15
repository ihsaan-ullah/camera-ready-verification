from .review_collector import OpenReview_ReviewCollector
from settings.config import RESULT_DIRECTORY, OPENREVIEW_PAPER_ID, REVIEWS_JSON
from .utils import save_json_to_file


if __name__ == "__main__":

    try:
        reviewCollector = OpenReview_ReviewCollector(
            openreview_group_id="ICLR.cc",
            conference_year="2024",
            conference_type="Conference",
            openreview_paper_id=OPENREVIEW_PAPER_ID
        )

        reviewCollector.get_paper()
        reviewCollector.get_paper_reviews()
        reviews = reviewCollector.get_clean_reviews()

        save_json_to_file(data=reviews, directory=RESULT_DIRECTORY, filename=REVIEWS_JSON)

    except Exception as e:
        print(f"[-] Error: {e}")
