import importlib.util
from operator import itemgetter
from pathlib import Path

from langchain.chat_models import ChatAnyscale
from langchain.llms.openai import OpenAI
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.prompts.chat import HumanMessagePromptTemplate
from langchain.schema import format_document
from langchain.schema.messages import SystemMessage
from langchain.schema.output_parser import StrOutputParser
from nbformat import write
from nbformat.v4 import (
    new_code_cell,
    new_markdown_cell,
    new_notebook,
    reads,
    writes,
)
from phoenix.trace.langchain import LangChainInstrumentor, OpenInferenceTracer

DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(template="{page_content}")

tracer = OpenInferenceTracer()
LangChainInstrumentor(tracer).instrument()


lib = importlib.util.find_spec("nbmake")

# Assumes the 'openai-python' repository exists in the user's root directory
code_root = Path(lib.submodule_search_locations._path[0])  # type: ignore
code = (code_root / "nb_run.py").read_text()

SYSTEM_PROMPT = """
You are a python programmer writing an ipynb document describing a task.

Do install any packages you need using pip
Do import any libraries you need
Write 30 lines max per response
Write snippets of markdown before each section of code
Use a help and authoritative tone
Do not use conversational language
"""

placeholder_task = "Create a hello world notebook 'x.ipynb', use nbmake's NotebookRun class to test it from a Python application"
s1 = "create a hello world notebook using nbformat"
s2 = "use nbmake's NotebookRun class to execute it from a Python application"
s3 = "check the output notebook printed what we were expecting"
h1 = ""
h2 = "use NotebookRun(notebook, timeout)"
query = "use nbmake.nb_run.NotebookRun"


def complete(path: Path, out_path: Path):
    code_out = gen(query, placeholder_task, s1, s2, s3, h1, h2)
    title = "AI!"
    nb = new_notebook()
    # nb.metadata = metadata

    sections = code_out.split("```")

    for i in range(0, len(sections)):
        if i % 2 == 0:
            nb.cells.append(new_markdown_cell(sections[i]))
        else:
            nb.cells.append(new_code_cell(sections[i]))

    # double check some basic structure
    string = writes(nb)
    _ = reads(string)
    write(nb, str(out_path))


template_string = """

task: {guide}

step 1: {step1}
step 2: {step2}
step 3: {step3}

hint 1: {hint1}
hint 2: {hint2}

context:

{context}
"""


def _combine_documents(
    docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"
):
    doc_strings = [format_document(doc, document_prompt) for doc in docs]
    return document_separator.join(doc_strings)


def gen(
    query: str, guide: str, step1: str, step2: str, step3: str, hint1: str, hint2: str
) -> str:
    """Write demo notebooks based on prompts in the notebook and the index"""
    # openai.organization = os.getenv("OPENAI_ORG_ID")

    temperature = 0.1
    model = "codellama/CodeLlama-34b-Instruct-hf"

    llm = ChatAnyscale(
        temperature=temperature,
        model_name=model,
        # streaming=True,
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

    chain = (
        {
            "context": itemgetter("query") | retriever | _combine_documents,
            "guide": itemgetter("guide"),
            "step1": itemgetter("step1"),
            "step2": itemgetter("step2"),
            "step3": itemgetter("step3"),
            "hint1": itemgetter("hint1"),
            "hint2": itemgetter("hint2"),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    code_out = chain.invoke(
        {
            "query": query,
            "guide": guide,
            "step1": step1,
            "step2": step2,
            "step3": step3,
            "hint1": hint1,
            "hint2": hint2,
        }
    )
    return code_out
