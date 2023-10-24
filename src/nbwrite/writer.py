import logging
import os
import re
from dataclasses import dataclass
from datetime import datetime
from operator import itemgetter
from pathlib import Path
from typing import Dict

import click
import nbformat
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.prompts.chat import HumanMessagePromptTemplate
from langchain.schema import format_document
from langchain.schema.messages import SystemMessage
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableParallel
from nbformat.v4 import (
    new_code_cell,
    new_markdown_cell,
    new_notebook,
    reads,
    writes,
)

from nbwrite.config import Config
from nbwrite.constants import TEMPLATE_STRING
from nbwrite.index import create_index

logger = logging.getLogger(__name__)


def get_llm(**llm_kwargs: Dict[str, any]):
    return ChatOpenAI(**llm_kwargs)


def gen(
    config: Config,
):
    now = datetime.now()

    if os.getenv("NBWRITE_PHOENIX_TRACE"):
        click.echo("Enabling Phoenix Trace")
        from phoenix.trace.langchain import (
            LangChainInstrumentor,
            OpenInferenceTracer,
        )

        tracer = OpenInferenceTracer()
        LangChainInstrumentor(tracer).instrument()

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=config.generation.system_prompt),
            HumanMessagePromptTemplate.from_template(TEMPLATE_STRING),
        ]
    )

    retriever = create_index(
        config.packages,
        config.generation.retriever_kwargs,
        config.generation.text_splitter_kwargs,
    )

    def _combine_documents(
        docs, document_prompt=PromptTemplate.from_template(template="{page_content}"), document_separator="\n\n"  # type: ignore
    ):
        doc_strings = [format_document(doc, document_prompt) for doc in docs]
        return document_separator.join(doc_strings)

    llm = get_llm(**config.generation.llm_kwargs) | StrOutputParser()
    chain = (
        {
            "context": itemgetter("task") | retriever | _combine_documents,
            "task": itemgetter("task"),
            "steps": itemgetter("steps"),
            "packages": itemgetter("packages"),
        }
        | prompt
        | RunnableParallel(**{str(gg): llm for gg in range(config.generation.count)})
    )

    click.echo(f"Invoking LLM")
    code_out = chain.invoke(
        {
            "task": config.task,
            "steps": "\n".join(config.steps),
            "packages": "\n".join(config.packages),
        }
    )

    out_dir = Path(config.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    for generation in code_out.keys():
        try:
            nb = new_notebook()

            sections = re.split(r"```(?:python\n)?", code_out[generation])

            for i in range(0, len(sections)):
                if i % 2 == 0:
                    nb.cells.append(new_markdown_cell(sections[i]))
                else:
                    nb.cells.append(new_code_cell(sections[i]))

            time = now.strftime("%Y-%m-%d_%H-%M-%S")
            filename = Path(config.out) / f"{time}-gen-{generation}.ipynb"
            string = writes(nb)
            _ = reads(string)

            nbformat.write(nb, (filename.as_posix()))
            click.echo(f"Wrote notebook to {filename}")
        except Exception as e:
            logger.error(f"Error writing notebook (generation {generation}): {e}")
