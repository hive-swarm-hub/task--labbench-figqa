"""LabBench FigQA solver — answers MCQ about scientific figures.

Takes a JSON task on stdin (question, choices, image path), prints the answer letter (A/B/C/D) on stdout.
"""

import sys
import os
import json
import base64

from openai import OpenAI


def solve(question: str, choices: list[str], image_path: str) -> str:
    """Given a question, choices, and an image, return the answer letter (A/B/C/D)."""
    client = OpenAI()

    # Encode image as base64
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()

    choices_text = "\n".join(f"{chr(65+i)}. {c}" for i, c in enumerate(choices))

    response = client.chat.completions.create(
        model=os.environ.get("SOLVER_MODEL", "gpt-4.1-mini"),
        messages=[
            {"role": "system", "content": "You are answering a multiple choice question about a scientific figure. Output ONLY the letter (A, B, C, or D). Nothing else."},
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}},
                {"type": "text", "text": f"{question}\n\n{choices_text}"},
            ]},
        ],
        temperature=0,
        max_tokens=1,
    )
    return response.choices[0].message.content.strip().upper()[:1]


if __name__ == "__main__":
    data = json.loads(sys.stdin.read().strip())
    print(solve(data["question"], data["choices"], data["image_path"]))
