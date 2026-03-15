import openreview


class OpenReview_ReviewCollector:

    def __init__(
        self,
        openreview_group_id,  # example "ICLR.cc"
        conference_year,  # example "2024"
        conference_type,  # example "Conference"
        openreview_paper_id  # example "MbfAK4s61A"
    ):
        self.client = openreview.api.OpenReviewClient(baseurl='https://api2.openreview.net')
        self.openreview_group_id = openreview_group_id
        self.conference_year = conference_year
        self.conference_type = conference_type
        self.openreview_paper_id = openreview_paper_id

    def get_paper(self):
        self.paper = self.client.get_note(self.openreview_paper_id)

    def get_paper_reviews(self):
        paper_number = self.paper.number

        invitation_id = f"{self.openreview_group_id}/{self.conference_year}/{self.conference_type }/Submission{paper_number}/-/Official_Review"
        # example: 'ICLR.cc/2024/Conference/Submission{paper_number}/-/Official_Review'

        self.reviews = self.client.get_notes(invitation=invitation_id, details='replies')

    def get_clean_reviews(self):
        cleaned_reviews = []
        for review in self.reviews:
            review_dict = {}
            review_dict["id"] = review.id
            review_dict["content"] = review.content

            review_replies = []
            for reply in reversed(review.details['replies']):
                reply_content = reply['content']
                try:
                    title = reply_content["title"]["value"]
                except:
                    title = ""
                comment = reply_content["comment"]["value"]
                review_replies.append({
                    "title": title,
                    "comment": comment
                })
            review_dict["replies"] = review_replies
            cleaned_reviews.append(review_dict)
        return cleaned_reviews
