import datetime
import os
from pathlib import Path
from typing import Any, Dict, List

from langchain.callbacks import wandb_tracing_enabled as _
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from nbformat import write
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook


def complete(path: Path, out_path: Path):
    """Write demo notebooks based on prompts in the notebook and the index"""
    # openai.organization = os.getenv("OPENAI_ORG_ID")
    temperature = 0.7
    llm = OpenAI(temperature=temperature)
    task = "reverse a list"

    prompt = PromptTemplate.from_template(
        "Write a short Python snippet (max 15 lines) that implements {task}?"
    )
    messages = [HumanMessage(content=prompt.format(task=task))]
    code_out = llm.predict_messages(messages)

    description_prompt = PromptTemplate.from_template(
        "Write a snippet of markdown describing how the following code works to achieve the goal of {task}.\n\n{code}?"
    )
    messages = [
        HumanMessage(content=description_prompt.format(task=task, code=code_out))
    ]
    description_out = llm.predict_messages(messages)
    title = "AI!"
    sources = [code_out.content]
    nb = new_notebook()
    # nb.metadata = metadata
    nb.cells.append(new_markdown_cell(f"# {title}\n\n{description_out.content}"))
    for src in sources:
        nb.cells.append(new_code_cell(src))
    write(nb, str(out_path))
