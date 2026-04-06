prompt = """
You are an expert in reviewing research papers and detecting flaws in them. You are given two research papers in HTML format: Submitted paper and Camera ready paper. You are also given flaws identified in the submitted paper in json format.

Task:
-----
- Carefully examine the submitted paper, camera ready paper and the flaws to check if the identified flaws are addressed in the camera ready paper or not.
- Focus on visible text; ignore HTML tags unless they contain essential content (e.g., equations, figures).

Instructions:
-------------
- Exhaustiveness: You must evaluate every single flaw provided in the "Flaws" list. The returned JSON array must contain exactly one object for every input flaw, representing whether it was addressed or not.
After your review, return **a valid JSON array** of objects. Each object must include:

- flaw_id: integer id of the flaw that is addressed (points to flaw_id in the flaws list)
- is_addressed: boolean (true/false) indicating if the flaw was addressed in the camera ready paper
- start_of_flaw_addressed_text: first 5 words of the paragraph where flaw is addressed (null or empty string if is_addressed is false)
- end_of_flaw_addressed_text: last 5 words of the paragraph where flaw is addressed (null or empty string if is_addressed is false)
- flaw_addressed_description: detailed description of how the flaw is addressed (or explaining why it is considered not addressed, if is_addressed is false)
- flaw_addressed_quality (integer value between 1 and 5, higher value means high quality): how well the flaw is addressed you are about the flaw (null if is_addressed is false)
- flaw_addressed_confidence (integer value between 1 and 5, higher value means high confidence): how confident you are about the flaw addressed quality

Formatting Instructions:
------------------------
- You must return only a valid JSON array containing the identified flaws.
- Do NOT include any explanations, comments, or text outside the JSON array.
- Do NOT wrap the JSON array in markdown code markers or any other styling.
- The JSON must be properly formatted so it can be parsed programmatically.
- Each object in the array should exactly follow the specified fields:
  flaw_id, is_addressed, start_of_flaw_addressed_text, end_of_flaw_addressed_text, flaw_addressed_description, flaw_addressed_quality, flaw_addressed_confidence.

Example JSON response:
----------------------
[
    {
        "flaw_id": 1,
        "is_addressed": true,
        "start_of_flaw_addressed_text": "our experiments show that the",
        "end_of_flaw_addressed_text": "confidence intervals cannot be found.",
        "flaw_addressed_description": "The paper fails to analyze why the method works, missing ablation studies and sensitivity checks.",
        "flaw_addressed_quality": 3,
        "flaw_addressed_confidence": 4
    },
    {
        "flaw_id": 2,
        "is_addressed": false,
        "start_of_flaw_addressed_text": null,
        "end_of_flaw_addressed_text": null,
        "flaw_addressed_description": "We searched the camera ready paper but could not find any ablation studies addressing this flaw.",
        "flaw_addressed_quality": null,
        "flaw_addressed_confidence": 5
    }
]



Submitted Paper:
<START OF SUBMITTED PAPER>
{submitted_paper}
<END OF SUBMITTED PAPER>


Camera Ready Paper:
<START OF CAMERA-READY PAPER>
{camera_ready_paper}
<END OF CAMERA-READY PAPER>


Flaws:
<START OF FLAWS>
{flaws}
<END OF FLAWS>
"""
