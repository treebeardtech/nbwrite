import datetime
import importlib.util
import os
from pathlib import Path
from typing import Any, Dict, List

from langchain.callbacks import wandb_tracing_enabled as _
from langchain.chat_models import ChatAnyscale
from langchain.llms.openai import OpenAI
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.prompts.chat import HumanMessagePromptTemplate, SystemMessage
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

SYSTEM_PROMPT = """
You are a python programmer

Respond using only Python code
Do not use comments
Do not use quotes
Do not explain anything
Do import any libraries you need
Write 25 lines max per response
"""

template_string = """

task: '{task}'.

nbmake/nb_run.py: {code}"
"""

# Now we can use the NotebookRun class to execute it and check that it printed what we were expecting

# The following class has been imported `nbmake.nb_run.NotebookRun`:


def complete(path: Path, out_path: Path):
    """Write demo notebooks based on prompts in the notebook and the index"""
    # openai.organization = os.getenv("OPENAI_ORG_ID")
    temperature = 0.1
    model = "codellama/CodeLlama-34b-Instruct-hf"

    llm_anyscale = ChatAnyscale(
        temperature=temperature,
        model_name=model,
        streaming=True,
    )

    llm = OpenAI(
        model_name="gpt-4",
        temperature=0.1,
        max_tokens=512,
    )
    task = "Create a hello world notebook 'x.ipynb', use nbmake's NotebookRun class to test it from a Python application"

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=(SYSTEM_PROMPT)),
            HumanMessagePromptTemplate.from_template(template_string),
        ]
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
