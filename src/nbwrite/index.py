import importlib.util
import os
from pathlib import Path
from typing import Any, Dict, List

from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import Language, RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

if os.getenv("NBWRITE_OVERRIDE_SQLITE"):
    # https://docs.trychroma.com/troubleshooting#sqlite
    __import__("pysqlite3")
    import sys

    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")


def create_index(
    pkgs: List[str],
    retriever_kwargs: Dict[str, Any],
    text_splitter_kwargs: Dict[str, Any],
):

    python_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON, **text_splitter_kwargs
    )

    texts = []
    for pkg in pkgs:
        lib = importlib.util.find_spec(pkg)
        code_root = Path(lib.submodule_search_locations[0])  # type: ignore
        loader = GenericLoader.from_filesystem(
            code_root,
            glob="**/*",
            suffixes=[".py"],
            parser=LanguageParser(language=Language.PYTHON, parser_threshold=500),
        )
        texts += python_splitter.split_documents(loader.load())

    db = Chroma.from_documents(texts, OpenAIEmbeddings(disallowed_special=()))
    retriever = db.as_retriever(**retriever_kwargs)

    return retriever
