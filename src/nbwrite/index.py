import importlib.util
from pathlib import Path

from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser
from langchain.text_splitter import Language

# https://docs.trychroma.com/troubleshooting#sqlite
__import__("pysqlite3")
import sys

sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")


def create_index():
    lib = importlib.util.find_spec("nbmake")

    # Assumes the 'openai-python' repository exists in the user's root directory
    code_root = Path(lib.submodule_search_locations._path[0])  # type: ignore
    code = (code_root / "nb_run.py").read_text()

    # Load
    loader = GenericLoader.from_filesystem(
        code_root,
        glob="**/*",
        suffixes=[".py"],
        parser=LanguageParser(language=Language.PYTHON, parser_threshold=500),
    )
    documents = loader.load()
    len(documents)

    from langchain.text_splitter import RecursiveCharacterTextSplitter

    python_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON, chunk_size=2000, chunk_overlap=200
    )
    texts = python_splitter.split_documents(documents)
    len(texts)

    from langchain.embeddings.openai import OpenAIEmbeddings
    from langchain.vectorstores import Chroma

    db = Chroma.from_documents(texts, OpenAIEmbeddings(disallowed_special=()))
    retriever = db.as_retriever(
        search_type="mmr",  # Also test "similarity"
        search_kwargs={"k": 8},
    )

    return retriever
