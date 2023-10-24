# Nbwrite

nbwrite writes notebook-based documentation for you

{{ intro }}


## Quick start

```python
nbwrite \
  my_nb.ipynb \
  output.ipynb \
  --task 'test a notebook from the Python API using the notebook run class' \
  --step 'create an example nb using the nbformat library' \
  --step 'call notebookrun' \
  --step 'check the output' \
  --context nbmake \
  --context another_lib
```

## Guides

{{ how to write a spec file }}

## Data Security

{embeddings and openai}