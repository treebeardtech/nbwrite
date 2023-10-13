import datetime
import importlib.util
import os
from pathlib import Path
from typing import Any, Dict, List

from langchain.callbacks import wandb_tracing_enabled as _
from langchain.llms.openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
from nbformat import write
from nbformat.v4 import (
    new_code_cell,
    new_markdown_cell,
    new_notebook,
    reads,
    writes,
)

lib = importlib.util.find_spec("nbmake")

# Assumes the 'openai-python' repository exists in the user's root directory
code_root = Path(lib.submodule_search_locations._path[0])  # type: ignore
code = (code_root / "nb_run.py").read_text()


def complete(path: Path, out_path: Path):
    """Write demo notebooks based on prompts in the notebook and the index"""
    # openai.organization = os.getenv("OPENAI_ORG_ID")
    temperature = 0.7
    llm = OpenAI(temperature=temperature)
    task = (
        "use nbmake's NotebookRun class to test 'res/x.ipynb' from a Python application"
    )

    prompt = PromptTemplate.from_template(
        "Write an executable Python example in under 50 lines that implements '{task}'.\n\nUse this relevant dependency:\n\n{code}"
    )

    chain = prompt | llm
    code_out = chain.invoke({"task": task, "code": code})
    title = "AI!"
    sources = [code_out]
    nb = new_notebook()
    # nb.metadata = metadata
    nb.cells.append(new_markdown_cell(f"# {title}"))
    for src in sources:
        nb.cells.append(new_code_cell(src))

    # double check some basic structure
    string = writes(nb)
    _ = reads(string)
    write(nb, str(out_path))
