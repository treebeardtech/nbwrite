import os
from pathlib import Path

import openai


def complete(path: Path):
    """Write demo notebooks based on prompts in the notebook and the index"""
    # openai.organization = os.getenv("OPENAI_ORG_ID")
    openai.api_key = os.getenv("OPENAI_API_KEY")

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are Python developer who writes documentation in the form of JSON-based Jupyter notebooks (ipynb files).\nAll of your outputs are valid notebook JSON files with cells that are alternating markdown and Python content. Your tone should be concise, friendly, and professional.",
            },
            {
                "role": "user",
                "content": "I need a demo for how to reverse a linked list in Python",
            },
        ],
    )

    print(completion.choices[0].message)
