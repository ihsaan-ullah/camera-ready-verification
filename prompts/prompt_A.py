prompt = """
You are an expert in reviewing research papers and detecting flaws in them. You are given a research paper in HTML format and its reviews in json format.

Task:
-----
- Carefully examine the reviews and their replies to identify concensus flaws (flaws that the authors have acknowledged and agreed to correct or have corrected)
- Carefully examine the paper to identify the location of the detected concensus flaws. Focus on visible text; ignore HTML tags unless they contain essential content (e.g., equations, figures).
- Give a title and description to the flaws you have identified and categorize them according to the criteria below

Flaw Criteria:
--------------
Category 1: Empirical Evaluation Flaws
(Concerns the experiments and evidence used to support the claims.)
    1a: Insufficient Baselines/Comparisons: The evaluation is missing comparisons to relevant, state-of-the-art, or obvious alternative methods.
    1b: Weak or Limited Scope of Experiments: The experiments are too narrow to support the paper's general claims (e.g., "toy" problems, insufficient data, no real-world testing).
    1c: Lack of Necessary Ablation or Analysis: The paper fails to analyze why its method works, missing ablation studies, cost/scalability analysis, or parameter sensitivity checks.
    1d: Flawed Evaluation Metrics or Setup: The metrics used are inappropriate or misleading, or the experimental setup is unreliable.

Category 2: Methodological & Theoretical Flaws
(Concerns the core technical contribution—the algorithm, model, or theory itself.)
    2a: Fundamental Technical Limitation: The proposed method has an inherent design flaw that severely restricts its applicability or performance (e.g., requires unrealistic inputs, cannot scale by design).
    2b: Missing or Incomplete Theoretical Foundation: The paper requires but lacks a formal theoretical justification for its method (e.g., no convergence guarantees, no formal proof).
    2c: Technical or Mathematical Error: The paper contains a demonstrable error in its mathematical derivations, proofs, or algorithm description.

Category 3: Positioning & Contribution Flaws
(Concerns how the work is framed and what it claims to contribute.)
    3a: Insufficient Novelty / Unacknowledged Prior Work: The core contribution is highly similar to or an uncredited rediscovery of existing work.
    3b: Overstated Claims or Mismatch Between Claim and Evidence: The paper's claims in the abstract, introduction, or conclusion are stronger than what the experimental results actually support.

Category 4: Presentation & Reproducibility Flaws
(Concerns the quality of the writing and the ability for others to understand and use the work.)
    4a: Lack of Clarity / Ambiguity: The paper is written in a way that is ambiguous or difficult to understand, preventing an expert from properly interpreting the work.
    4b: Missing Implementation or Methodological Details: The paper omits crucial details needed for reproduction (e.g., key hyperparameters, data processing steps, source code).

Category 5: Failure to Address Limitations or Ethical Concerns
(Concerns the omission of a proper discussion of the work's boundaries and potential consequences.)
    5a: Unacknowledged Technical Limitations: The paper fails to discuss or downplays obvious or crucial limitations of its method, evaluation, or theoretical assumptions.
    5b: Unaddressed Ethical or Societal Impact: The paper fails to address potential negative societal impacts, risks of misuse, fairness, or other ethical considerations raised by the research.

Instructions:
-------------
After you identify all the flaws in the paper, return **a valid JSON array** of objects for all identified flaws. Each object must include:
- flaw_id: integer id assigned to each assigned flaw
- start_of_flaw: first 5 words of the paragraph where flaw occurs
- end_of_flaw: last 5 words of the paragraph where flaw occurs
- flaw_category: category code (1a–5b) category of the flaw found in the text between start_of_flaw and end_of_flaw
- flaw_title: title of the flaw that you have given to it
- flaw_description: detailed description of the flaw in a pargraph form that describes your undestanding of the flaw
- flaw_severity: (low, medium, high): how severe the flaw is
- flaw_confidence (integer value between 1 and 5, higher value means high confidence): how confident you are about the flaw
- review_id: id of the review where you found this flaw

Formatting Instructions:
------------------------
- You must return only a valid JSON array containing the identified flaws.
- Do NOT include any explanations, comments, or text outside the JSON array.
- Do NOT wrap the JSON array in markdown code markers or any other styling.
- The JSON must be properly formatted so it can be parsed programmatically.
- Each object in the array should exactly follow the specified fields: 
  flaw_id, start_of_flaw, end_of_flaw, flaw_category, flaw_title, flaw_description, flaw_severity, flaw_confidence, review_id.
- If no flaws are found, return an empty JSON array: []

Example JSON response:
----------------------
[
    {
        "flaw_id": 1,
        "start_of_flaw": "our experiments show that the",
        "end_of_flaw": "confidence intervals cannot be found.",
        "flaw_category": "1c",
        "flaw_title": "Missing ablation studies"
        "flaw_description": "The paper fails to analyze why the method works, missing ablation studies and sensitivity checks.",
        "flaw_severity": "low",
        "flaw_confidence": 4,
        "review_id": "REVIEW_ID"
    }
]



Paper:
<START OF PAPER>
{paper}
<END OF PAPER>


Reviews:
<START OF REVIEWS>
{reviews}
<END OF REVIEWS>
"""
