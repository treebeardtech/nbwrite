# # from langchain import PromptTemplate

# # template = """Question: {question}

# # Answer: """
# # prompt = PromptTemplate(template=template, input_variables=["question"])

# # # user question
# question = "Which NFL team won the Super Bowl in the 2010 season?"

# # import os

# # from langchain.llms import OpenAI

# # davinci = OpenAI(model_name="text-davinci-003")
# # from langchain import HuggingFaceHub, LLMChain

# # llm_chain = LLMChain(prompt=prompt, llm=davinci)

# # print(llm_chain.run(question))

# # import pinecone

# # pinecone.init(api_key=os.environ["PINECONE_API_KEY"], environment="gcp-starter")
# # index = pinecone.Index("nbwrite")

# # index.upsert(
# #     [
# #         ("A", [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]),
# #         ("B", [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]),
# #         ("C", [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]),
# #         ("D", [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4]),
# #         ("E", [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]),
# #     ]
# # )
