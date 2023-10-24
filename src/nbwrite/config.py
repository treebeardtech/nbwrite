from typing import Any, Dict, List

from pydantic import BaseModel

from nbwrite.constants import (
    DEFAULT_LLM_KWARGS,
    DEFAULT_RETRIEVER_KWARGS,
    DEFAULT_SYSTEM_PROMPT,
)


class GenerationConfig(BaseModel):
    count: int = 2
    system_prompt: str = DEFAULT_SYSTEM_PROMPT
    llm_kwargs: Dict[str, Any] = DEFAULT_LLM_KWARGS
    retriever_kwargs: Dict[str, Any] = DEFAULT_RETRIEVER_KWARGS


class Config(BaseModel):
    task: str
    steps: List[str]
    packages: List[str]
    out: str
    generation: GenerationConfig
