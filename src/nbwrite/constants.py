from langchain.prompts import PromptTemplate

DEFAULT_MODEL = "gpt-4-0613"
DEFAULT_ANYSCALE_MODEL = "codellama/CodeLlama-34b-Instruct-hf"
TEMPERATURE = 0.1
MAX_TOKENS = 512
SYSTEM_PROMPT = """
You are a python programmer writing an ipynb document describing a task.

Do install any packages you need using pip
Do import any libraries you need
Write 30 lines max per response
Write snippets of markdown before each section of code
Use a help and authoritative tone
Do not use conversational language
"""

K = 5
SEARCH_TYPE = "mmr" # Also test "similarity"

DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(template="{page_content}")

TEMPLATE_STRING = """
---------------------------------------------------------------
task:

{task}

---------------------------------------------------------------

steps:

{steps}

---------------------------------------------------------------

context:

{context}

---------------------------------------------------------------
"""
