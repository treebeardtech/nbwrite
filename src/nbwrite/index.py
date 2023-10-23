import importlib.util
from pathlib import Path
from typing import List

from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser
from langchain.text_splitter import Language, RecursiveCharacterTextSplitter

from nbwrite.constants import SEARCH_TYPE, K


def create_index(pkgs: List[str], k: int = K, search_type: str = SEARCH_TYPE):

    # https://docs.trychroma.com/troubleshooting#sqlite
    __import__("pysqlite3")
    import sys

    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

    python_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON, chunk_size=2000, chunk_overlap=200
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

    from langchain.embeddings.openai import OpenAIEmbeddings
    from langchain.vectorstores import Chroma

    db = Chroma.from_documents(texts, OpenAIEmbeddings(disallowed_special=()))
    retriever = db.as_retriever(
        search_type=search_type,
        search_kwargs={"k": k},
    )

    return retriever
