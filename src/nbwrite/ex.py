from langchain import PromptTemplate

template = """Question: {question}

Answer: """
prompt = PromptTemplate(template=template, input_variables=["question"])

# user question
question = "Which NFL team won the Super Bowl in the 2010 season?"

import os

from langchain.llms import OpenAI

davinci = OpenAI(model_name="text-davinci-003")
from langchain import HuggingFaceHub, LLMChain

llm_chain = LLMChain(prompt=prompt, llm=davinci)

print(llm_chain.run(question))
