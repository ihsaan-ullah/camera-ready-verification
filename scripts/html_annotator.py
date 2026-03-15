import re
from jinja2 import Environment, FileSystemLoader
from .utils import (
    read_json_file,
    read_html_file,
    save_html_to_file
)


flaw_categories = {
    "1a": "Insufficient Baselines/Comparisons: The evaluation is missing comparisons to relevant, state-of-the-art, or obvious alternative methods.",
    "1b": "Weak or Limited Scope of Experiments: The experiments are too narrow to support the paper's general claims (e.g., \"toy\" problems, insufficient data, no real-world testing).",
    "1c": "Lack of Necessary Ablation or Analysis: The paper fails to analyze why its method works, missing ablation studies, cost/scalability analysis, or parameter sensitivity checks.",
    "1d": "Flawed Evaluation Metrics or Setup: The metrics used are inappropriate or misleading, or the experimental setup is unreliable.",
    "2a": "Fundamental Technical Limitation: The proposed method has an inherent design flaw that severely restricts its applicability or performance (e.g., requires unrealistic inputs, cannot scale by design).",
    "2b": "Missing or Incomplete Theoretical Foundation: The paper requires but lacks a formal theoretical justification for its method (e.g., no convergence guarantees, no formal proof).",
    "2c": "Technical or Mathematical Error: The paper contains a demonstrable error in its mathematical derivations, proofs, or algorithm description.",
    "3a": "Insufficient Novelty / Unacknowledged Prior Work: The core contribution is highly similar to or an uncredited rediscovery of existing work.",
    "3b": "Overstated Claims or Mismatch Between Claim and Evidence: The paper's claims in the abstract, introduction, or conclusion are stronger than what the experimental results actually support.",
    "4a": "Lack of Clarity / Ambiguity: The paper is written in a way that is ambiguous or difficult to understand, preventing an expert from properly interpreting the work.",
    "4b": "Missing Implementation or Methodological Details: The paper omits crucial details needed for reproduction (e.g., key hyperparameters, data processing steps, source code).",
    "5a": "Unacknowledged Technical Limitations: The paper fails to discuss or downplays obvious or crucial limitations of its method, evaluation, or theoretical assumptions.",
    "5b": "Unaddressed Ethical or Societal Impact: The paper fails to address potential negative societal impacts, risks of misuse, fairness, or other ethical considerations raised by the research."
}


class HTMLAnnotator:

    def __init__(self, template_directory, template_file, openreview_paper_id):

        self.template_directory = template_directory
        self.template_file = template_file
        self.openreview_paper_id = openreview_paper_id

        self.submitted_html_paper = ""
        self.camera_ready_html_paper = ""

        self.flaws = []
        self.flaws_addressed = []

        self.annotated_html = ""

    def load_html_papers(self, submitted_filepath, camera_ready_filepath):
        self.submitted_html_paper = read_html_file(filepath=submitted_filepath)
        self.camera_ready_html_paper = read_html_file(filepath=camera_ready_filepath)
        print("[+] Loaded HTML papers")

    def load_flaws(self, json_directory, json_file):
        self.flaws = read_json_file(directory=json_directory, filename=json_file)
        print("[+] Loaded flaws")

    def load_flaws_addressed(self, json_directory, json_file):
        self.flaws_addressed = read_json_file(directory=json_directory, filename=json_file)
        print("[+] Loaded flaws addressed")

    def load_reviews(self, json_directory, json_file):
        self.reviews = read_json_file(directory=json_directory, filename=json_file)
        print("[+] Loaded paper reviews")

    def _highlight_segment(self, html, start, end, flaw_id, side, is_addressed=True):

        flaw_or_addressed = "flaw" if side == "submitted" else "flaw addressed"

        pattern = re.escape(start) + r"(.*?)" + re.escape(end)

        match = re.search(pattern, html, flags=re.DOTALL)

        if not match:
            print(f"❌ Could not locate {flaw_or_addressed} {flaw_id}")
            return html

        extra_class = "" if is_addressed else "unaddressed"

        def replacer(m):
            segment = m.group(0)
            return (
                f'<span class="flaw {extra_class}" '
                f'data-flaw-id="{flaw_id}" '
                f'data-side="{side}">{segment}</span>'
            )

        html = re.sub(pattern, replacer, html, count=1, flags=re.DOTALL)

        return html

    def annotate_html(self):

        submitted_html = self.submitted_html_paper
        camera_html = self.camera_ready_html_paper

        addressed_ids = {f["flaw_id"] for f in self.flaws_addressed}

        for flaw in self.flaws:

            flaw["is_addressed"] = flaw["flaw_id"] in addressed_ids
            flaw["flaw_category_description"] = flaw_categories[flaw["flaw_category"]]

            flaw_id = flaw["flaw_id"]

            start = flaw.get("start_of_flaw")
            end = flaw.get("end_of_flaw")

            if not start or not end:
                continue

            submitted_html = self._highlight_segment(
                submitted_html,
                start,
                end,
                flaw_id,
                "submitted"
            )

        for flaw in self.flaws_addressed:

            flaw_id = flaw["flaw_id"]

            start = flaw.get("start_of_flaw_addressed_text")
            end = flaw.get("end_of_flaw_addressed_text")

            if not start or not end:
                continue

            camera_html = self._highlight_segment(
                camera_html,
                start,
                end,
                flaw_id,
                "camera"
            )

        env = Environment(
            loader=FileSystemLoader(self.template_directory)
        )

        template = env.get_template(self.template_file)

        self.annotated_html = template.render(
            submitted_paper_html=submitted_html,
            camera_ready_paper_html=camera_html,
            flaws=self.flaws,
            flaws_addressed=self.flaws_addressed,
            reviews=self.reviews,
            openreview_paper_id=self.openreview_paper_id
        )

        print("[+] HTML annotated and template rendered")

    def save_annotated_html(self, html_directory, html_file):

        if not self.annotated_html:
            raise ValueError(
                "Annotated HTML not generated. Call annotate_html() first."
            )

        saved_path = save_html_to_file(
            html_content=self.annotated_html,
            directory=html_directory,
            filename=html_file
        )

        print(f"[+] Saved annotated HTML to {saved_path}")
