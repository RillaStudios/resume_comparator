from typing import Any


class Model:

    name: str
    model: Any
    tokenizer: Any

    def __init__(self, name: str, model: Any, tokenizer: Any):
        self.name = name
        self.model = model
        self.tokenizer = tokenizer