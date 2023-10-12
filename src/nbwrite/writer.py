import datetime
import os
from pathlib import Path

import openai
from wandb.sdk.data_types.trace_tree import Trace

import wandb


def complete(path: Path):
    """Write demo notebooks based on prompts in the notebook and the index"""
    # openai.organization = os.getenv("OPENAI_ORG_ID")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    temperature = 0.7
    model_name = "gpt-3.5-turbo"
    system_message = "You are Python developer who writes documentation in the form of JSON-based Jupyter notebooks (ipynb files).\nAll of your outputs are valid notebook JSON files with cells that are alternating markdown and Python content. Your tone should be concise, friendly, and professional."
    doc_query = "I need a demo for how to reverse a linked list in Python"
    messages = [
        {
            "role": "system",
            "content": system_message,
        },
        {
            "role": "user",
            "content": doc_query,
        },
    ]
    wandb.init(project="nbgen")

    start_time_ms = round(datetime.datetime.now().timestamp() * 1000)
    response = openai.ChatCompletion.create(
        model=model_name, temperature=temperature, messages=messages
    )

    llm_end_time_ms = round(datetime.datetime.now().timestamp() * 1000)
    token_usage = response["usage"].to_dict()

    root_span = Trace(name="LLMChain", kind="chain", start_time_ms=start_time_ms)
    # wandb.log({f'intermediate.{i}': response_text}, commit=False)
    response_text = response["choices"][0]["message"]["content"]
    llm_span = Trace(
        name="OpenAI",
        kind="llm",
        status_code="success",
        metadata={
            "temperature": temperature,
            "token_usage": token_usage,
            "model_name": model_name,
        },
        start_time_ms=start_time_ms,
        end_time_ms=llm_end_time_ms,
        inputs={"system_prompt": system_message, "query": doc_query},
        outputs={"response": response_text},
    )
    root_span.add_child(llm_span)

    root_span.add_child(llm_span)
    # root_span.add_inputs_and_outputs(
    # inputs={"query": doc},
    # outputs={"response": response_text})

    # update the Chain span's end time
    root_span._span.end_time_ms = llm_end_time_ms

    # add metadata to the trace table
    accuracy = 0.7
    wandb.log({"accuracy": accuracy, "overall_f1": 0.9}, commit=False)
    # log all spans to W&B by logging the root span
    root_span.log(name="docs_trace")
    print(response.choices[0].message)
