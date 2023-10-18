import datetime
import importlib.util
import os
from pathlib import Path
from typing import Any, Dict, List

# from langchain.callbacks import wandb_tracing_enabled as _
from langchain.chains import RetrievalQA
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
from phoenix.trace.langchain import LangChainInstrumentor, OpenInferenceTracer

# Once you have started a Phoenix server, you can start your LangChain application with the OpenInferenceTracer as a callback. To do this, you will have to instrument your LangChain application with the tracer:


# If no exporter is specified, the tracer will export to the locally running Phoenix server
tracer = OpenInferenceTracer()
LangChainInstrumentor(tracer).instrument()


lib = importlib.util.find_spec("nbmake")

# Assumes the 'openai-python' repository exists in the user's root directory
code_root = Path(lib.submodule_search_locations._path[0])  # type: ignore
code = (code_root / "nb_run.py").read_text()

SYSTEM_PROMPT = """
You are a python programmer writing a markdown document describing a task.

Do install any packages you need using pip
Do import any libraries you need
Write 30 lines max per response
Write snippets of markdown before each section of code
Use a help and authoritative tone
Do not use conversational language
"""


# Now we can use the NotebookRun class to execute it and check that it printed what we were expecting

# The following class has been imported `nbmake.nb_run.NotebookRun`:

placeholder_task = "Create a hello world notebook 'x.ipynb', use nbmake's NotebookRun class to test it from a Python application"
s1 = "create a hello world notebook using nbformat"
s2 = "use nbmake's NotebookRun class to execute it from a Python application"
s3 = "check the output notebook printed what we were expecting"
h1 = "use nbformat"
h2 = "use NotebookRun"


def complete(path: Path, out_path: Path):
    code_out = gen(placeholder_task, s1, s2, s3, h1, h2)
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


def gen(guide: str, step1: str, step2: str, step3: str, hint1: str, hint2: str) -> str:
    """Write demo notebooks based on prompts in the notebook and the index"""
    # openai.organization = os.getenv("OPENAI_ORG_ID")

    template_string = f"""

    task: {guide}

    step 1: {step1}
    step 2: {step2}
    step 3: {step3}

    context:

    {"{context}"}
    """
    temperature = 0.1
    model = "codellama/CodeLlama-34b-Instruct-hf"

    llm = ChatAnyscale(
        temperature=temperature,
        model_name=model,
        streaming=True,
    )

    # llm = OpenAI(
    #     model_name="gpt-4",
    #     temperature=0.1,
    #     max_tokens=512,
    # )

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=(SYSTEM_PROMPT)),
            HumanMessagePromptTemplate.from_template(template_string),
        ]
    )

    from nbwrite.index import create_index

    retriever = create_index()
    chain_type_kwargs = {"prompt": prompt}
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs=chain_type_kwargs,
    )

    # chain = retriever | prompt | llm
    code_out = chain.invoke({"query": "use nbmake.nb_run.NotebookRun"})
    return code_out["result"]
