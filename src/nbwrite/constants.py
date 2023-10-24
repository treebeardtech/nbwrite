DEFAULT_LLM_KWARGS = {
    "model": "gpt-4-0613",
    "temperature": 0.1,
    "max_tokens": 512,
}

DEFAULT_TEXT_SPLITTER_KWARGS = {
    "chunk_size": 2000,
    "chunk_overlap": 200,
}

DEFAULT_RETRIEVER_KWARGS = {
    "k": 5,
    "search_type": "mmr",
}

DEFAULT_SYSTEM_PROMPT = """
You are a python programmer writing an ipynb document describing a task.

Do install any packages you need using pip
Do import any libraries you need
Write 30 lines max per response
Write snippets of markdown before each section of code
Use a help and authoritative tone
Do not use conversational language
"""

TEMPLATE_STRING = """
---------------------------------------------------------------
task:

{task}

---------------------------------------------------------------

steps:

{steps}

---------------------------------------------------------------

packages:

{packages}

---------------------------------------------------------------

context:

{context}

---------------------------------------------------------------
"""
