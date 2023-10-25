from typing import Any, Dict, List

from pydantic import BaseModel

from nbwrite.constants import (
    DEFAULT_LLM_KWARGS,
    DEFAULT_RETRIEVER_KWARGS,
    DEFAULT_SYSTEM_PROMPT,
    DEFAULT_TEXT_SPLITTER_KWARGS,
)


class GenerationConfig(BaseModel):
    count: int = 1
    system_prompt: str = DEFAULT_SYSTEM_PROMPT
    llm_kwargs: Dict[str, Any] = DEFAULT_LLM_KWARGS
    retriever_kwargs: Dict[str, Any] = DEFAULT_RETRIEVER_KWARGS
    text_splitter_kwargs: Dict[str, Any] = DEFAULT_TEXT_SPLITTER_KWARGS


class Config(BaseModel):
    task: str
    steps: List[str] = []
    packages: List[str] = []
    out: str = "nbwrite-out"
    generation: GenerationConfig = GenerationConfig()
