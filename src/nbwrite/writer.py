import importlib.util
from operator import itemgetter
from pathlib import Path

from langchain.chat_models import ChatAnyscale, ChatOpenAI
from langchain.llms.openai import OpenAI
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.prompts.chat import HumanMessagePromptTemplate
from langchain.schema import format_document
from langchain.schema.messages import AIMessage, HumanMessage
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

    temperature = 0
    model = "codellama/CodeLlama-34b-Instruct-hf"

    # llm = ChatAnyscale(
    #     temperature=temperature,
    #     model_name=model,
    #     # streaming=True,
    # )

    llm = ChatOpenAI(
        model_name="gpt-4",
        temperature=temperature,
        max_tokens=512,
    )

    from langchain.agents import tool

    @tool
    def test_script(script: str) -> str:
        """Returns the output of the script."""
        # return "input(f"what is the output?\n\n{script_base64}")"
        return "Success!"

    tools = [test_script]
    from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

    MEMORY_KEY = "chat_history"
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a Python developer. You are good at writing code but bad at knowing what the output will be",
            ),
            MessagesPlaceholder(variable_name=MEMORY_KEY),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    from langchain.tools.render import format_tool_to_openai_function

    llm_with_tools = llm.bind(
        functions=[format_tool_to_openai_function(t) for t in tools]
    )
    from langchain.agents.format_scratchpad import format_to_openai_functions
    from langchain.agents.output_parsers import (
        OpenAIFunctionsAgentOutputParser,
    )

    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_functions(
                x["intermediate_steps"]
            ),
            "chat_history": lambda x: x["chat_history"],
        }
        | prompt
        | llm_with_tools
        | OpenAIFunctionsAgentOutputParser()
    )

    from langchain.agents import AgentExecutor

    agent_executor = AgentExecutor(
        agent=agent, tools=tools, verbose=True, handle_parsing_errors=True
    )

    chat_history = []

    input1 = "how to use the groupby function to plot the iris dataset"
    result = agent_executor.invoke({"input": input1, "chat_history": chat_history})
    chat_history.append(HumanMessage(content=input1))
    chat_history.append(AIMessage(content=result["output"]))
    out = agent_executor.invoke(
        {"input": "what is the output?", "chat_history": chat_history}
    )
    return out["output"]
