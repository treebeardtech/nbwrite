from pathlib import Path

import nbmake

from nbwrite import ex


def test_when_index_then_build_index():
    assert ex.question == "Which NFL team won the Super Bowl in the 2010 season?"


def test_when_gen_nbrun_doc_then_nb_output():
    assert ex.question == "Which NFL team won the Super Bowl in the 2010 season?"


def test_openai():
    # Set user root directory to the 'openai-python' repository
    # root_dir = Path.home()

    import importlib.util

    lib = importlib.util.find_spec("nbmake")

    # Assumes the 'openai-python' repository exists in the user's root directory
    code_root = Path(lib.submodule_search_locations._path[0])
    # from nbwrite.example import extract_functions_from_repo
    # Extract all functions from the repository
    from nbwrite.example_helpers import extract_functions_from_repo

    all_funcs = extract_functions_from_repo(code_root)

    import pandas as pd
    from openai.embeddings_utils import get_embedding

    df = pd.DataFrame(all_funcs)
    df["code_embedding"] = df["code"].apply(
        lambda x: get_embedding(x, engine="text-embedding-ada-002")
    )
    df["filepath"] = df["filepath"].map(lambda x: Path(x).relative_to(code_root))
    # df.to_csv("data/code_search_openai-python.csv", index=False)
    df.head()

    from openai.embeddings_utils import cosine_similarity

    def search_functions(df, code_query, n=3, pprint=True, n_lines=7):
        embedding = get_embedding(code_query, engine="text-embedding-ada-002")
        df["similarities"] = df.code_embedding.apply(
            lambda x: cosine_similarity(x, embedding)
        )

        res = df.sort_values("similarities", ascending=False).head(n)

        if pprint:
            for r in res.iterrows():
                print(
                    f"{r[1].filepath}:{r[1].function_name}  score={round(r[1].similarities, 3)}"
                )
                print("\n".join(r[1].code.split("\n")[:n_lines]))
                print("-" * 70)

        return res

    res = search_functions(df, "fine-tuning input data validation logic", n=3)
