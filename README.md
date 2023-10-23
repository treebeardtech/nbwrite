# Nbwrite

nbwrite writes notebook-based documentation for you

Tutorials, guides, demos, examples -- it creates runnable and testable python code which
give your users critical support in using your product.

To write your first notebook, create an ipynb file and use the cli like so

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

TODOs before releasing

- basic eval/testing
- document setup

## Data Security