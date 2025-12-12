from textwrap import dedent

rubric_prompt = dedent("""
You are a strict YES/NO evaluator.
Analyze the provided video frames for their visual content and adherence to the marketing/creative standards below.

**Output Requirement:**
Provide the full **rubric checklist** (YES or NO for every single sub-check).

Return STRICT JSON ONLY based on the required schema. Do not add any text or explanation outside the JSON object.
""").strip()
