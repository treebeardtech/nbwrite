# nbwrite

**Note: This is an experimental use case for LLMs, the output may at times be unhelpful or inappropriate**

nbwrite is a CLI tool which generates notebook-based Python examples using LLMs

Potential use cases include:
1. You are writing a Python package and you want to produce executable tutorials for your stakeholders
2. You are using a Python package and you want to generate a kick-start guide
3. You want to generate regression tests for a python package

## Features

- Converts a set of steps and a task description into an executable Python notebook
- Configurable OpenAI API parameters
- Generate notebooks based on your own code using retrieval augmented generation

## Getting Started

### 1. Install via any Python package manager

```sh
pip install nbwrite
```

### 2. Setup your OpenAI API Access

You will need to create an account and potentially buy credits via https://platform.openai.com/
```sh
export OPENAI_API_KEY='sk-xxxx'
```

### 3. Create a spec file for your generation job

e.g. nbwrite/example1.yaml:
```yaml
task: |
  Plot the iris dataset using pandas
generation:
  count: 2
```

### 4. Generate some notebooks

```sh
nbwrite ./nbwrite/example1.yaml
```

Your outputs will be in your current directory

## Guides

### Generate guides for my closed-source code

You will need to install the 'rag' extra `pip install 'nbwrite[rag]'`

By default, OpenAI's models can generate docs based on parametric knowledge.
This is limited to popular open source libraries.

The `packages` input in the spec file can be used to reference Python packages in your
current environment, which will be indexed in a local Vector DB. Code relevant to the
task is then stuffed into the prompt.

You can pass in an arbitrary number of packages, just remember that the code will be
sent to OpenAI to create embeddings, and this costs money.

example:
```yaml
packages:
  - my_internal_pkg
  - another.internal.pkg
```

### Customise the OpenAI parameters

You can modify both the system prompt and the llm args to try out different OpenAI models,
temperatures, etc. See [Langchain's API ref](https://api.python.langchain.com/en/latest/llms/langchain.llms.openai.BaseOpenAI.html#langchain.llms.openai.BaseOpenAI)

Note! This is a confusing use case -- change it to something relevant to your work.

```yaml
task: |
  Create a hello world notebook 'x.ipynb', use nbmake's NotebookRun class to test it from a Python application
steps:
  - Create a hello world notebook using nbformat
  - Use nbmake's NotebookRun class to execute it from a Python application
  - Check the output notebook printed what we were expecting
packages:
  - nbmake
  - nbformat
  - nbclient
generation:
  count: 2 # number of notebooks to generate
  # system_prompt:
  llm_kwargs:
    # https://api.python.langchain.com/en/latest/llms/langchain.llms.openai.BaseOpenAI.html#langchain.llms.openai.BaseOpenAI
    model_name: gpt-3.5-turbo # The API name of the model as per https://platform.openai.com/docs/models
    temperature: 0.5
  retriever_kwargs:
    k: 3
    search_type: similarity
```

## FAQs and Troubleshooting

### How much does this cost

It depends on (a) the model you use and other params such as context length, (b) the number of outputs you generate.

See OpenAI usage here https://platform.openai.com/account/usage

### Debugging with Phoenix

This is an Alpha stage product, and we encourage you to investigate and report bugs

You will need to install the 'tracing' extra `pip install 'nbwrite[tracing]'`

For any errors occurring during the main generation process, it's possible to view traces
using Phoenix.

1. Start Phoenix with this script

    ```sh
    #! /usr/bin/env python

    import phoenix
    phoenix.launch_app()

    input("Press any key to exit...")
    ```
1. In another termianl, run nbwrite with the following var set: `export NBWRITE_PHOENIX_TRACE=1`
1. Check the phoenix traces in the dashboard (default http://127.0.0.1:6060/)
