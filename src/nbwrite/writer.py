from dataclasses import dataclass
from operator import itemgetter
from pathlib import Path
from typing import List

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

from nbwrite.constants import (
    DEFAULT_DOCUMENT_PROMPT,
    MAX_TOKENS,
    SYSTEM_PROMPT,
    TEMPERATURE,
    TEMPLATE_STRING,
)
from nbwrite.index import create_index


@dataclass
class Config:
    task: str
    steps: List[str]
    packages: List[str]
    out: Path
    models: List[str]
    generations: int
    phoenix_trace: bool


def complete(path: Path, out_path: Path):
    from phoenix.trace.langchain import (
        LangChainInstrumentor,
        OpenInferenceTracer,
    )

    tracer = OpenInferenceTracer()
    LangChainInstrumentor(tracer).instrument()
    code_out = gen(query, placeholder_task, s1, s2, s3, h1, h2, pkgs, k)
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


def gen(
    config: Config,
) -> str:
    """Write demo notebooks based on prompts in the notebook and the index"""
    # openai.organization = os.getenv("OPENAI_ORG_ID")

    llms = {
        mm: OpenAI(model_name=mm, temperature=TEMPERATURE, max_tokens=MAX_TOKENS) for mm in config.models
    }

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessagePromptTemplate.from_template(TEMPLATE_STRING),
        ]
    )

    retriever = create_index(config.packages)

    def _combine_documents(
        docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"  # type: ignore
    ):
        doc_strings = [format_document(doc, document_prompt) for doc in docs]
        return document_separator.join(doc_strings)

    llm = llms[config.models[0]] # TODO make parallel and combine all generations for all models
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
